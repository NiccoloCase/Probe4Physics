# Temporal-control cluster jobs

The retained job layout is `jobs/baseline/<control>/<dataset>/<extract|eval>/`.
Datasets are MVP and IntPhys2. `single_frame` repeats a deterministic sampled
frame; the historical `frame_shuffling` folder calls `displacement`, which is a
non-zero circular temporal shift. Both extract only test features and evaluate
existing normal probe checkpoints.

For example, after normal data preparation:

```bash
MODE=smoke sbatch jobs/baseline/frame_shuffling/intphys2/extract/jepa_v1.sh
sbatch jobs/baseline/single_frame/mvp/extract/jepa_v1.sh
```

Evaluation needs the original backbone settings and probe checkpoint. Review
wrapper variables and layer selections before submitting. These are historical
cluster wrappers and may reference older backbone variants; they are not a
substitute for the selected configuration in the paper's saved manifests.
See [experiment controls](../../docs/experiments.md) and
[cluster instructions](../../docs/cluster.md).
