# Submission Checklist

## Verified

- Reusable script entry point: `run_feature_pipeline.py`
- Config layer: `config/feature_config.yaml`
- Modular source code: `src/config.py`, `src/features.py`, `src/pipeline.py`, `src/validation.py`
- Executable tests: `tests/test_features.py`
- README with setup, run instructions, assumptions, limitations, and extension guidance
- Leakage review: `reports/leakage_review.md`
- Feature dictionary template/generated report location: `reports/feature_dictionary.md`
- Validation report template/generated report location: `reports/validation_report.md`
- Supplemental test plan: `reports/supplemental_test_plan.md`
- Tests pass with:

```bash
python -m pytest --basetemp C:\tmp\pytest-bases-assis2 -o cache_dir=C:\tmp\pytest-cache-assis2
```

## Required Before Final Submission

Add the Kaggle House Prices files:

```text
data/raw/train.csv
data/raw/test.csv
data/raw/data_description.txt
```

Then run:

```bash
python run_feature_pipeline.py
```

This will generate:

- `data/processed/feature_ready_train.csv`
- `data/processed/feature_ready_test.csv`
- `data/processed/target_train.csv`
- refreshed `reports/validation_report.md`
- refreshed `reports/feature_dictionary.md`
- refreshed `reports/leakage_review.md`

## Current Status

The code has been tested with synthetic data and passes. The real feature-ready CSV artifacts cannot be verified or generated until the Kaggle raw CSV files are added locally.
