# Snellius execution

The existing wrappers target Snellius and assume the `2025` software collection,
`Anaconda3/2025.06-1`, Slurm, and a Conda environment named `probe4physics-gpu`.
They are preserved execution tools, not portable shell launchers. Override
`CONDA_ENV_NAME` when using another compatible environment.

Run from the repository root. Use the existing setup wrapper if provisioning a
cluster environment: `sbatch jobs/init/env/setup_env.sh`. Review storage, partitions,
memory, and wall-time settings before allocating compute.

## Storage

Set dataset/cache paths explicitly rather than relying on another researcher's
scratch directory:

```bash
export P4P_MVP_VIDEOS_ROOT=/scratch-shared/$USER/probe4physics/data/videos/mvp
export P4P_MVP_FEATURE_DIR=/scratch-shared/$USER/probe4physics/artifacts/features/mvp
export P4P_INTPHYS2_FEATURE_DIR=/scratch-shared/$USER/probe4physics/artifacts/features/intphys2
export VIDEOS_ROOT="$P4P_MVP_VIDEOS_ROOT"
export FEATURE_DIR="$P4P_MVP_FEATURE_DIR"
```

The `P4P_*` variables configure dataset YAMLs and health checks. Extraction
wrappers additionally accept `VIDEOS_ROOT`, `FEATURE_DIR`, `SPLIT_DIR`, and
`PROJECT_ROOT`. `FEATURE_DIR` and dataset-specific values must be changed when
switching benchmarks. Hugging Face caches default to your own scratch space
through `jobs/extract/common.sh`.

## Submission examples

After preparing annotations, splits, videos, and weights:

```bash
mkdir -p output/training output/baseline
MODE=smoke sbatch jobs/extract/mvp/jepa_v1.sh
sbatch jobs/train/seed_runs/layerwise_main_linear_cpu_array.sh --dry-run
```

The extraction smoke mode processes two ordered clips; it does not represent
full extraction. Manifest array dry runs print the intended command but do not
train. Review the wrapper's array range and manifest before full submission.
Use [experiments.md](experiments.md) to inspect a manifest row without Slurm.

Linear/MLP jobs use CPU partitions; attentive jobs and backbone extraction use
GPU partitions. Historical wrappers include A100/H100 settings and different
training regimes. In particular, older attentive wrappers are not equivalent
to all final paper manifests. Select the intended saved configuration rather
than treating every retained job as the canonical paper experiment.

Temporal wrappers remain under `jobs/baseline/`; their `frame_shuffling`
folder executes the circular displacement control. No cluster jobs were
submitted during release validation. Dataset, scheduler, memory, and GPU
compatibility must be checked on the target system.
