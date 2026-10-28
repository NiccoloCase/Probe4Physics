# Data and pretrained checkpoints

Run commands from the repository root. Dataset videos and model weights are
external assets and are not distributed with the result spreadsheets.

## Minimal Video Pairs

Initialize submodules and follow `third_party/minimal_video_pairs/README.md` and
its `setup/` instructions to obtain the benchmark videos. The expected root is
`data/videos/mvp`; preserve annotation-relative video paths below that root.

```bash
python run.py init.mvp
```

Initialization can download annotations from `facebook/minimal_video_pairs`
when absent. It selects intuitive-physics binary-plausibility questions,
normalizes semantic yes/no labels, keeps complete pairs, and creates a
60/20/20 split grouped by pair and stratified by source/question template.
Expected paper counts are 4,943 retained pairs: 2,965 train, 989 validation,
989 test. These counts require the original compatible annotations; they were
not re-established from a dataset download during this release cleanup.

Outputs include `split_pairs.parquet`, `manifest.json`, `selection_kept.csv`,
`selection_dropped.csv`, and `selection_report.json` below
`data/splits/mvp/full_60_20_20`. Inspect the selection report before extraction.

## IntPhys2

```bash
python run.py download.intphys2
python run.py init.intphys2
```

The downloader uses `facebook/IntPhys2`, stores videos below
`data/videos/intphys2`, and writes `data/annotations/intphys2_metadata.csv`.
Initialization retains Main and groups four clips per scene, stratifying by
physics condition. Expected paper counts are 253 scenes: 151 train and 51 each
for validation/test. Split outputs are `data/splits/intphys2/split_scenes.parquet`
and `manifest.json`. Regenerating these requires the external dataset.

## Storage configuration

| Environment variable | Default |
| --- | --- |
| `P4P_MVP_VIDEOS_ROOT` | `data/videos/mvp` |
| `P4P_INTPHYS2_VIDEOS_ROOT` | `data/videos/intphys2` |
| `P4P_MVP_FEATURE_DIR` | `artifacts/features/mvp` |
| `P4P_INTPHYS2_FEATURE_DIR` | `artifacts/features/intphys2` |

Explicit Hydra overrides take precedence over these environment defaults:

```bash
python run.py init.mvp videos_root=/absolute/path/to/mvp
python run.py extract.mvp feature_cache.dir=/absolute/path/to/features
```

The latter illustrates storage selection; extraction also requires valid videos,
splits, and a backbone. Readiness checks read dataset YAML defaults; use the
same environment variables for `health` and `health.features` when inspecting
non-default assets. Cluster wrappers additionally expose their own storage
variables; see [cluster.md](cluster.md).

### Existing caches and resumable extractions

Cache signatures and resume validation have not been changed. Preserve all
original scientific settings, annotation/split paths, and backbone overrides.
In particular, MVP's resume configuration records `videos_root` and
`official_repo_root`; changing those strings can invalidate a resume state even
when videos are identical. Point to an existing cache with `feature_cache.dir`
and retain the paths used by its manifest. Never force compatibility by editing
its signature or manifest.

To use the original deployment paths, set:

```bash
export P4P_MVP_VIDEOS_ROOT=/scratch-shared/spunzo1/probe4physics/data/videos/mvp
export P4P_MVP_FEATURE_DIR=/scratch-shared/spunzo1/probe4physics/artifacts/features/mvp
export P4P_INTPHYS2_FEATURE_DIR=/scratch-shared/spunzo1/probe4physics/artifacts/features/intphys2
```

## Checkpoints

`configs/backbones.yaml` records exact adapter variants and expected filenames.
JEPA weights normally live below `data/checkpoints/jepa_v1`, `jepa_v2`, and
`jepa_v2_1`. Existing download jobs are
`jobs/init/backbones/checkpoints_init.sh`, `checkpoints_same_l_init.sh`, and
`checkpoints_jepa_v2_1_sweep_init.sh`. Review their requirements before submitting.
VideoMAE/LTX use the Hugging Face identifiers in the configuration.

Use `python run.py health` to inspect missing assets. This checks readiness;
it does not download weights. Upstream code, datasets, and weights retain their
own terms; see [third_party.md](third_party.md).
