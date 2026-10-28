# Third-party code, datasets, and checkpoints

This repository does not change the ownership or licensing of any upstream
asset. Dataset access and weight usage must follow the corresponding upstream
terms. A license for Probe4Physics's own code has not yet been selected.

## Recorded code dependencies

| Component | Upstream | Recorded commit |
| --- | --- | --- |
| MVP evaluation and setup | [facebookresearch/minimal_video_pairs](https://github.com/facebookresearch/minimal_video_pairs) | `0ce9a263882042938d47c1b9a69d0f48a8a9f140` |
| V-JEPA | [facebookresearch/jepa](https://github.com/facebookresearch/jepa) | `51c59d518fc63c08464af6de585f78ac0c7ed4d5` |
| V-JEPA 2 / 2.1 | [facebookresearch/vjepa2](https://github.com/facebookresearch/vjepa2) | `204698b45b3712590f06245fbfba32d3be539812` |

Initialize the Git submodules at those recorded commits. Their license files
and notices stay inside their own directories. The original research checkout has a local configuration diff; its patch is
preserved in the separate archive and is not applied to the release checkout.
The recorded upstream commit contains nine pairs of YAML paths differing only
by case (`vitG` versus `vitg`). On this Mac, a fresh checkout therefore reports
configuration differences because the filesystem cannot represent both paths.
This does not change the recorded commit or model implementation. Use a
case-sensitive filesystem (for example Linux) for a fully clean upstream
checkout; do not commit these filesystem-induced changes.

## Datasets and model weights

- MVP annotations: `facebook/minimal_video_pairs` on Hugging Face; upstream
  setup provides the source-specific video acquisition procedures.
- IntPhys2: `facebook/IntPhys2`; the existing downloader identifies CC BY-NC 4.0.
  Consult the dataset's distribution terms before reuse or redistribution.
- V-JEPA checkpoints: releases linked by the corresponding upstream code.
- VideoMAE / VideoMAE-v2: Hugging Face model identifiers in
  `configs/backbones.yaml`; architecture code can be loaded from the configured
  upstream model snapshots.
- LTX-Video: Lightricks model identifiers in `configs/backbones.yaml`, accessed
  through the existing Diffusers adapter.

No datasets or weights are relicensed by this repository. Check each upstream
license/model card rather than assuming one model's terms cover another variant.
Upstream references to Something-Something v2 describe model provenance or
upstream features, not an additional supported Probe4Physics benchmark.

The paper's bibliography credits the original benchmark, backbone, and probing
work. Citation metadata for this paper is in `CITATION.cff` and the README.
