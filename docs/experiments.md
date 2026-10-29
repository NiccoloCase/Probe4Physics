# Experiment execution

The pipeline is initialization → frozen extraction → probe training → evaluation.
Keep the same resolved backbone configuration when extracting and loading a
cache. This guide describes existing behavior; the cleanup changes no selection,
training, metric, or temporal-control algorithm.

## Extraction and probing

After [data preparation](data.md), an example using the main V-JEPA variant is:

```bash
python run.py extract.intphys2 \
  +backbone.kwargs.variant=vith16_384 \
  +backbone.kwargs.checkpoint_path=/absolute/path/to/vith16-384.pth.tar \
  backbone.kwargs.device=cuda
python run.py train_eval.probe.intphys2 \
  +backbone.kwargs.variant=vith16_384 \
  +backbone.kwargs.checkpoint_path=/absolute/path/to/vith16-384.pth.tar \
  backbone.kwargs.device=cuda \
  probe.name=linear probe.layer=24 probe.device=cpu
```

Hydra requires `+` for kwargs absent from the base YAML, such as `variant` and
`checkpoint_path`. Existing keys, including `device`, take ordinary overrides.
These commands require downloaded assets; their configuration syntax and
fixture-based execution paths are checked without running full GPU workloads.

`probe.name` accepts `linear`, `mlp`, or `temporal_attn`. Feature view `auto`
selects pooled clip vectors for linear/MLP and tokens for attentive probes.
Use `probe.layers=[8,16,24,32]` for a V-JEPA ViT-H layer sweep. Other backbones
have different valid depths; inspect `python run.py health.layers`.

Linear/MLP hyperparameter search is enabled with `probe.optuna.enabled=true`.
The dataset YAMLs define search spaces. Epoch search is disabled by default;
explicitly enable `probe.optuna.search_space.epochs.enabled=true` if required
by the historical configuration. Do not assume generic defaults reproduce a
specific saved experiment.

The implementation saves the epoch with highest validation clip accuracy,
breaking ties by loss. Optuna evaluates that checkpoint using validation pair
consistency or VOE. The paper-result notebooks select best layers using test
scores. These existing choices are preserved.

## Exact historical configurations and seeds

`results/verified_layerwise_probe_configs.csv` and
`results/verified_best_probe_configs.csv` record recovered configurations.
The seed manifests in `results/seed_runs/` specify individual fixed-config runs,
including overrides, seeds, output paths, and source hashes. `main`, `same_L`,
`backbone_sweep`, and `ltx` distinguish experiment groups.

Preview a row before executing it:

```bash
python scripts/run_seed_manifest_row.py \
  --manifest results/seed_runs/seed_manifest_layerwise_main_linear_mlp_v1.csv \
  --probe linear --task-index 0 --dry-run
```

Remove `--dry-run` only after verifying the paths, dataset, seed, and required
cache. The runner validates source rows and blocked status. It intentionally
fails when required evidence is absent or incompatible. Historical absolute
cluster paths may need explicit final Hydra overrides; do not rewrite source
CSV records merely to bypass their hashes.

To collect run outputs, select the corresponding source/manifest and write new
exports below `output/`, rather than overwriting the checked-in evidence:

```bash
python scripts/collect_seed_results.py \
  --manifest results/seed_runs/seed_manifest_layerwise_main_linear_mlp_v1.csv \
  --long-output output/collection/seed_results_long.csv \
  --summary-output output/collection/seed_summary.csv
```

Collection requires the run artifacts referenced by the manifest. Missing runs
must remain visible as missing; they must not be replaced with duplicate seeds.

## Temporal and random-label controls

For either dataset, the retained controls use normal probe checkpoints:

```bash
python run.py extract.mvp.displacement
python run.py eval.probe.mvp.displacement probe.checkpoint_path=/absolute/path/to/probe_best.pt
python run.py extract.mvp.single_frame
python run.py eval.probe.mvp.single_frame probe.checkpoint_path=/absolute/path/to/probe_best.pt
```

Supply the same backbone/layer overrides used for the original probe. These
commands extract only test clips. Displacement is a deterministic non-zero
circular shift within the sampled 16 frames. Single-frame control chooses one
sample-dependent frame and repeats it.

Structured random labels use
`probe.label_control.mode=structured_random` and `probe.label_control.seed=42`
with otherwise fixed training settings. They are shuffled within pairs/scenes
by the existing pipeline. No label-control behavior is changed by the release.

## LTX slots and output artifacts

LTX exposes a noise-by-block grid as ordered slot IDs. With the default 10 noise
levels and four depths there are 40 slots. Slots are noise-major, depth-minor:
`slot = noise_index * 4 + depth_index + 1`. Noise levels are ordered exactly as
listed in `configs/backbones.yaml` (1.0 down to 0.1). For the 48-block variant,
slot 34 is block 24 at noise 0.2. Use manifest slot metadata rather than treating
a slot number as a transformer block number.

Caches contain `index.parquet`, a manifest, pooled tensors, and token tensors
or resumable chunks. Training saves best/last checkpoints and summaries;
evaluation saves predictions, benchmark metrics, and provenance. Configurable
output roots prevent new runs overwriting saved results. See
[reproduction.md](reproduction.md) for the mapping to paper outputs.
