# Release validation

Validation was performed on the `refactor/paper-release` worktree against
research baseline `bbbb6028c0fe984f3ceb9251c50c46443bec9c64`.
The original `main` branch and original local upstream diff remain unchanged.

## Results

| Check | Outcome |
| --- | --- |
| Original CPU suite | 308 tests; seven existing errors, all in the removed SSv2 benchmark's label fixtures |
| Retained suite immediately after SSv2 removal | 269 tests passed |
| Final CPU suite, including release-interface tests | 277 tests passed |
| Public help and recipe listing | Passed; maintenance commands excluded from public registration |
| Configured backbone/layer health | Passed with `strict_exit=true` |
| Manifest dry run | First linear row of `seed_manifest_layerwise_main_linear_mlp_v1.csv` validated and printed without training |
| Paper input integrity | 127 existing result/notebook files match baseline SHA-256 values |
| Notebook execution | All eight notebooks executed in isolated snapshots |
| Numerical/analysis comparison | All 60 exported DataFrame CSVs match baseline after normalizing snapshot-root strings |
| Original checkout protection | `main` still points to `bbbb602`; original V-JEPA submodule patch matches its saved copy |
| Archive preservation | All 673 original tracked regular files copied and checksum-verified before cleanup; 272 original paths now absent from release are indexed in the archive manifest |

Local/default path configurations also resolve exactly to their baseline values
when the original deployment paths are supplied.

The tests exercise CPU fixtures, mocked backbones, cache/resume validation,
checkpoint save/load, label semantics, scoring, command dispatch, and path
configuration. Release-specific coverage checks local defaults, environment
variables, explicit path precedence, health interpolation, README configuration
syntax, and exclusion of removed commands.

No pretrained backbone weights, raw videos, GPU extraction, attentive GPU
training, Slurm submissions, or live hosted CI runs were exercised. The CI
workflow targets Linux/Python 3.11; local validation used Python 3.13.0 with
PyTorch 2.11.0. [The environment record](validation-environment.json) lists all
relevant installed versions. This is not an exact historical experiment lock.

## Saved-result limitations

Notebook execution is not equivalent to complete scientific reproduction.
These diagnostics were already present in the baseline and are unchanged:

- Main layerwise analysis reports eight seed-coverage issues. The selected
  main table reports two, both LTX-13B attentive rows (one per dataset).
- The matched-family comparison reports four incomplete LTX seed rows.
- The backbone-sweep summary reports no seed-coverage issues.
- The seed-traceability notebook reports 37 problematic evidence rows.
- Random-label checkpoint discovery produces missing random-label values in
  its regenerated table because external probe artifacts are absent. The saved
  `results/random_label_controls_main_vs_seed42.csv` contains the paper's
  comparison and is retained unchanged.

The reproduction index distinguishes these cases from complete outputs.
Illustrative figure sources, dedicated compute-table generators, and many
original per-run artifacts are not included. The cleanup neither reconstructs
missing measurements nor changes the interpretation or selection of results.

## Notebook execution safety

`scripts/reproduce_notebooks.py` copies inputs before execution and appends a
DataFrame-export cell only to the executed copy. Its JSON report records cell
errors, and execution returns nonzero if a notebook has errors. Generated CSVs
and figures remain under the selected output directory.

Jupyter needs local kernel sockets. The sandboxed attempt could not start them;
validation succeeded with local socket access enabled. This is an execution-host
restriction, not a dependency on a remote notebook service.

## Upstream checkout limitation on macOS

The recorded V-JEPA upstream commit contains nine pairs of configuration paths
that differ only in case (`vitG` and `vitg`). This Mac's case-insensitive
filesystem cannot materialize both versions. A fresh submodule checkout therefore
reports YAML differences even without source edits. That apparent dirty state
was initially attributed to tests, then traced to the upstream path collisions.
No upstream commit, model code, or submodule reference was changed.

Use a case-sensitive filesystem for an entirely clean upstream checkout. The
original local diff is preserved verbatim in the archive; it was not applied as
a patch to the release. The first-party release worktree is clean after commits.

## Rechecking

```bash
python -m unittest discover -s tests -q
python scripts/verify_release_inputs.py
python run.py help
python run.py exp.list
python run.py health.layers strict_exit=true
python scripts/reproduce_notebooks.py --output-dir output/reproduction/check
```

Choose a new notebook output directory. Full execution reports and test logs
are local validation artifacts under `output/validation/` and the separate
research archive; concise outcomes are recorded here for the public repository.

## Development snapshot verification — October 29, 2026

Before establishing `dev`, the retained CPU suite was rerun: 277 tests passed.
Input verification confirmed all 127 baseline paper files unchanged. CLI help,
recipe listing, configured layer health, and local Markdown file links passed.
The checks used the existing Python 3.13 validation environment recorded above;
no dependency definitions or scientific code changed. Notebooks and GPU workloads
were not rerun for these documentation-only edits. Logs are under ignored
`output/validation/dev-*` paths.

The shared README describes the portable paper workflow and is intended to remain
identical on `dev` and the public release branch. HPC jobs and maintenance tools
remain available in the development snapshot. Archive recovery instructions and
the archive inventory are preserved beside the separate research archive rather
than in the repository documentation.
