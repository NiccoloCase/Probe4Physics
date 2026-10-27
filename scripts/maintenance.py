"""Run preserved artifact-repair utilities outside the public paper CLI."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('backfill.intphys2.roc_auc', 'backfill.baseline_labels'))
    args, overrides = parser.parse_known_args()
    from omegaconf import OmegaConf
    from run import _compose_config
    from training.baseline_postprocess import run_baseline_label_backfill
    from training.intphys2_postprocess import run_intphys2_backfill_roc_auc

    config_name = 'intphys2' if args.operation == 'backfill.intphys2.roc_auc' else 'mvp'
    config = OmegaConf.to_container(_compose_config(config_name, overrides), resolve=True)
    handler = (run_intphys2_backfill_roc_auc if config_name == 'intphys2'
               else run_baseline_label_backfill)
    print(json.dumps(handler(config), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
