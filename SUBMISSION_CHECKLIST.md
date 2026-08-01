# Submission Checklist

## Verified Complete

- Reusable script entry point: `run_feature_pipeline.py`
- Config layer: `config/feature_config.yaml`
- Modular source code: `src/config.py`, `src/features.py`, `src/pipeline.py`, `src/validation.py`
- Executable tests: `tests/test_features.py`
- README with setup, run instructions, assumptions, limitations, and extension guidance
- Leakage review: `reports/leakage_review.md`
- Feature dictionary: `reports/feature_dictionary.md`
- Validation report: `reports/validation_report.md`
- Supplemental test plan: `reports/supplemental_test_plan.md`
- Feature-ready train dataset: `data/processed/feature_ready_train.csv`
- Feature-ready future/test dataset: `data/processed/feature_ready_test.csv`
- Training target artifact: `data/processed/target_train.csv`

## Real Data Run Evidence

The pipeline was run against Ames/House Prices train and test CSV files.

- Raw train shape: `(1460, 81)`
- Raw test shape: `(1459, 80)`
- Final train feature shape: `(1460, 224)`
- Final test feature shape: `(1459, 224)`
- Train/test feature columns align: yes
- Final feature matrices are numeric-only: yes
- Missing values in final feature matrices: none
- `SalePrice` excluded from feature matrix: yes
- `Id` excluded from feature matrix: yes

## Test Evidence

Tests passed with:

```bash
python -m pytest --basetemp C:\tmp\pytest-bases-assis2 -o cache_dir=C:\tmp\pytest-cache-assis2
```

Result: `4 passed`.

## Note

Raw Kaggle CSV files are not committed to the repository. The processed CSV deliverables and generated reports are committed for assessment review.
