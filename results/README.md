# Experiment configuration records

The public release keeps this directory for selected configurations and run
instructions. Measurement workbooks, aggregated paper scores, historical backups,
and performance-analysis exports are retained on the development branch.

## Retained inputs

| Files | Purpose |
| --- | --- |
| `verified_best_probe_configs.csv` | Recovered selected configurations used by the default seed manifest |
| `verified_layerwise_probe_configs.csv` | Per-layer settings used by layerwise, backbone-scale, and matched-family runs |
| `seed_runs/seed_manifest*.csv` | Fixed-configuration rerun instructions, seeds, overrides, and source-row hashes |
| `seed_runs/jepa_v2_mlp_layerwise_seed_source_v1.csv` | Configuration source required by the JEPA v2 MLP manifest |
| `seed_runs/attentive_continuation_manifest_v1.csv` | Historical attentive-resume instructions and source-manifest references |

These files remain byte-for-byte unchanged from the research baseline. Source
configuration rows include historical metric and provenance fields because the
manifest validators hash entire rows. Those fields are retained to preserve
validation and configuration selection; they are not newly generated results.
Do not strip columns or rewrite paths in these checked-in records.

```bash
python scripts/verify_release_inputs.py
```

## Running and collecting new experiments

Use `scripts/run_seed_manifest_row.py` to preview or execute a row, supplying
local execution paths as final Hydra overrides. See
[experiments](../docs/experiments.md) for a complete command example. Write new
metrics and collection exports below ignored `artifacts/` or `output/` paths.
When collecting newly executed manifest rows, use `--no-source-seed` to avoid
mixing new measurements with historical source-row scores. Set `--expected-seeds`
to the seeds actually being collected; full paper comparisons require the
recorded three-seed protocol, including a newly executed seed 42.

Historical paths do not mean the referenced files are bundled. In particular,
attentive continuation validation requires the original source checkpoint and
training summary before execution overrides are applied. Without those assets,
that historical resume path is unavailable; a fresh training run is a distinct
execution and must not be presented as a validated continuation.

Raw videos, pretrained weights, feature caches, trained probes, and original
per-run outputs are external. The public release does not regenerate paper
plots from included measurements. See [reproduction](../docs/reproduction.md)
for the workflow and availability limits.
