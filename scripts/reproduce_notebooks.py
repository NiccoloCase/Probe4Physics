"""Execute unchanged paper notebooks in a disposable snapshot of their inputs."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import sys

DEFAULT_NOTEBOOKS = ('main', 'main_accuracy', 'large_ablation', 'backbone_ablation',
                     'temporal_controls_table', 'random_label_controls_table', 'parameter_counts')

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--notebooks', nargs='+', choices=DEFAULT_NOTEBOOKS, default=list(DEFAULT_NOTEBOOKS))
    args = parser.parse_args()
    root, out = args.repo_root.resolve(), args.output_dir.resolve()
    if out.exists():
        parser.error('Output directory already exists; choose a new run directory.')
    if out.is_relative_to(root) and not out.is_relative_to(root / 'output'):
        parser.error('Inside the repository, outputs must be below output/, never source or result inputs.')
    if root == out or root.is_relative_to(out):
        parser.error('Output directory must not contain the source repository.')
    from nbclient import NotebookClient
    import nbformat
    from jupyter_client import AsyncKernelManager

    class PythonKernelManager(AsyncKernelManager):
        """Use this interpreter and let nbclient own the kernel lifecycle."""
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.kernel_spec.argv = [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
    out.mkdir(parents=True)
    snapshot = out / 'snapshot'
    snapshot.mkdir()
    for dirname in ('notebooks', 'results', 'configs', 'models', 'scripts'):
        shutil.copytree(root / dirname, snapshot / dirname,
                        ignore=shutil.ignore_patterns('__pycache__', '.ipynb_checkpoints'))
    shutil.copy2(root / 'run.py', snapshot / 'run.py')
    report = {'python': sys.version, 'source_root': str(root), 'notebooks': {}}
    for name in args.notebooks:
        path = snapshot / 'notebooks' / f'{name}.ipynb'
        nb = nbformat.read(path, as_version=4)
        nb.cells.append(nbformat.v4.new_code_cell(
            "from pathlib import Path as _ReleasePath\n"
            "import pandas as _release_pd\n"
            f"_release_export = _ReleasePath({str(out / 'tables' / name)!r})\n"
            "_release_export.mkdir(parents=True, exist_ok=True)\n"
            "for _release_name, _release_value in list(globals().items()):\n"
            "    if isinstance(_release_value, _release_pd.DataFrame) and not _release_name.startswith('_release'):\n"
            "        _release_value.to_csv(_release_export / (_release_name + '.csv'), index=False)\n"))
        client = NotebookClient(nb, kernel_manager_class=PythonKernelManager, kernel_name='python3',
                                startup_timeout=180, timeout=600, allow_errors=True,
                                resources={'metadata': {'path': str(snapshot / 'notebooks')}})
        print(f'Executing {name}', flush=True)
        try:
            client.execute()
            errors = [{'cell': i, 'type': output.ename, 'message': output.evalue}
                      for i, cell in enumerate(nb.cells)
                      for output in cell.get('outputs', []) if output.output_type == 'error']
            report['notebooks'][name] = {'status': 'failed' if errors else 'passed', 'errors': errors}
        except Exception as exc:
            report['notebooks'][name] = {'status': 'failed', 'errors': [{'type': type(exc).__name__, 'message': str(exc)}]}
        nbformat.write(nb, out / f'{name}.ipynb')
        (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    raise SystemExit(int(any(row['status'] != 'passed' for row in report['notebooks'].values())))

if __name__ == '__main__':
    main()
