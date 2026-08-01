from pathlib import Path

import yaml


def load_config(path: str | Path = "config/feature_config.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)
