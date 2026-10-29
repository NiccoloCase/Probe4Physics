# Development and validation

Target Python 3.11. Keep the existing typed Python style, four-space indentation,
and dataset-specific code under `benchmarks/`. `run.py` is the public launcher;
its help is generated from the command registry. Shared model defaults belong
in configuration, and cluster wrappers should declare runtime requirements.

## Local checks

```bash
python -m unittest discover -s tests -q
python -m unittest tests.test_run_commands tests.test_release_cli tests.test_release_config -q
python scripts/verify_release_inputs.py
python run.py help
python run.py exp.list
python run.py health.layers strict_exit=true
```

Tests use CPU fixtures, temporary directories, and mocked backbone forwards.
They cover cache/resume semantics, labels, metrics, adapters, checkpoint loading,
training orchestration, and the command interface. No weights or videos need to
be downloaded to run the test suite. GPU behavior is outside this suite.

`health` and `health.features` additionally inspect external model/dataset/cache
readiness; a fresh checkout may legitimately fail those readiness checks. Do not
use their missing-asset results as evidence of unit-test failures.

## Notebook safety

Use `scripts/reproduce_notebooks.py` to execute analyses in copied input trees.
The original notebooks may write tracked CSVs if executed in-place. New output
belongs below ignored `output/`, `artifacts/`, or `logs/` paths. Never commit
videos, weights, caches, W&B files, or job output logs.

The CPU CI workflow checks tests, input hashes, public commands, and configured
layer mappings. It does not run cluster jobs or assert that all external paper
artifacts are present. Review generated notebook diagnostics alongside outputs.

## Scientific compatibility

A release-only edit must preserve split membership, semantic labels, cache
signatures, model preprocessing, optimizer settings, RNG ordering, checkpoint
selection, scoring, and existing result-selection logic. Add targeted regression
coverage for changed interfaces or paths rather than broad tests that merely
mirror the implementation. Keep upstream submodule commits stable.

Use separate commits for independent cleanup steps and state how each was
validated. Project licensing remains a coauthor decision. See
[validation.md](validation.md) for this release's recorded checks. The original
research snapshot is preserved at commit `bbbb6028c0fe984f3ceb9251c50c46443bec9c64`;
historical files and recovery records are retained in the separate local research
archive.
