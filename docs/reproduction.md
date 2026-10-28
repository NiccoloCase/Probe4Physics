# Paper reproduction index

This index refers to the numbered outputs in *How Do Video Foundation Models
Encode Intuitive Physics? Probing Across Pretraining Paradigms*, NeurIPS 2026
Workshop on World Models in Physical AI. It identifies generating analyses and
missing inputs; it is not a claim that the checkout independently reconstructs
every number, error bar, or editorial layout in the paper.

## Execute saved-result analyses

```bash
python scripts/verify_release_inputs.py
python scripts/reproduce_notebooks.py --output-dir output/reproduction/paper
```

The runner makes a disposable snapshot of `results/`, `notebooks/`, `configs/`,
`models/`, and `scripts/`. Executed notebooks are at the output root, exported
DataFrames at `tables/<notebook>/`, and notebook-native saved images/CSVs under
`snapshot/`. Figures not explicitly saved remain visible inside the executed
notebook. Original notebooks and result inputs are never executed in-place.
Use a new output directory for each invocation.

For one notebook, append `--notebooks <name>` without the `.ipynb` extension.
The names below are exact accepted arguments. Every notebook also runs in the
all-notebook command above.

## Numbered tables

| Paper output | Inputs | Generator / command | Output and availability |
| --- | --- | --- | --- |
| Table 1: largest-backbone probe comparison | Primary MVP/IntPhys2 workbooks plus ready seed/continuation summaries | `--notebooks main` | `tables/main/table1_display.csv`, LaTeX in executed notebook, selected rows in `_table1_best.csv`. Two selected LTX attentive rows have incomplete seed evidence in the local baseline. |
| Table 2: retained MVP template groups | Original MVP annotations and retained selection/split metadata | `python run.py init.mvp`; inspect `selection_kept.csv` and `selection_report.json` | Metadata generated below `data/splits/mvp/full_60_20_20`. Videos/annotations and a dedicated publication-table formatter are not bundled. |
| Table 3: MVP selection summary | Same annotations and selection settings | `python run.py init.mvp` | `selection_report.json` supplies selection counts. Dataset access is required; the exact table layout has no dedicated generator. |
| Table 4: model/backbone specification | `configs/backbones.yaml`, adapter metadata, parameter-count helpers | `--notebooks parameter_counts` | Parameter/layer tables in executed notebook and CSV exports. A combined publication-layout table is not generated automatically; exact checkpoint scopes must be checked against the adapter metadata. |
| Table 5: probe search spaces/settings | Dataset YAMLs, saved configurations, seed manifests | Inspect `configs/`, `results/verified_layerwise_probe_configs.csv`, and the relevant manifest | This is a methodology table, not a measurement export. Generic YAML defaults and older wrappers differ from some final-run settings; no dedicated formatter is present. |
| Table 6: temporal controls | `controls_db.xlsx`, recovered layerwise seed-42 configurations | `--notebooks temporal_controls_table` | `tables/temporal_controls_table/temporal_paper_table.csv`, plus the copied `snapshot/results/temporal_controls_main_vs_seed42.csv`. |
| Table 7: random-label comparison | Saved comparison CSV; notebook additionally discovers external checkpoints | `--notebooks random_label_controls_table` | The included `results/random_label_controls_main_vs_seed42.csv` preserves the paper comparison. Notebook regeneration yields missing random-label values without external checkpoints; do not overwrite the saved comparison with that partial output. |
| Table 8: extraction compute | Original extraction job timings and run logs | Historical extraction jobs; logs preserved in the local research archive | No dedicated timing-table generator or complete portable raw timing dataset is included. Full independent regeneration is not verified. |
| Table 9: probe search compute | Original probe job timings and search workloads | Historical probe jobs; logs preserved in the local research archive | No dedicated timing-table generator is included. Hardware and original workloads are needed to remeasure compute. |

To inspect the saved Table 7 values without checkpoint discovery:

```bash
python -c 'import pandas as pd; print(pd.read_csv("results/random_label_controls_main_vs_seed42.csv").to_string(index=False))'
```

## Numbered figures

| Paper output | Inputs | Generator / command | Output and availability |
| --- | --- | --- | --- |
| Figure 1: layerwise MLP profiles | Primary workbooks and seed summaries | `--notebooks main` | Layerwise MLP plot variants embedded in executed notebook; `tables/main/results.csv` holds plot inputs. |
| Figure 2: backbone-scale bars | Primary workbooks, backbone-sweep summaries | `--notebooks backbone_ablation` | Best-backbone bar variants in executed notebook; `tables/backbone_ablation/backbone_best.csv`. |
| Figure 3: matched-family comparison | Same-L workbooks/summaries, LTX references | `--notebooks large_ablation` | Saved `snapshot/notebooks/large_ablation*.png`, embedded figures, `best_large.csv`, and `pairwise_significance.csv`. Four selected LTX comparison rows have incomplete seed coverage. |
| Figure 4: IntPhys2 illustrations | Source dataset/paper imagery | No editable generator in this repository | Illustrative artwork; source layout/assets are not bundled. |
| Figure 5: MVP adaptation illustration | Source MVP imagery and diagram artwork | No editable generator in this repository | Illustrative artwork; source layout/assets are not bundled. |
| Figure 6: all-probe layer profiles | Same inputs as Figure 1 | `--notebooks main` | All-probe appendix plot in executed notebook. |
| Figure 7: LTX linear block/noise grid | LTX entries in primary workbooks and seed summaries | `--notebooks main` | Linear heatmaps in executed notebook; underlying rows in `results.csv`. |
| Figure 8: LTX MLP block/noise grid | Same LTX measurement inputs | `--notebooks main` | MLP heatmaps in executed notebook; underlying rows in `results.csv`. |
| Figure 9: backbone depth profiles | Same inputs as Figure 2 | `--notebooks backbone_ablation` | Depth-profile figures in executed notebook; `backbone_sweep.csv`. |
| Figure 10: temporal-control attentive scores | Same inputs as Table 6 | `--notebooks temporal_controls_table` | Absolute attentive-control plot in executed notebook; `absolute_table.csv` and `temporal_paper_table.csv`. |

`main_accuracy` preserves secondary clip-accuracy plots.
`seed_traceability_status` exports the availability audit; it is not a numbered
paper figure. All existing plot code, layer selection, statistics, and seed
policies are unchanged. Plot variants may need editorial selection to match a
particular paper layout; the runner does not invent unavailable figure sources.

## Full experimental reruns

Follow [data preparation](data.md), [experiments](experiments.md), and
[cluster submission](cluster.md). The saved configuration records and seed
manifests specify historical experiments; a single generic CLI invocation does
not replace the complete run matrix. The same checkpoints and resolved
extraction settings must be used when training from a feature cache.

The checkout excludes raw videos, pretrained weights, feature caches, trained
probe checkpoints, and many per-run cluster JSON artifacts. It also excludes
editable illustrative artwork. These availability gaps remain explicit rather
than being reconstructed from rounded paper numbers.

## What was verified

Eight notebooks execute on the included saved inputs. Sixty DataFrame CSV
exports match the pre-cleanup baseline after normalizing disposable snapshot
paths. Notebook execution is distinct from complete seed/checkpoint provenance:
coverage warnings and missing random-label artifacts remain visible. See
[validation.md](validation.md) for the environment and detailed limits.
