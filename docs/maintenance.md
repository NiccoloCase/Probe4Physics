# Maintenance utilities

These tools preserve historical artifact-repair functionality. They are outside
the public paper CLI and are not required when the saved results are used as-is.
They can modify saved artifacts; run them on copies and choose roots explicitly.

```bash
python scripts/maintenance.py backfill.intphys2.roc_auc
python scripts/maintenance.py backfill.baseline_labels \
  '+baseline_backfill.roots=[/absolute/path/to/copied/results]'
```

The dispatcher uses the existing Hydra dataset configuration and unchanged
`training/intphys2_postprocess.py` and `training/baseline_postprocess.py`
implementations. Review their configuration fields before running.

Other preserved scripts build manifests, inspect fit diagnostics, validate caches,
collect seed runs, and export workbooks. Each supports `--help`. Historical
absolute artifact paths are evidence of the originating environment; they are
not guarantees that the corresponding external files are bundled here.

For saved-result analysis, prefer `scripts/reproduce_notebooks.py`, which runs
against copied inputs. Avoid directly executing source notebooks if you want to
keep tracked CSVs and embedded outputs unchanged.
