# Saved experimental results

This directory contains versioned inputs to paper analysis, not newly generated
runtime output. All existing CSV/XLSX files are preserved byte-for-byte from
research commit `bbbb602`. Verify them with:

```bash
python scripts/verify_release_inputs.py
```

## Input roles

| Files | Role |
| --- | --- |
| `mvp_primary_db.xlsx`, `intphys_primary_db.xlsx` | Original per-model/per-layer measurement workbooks |
| `visualization_ready_results.xlsx` | Historical visualization export, retained for compatibility |
| `verified_layerwise_probe_configs.csv` | Recovered configurations and seed-42 metrics across layers |
| `verified_best_probe_configs.csv` | Historical selected configurations and evidence references |
| `controls_db.xlsx` | Temporal-control measurements |
| `temporal_controls_main_vs_seed42.csv` | Saved derived temporal-control table |
| `random_label_controls_main_vs_seed42.csv` | Saved main/random-label comparison used for paper Table 7 |
| `random_label_controls_table.csv` | Older random-label run summary; distinct from the final comparison |
| `seed_runs/*summary*.csv`, associated long CSVs | Seed aggregation and coverage records |
| `seed_runs/seed_manifest*.csv` | Fixed-config run instructions and source hashes |
| `seed_runs/*continuation*`, `*audit*` | Attentive continuation policy and execution evidence |
| `imports/` | Imported external-run evidence and audit notes |

The notebooks combine source workbooks with ready seed summaries through
`notebooks/seed_variance_loader.py`. That loader has an explicit precedence
between original summaries, attentive continuations, and ready manifests.
A workbook alone is therefore not the complete source of the final analysis.
Do not replace a missing seed by duplicating another seed or merge files solely
because their names appear similar.

Some provenance fields reference cluster artifacts or historical log paths.
Those strings are preserved, including hashes used by manifest validation.
Historical logs remain recoverable in the separate archive. Raw videos, feature
caches, trained checkpoints, and many per-run JSON outputs are not bundled.

## Generating new outputs

Use a fresh `output/reproduction/<run>` directory through the notebook runner.
It copies this directory before executing notebooks that write CSVs, ensuring
the original evidence remains unchanged. Its `tables/` exports expose loaded
DataFrames, selected layers, statistics, and coverage issues for comparison.

Notebook execution can succeed while reporting incomplete evidence. In the
release baseline, selected main-table LTX attentive rows lack complete seed
coverage, and random-label checkpoint discovery cannot regenerate Table 7
without external checkpoints. The saved Table 7 comparison CSV remains included.
See [reproduction](../docs/reproduction.md) for these limits.
