# Reusable Feature Engineering Pipeline

This project prepares the Kaggle House Prices / Ames Housing data for future modeling and analytics. It focuses on reusable feature engineering, validation, documentation, and train/future consistency. It does not train, compare, or tune predictive models.

One row represents one residential property sale or property record, not a time series or transaction log.

## Folder Structure

- `config/feature_config.yaml` - paths, target/ID columns, feature handling rules, missing-value controls, and derived feature settings.
- `src/` - reusable loading, validation, cleaning, feature engineering, encoding, scaling, and reporting code.
- `tests/` - executable pytest tests for alignment, leakage, unknown categories, schema validation, and derived features.
- `data/raw/` - place Kaggle `train.csv`, `test.csv`, and optionally `data_description.txt` here.
- `data/processed/` - generated feature-ready train/test outputs.
- `reports/` - generated validation report, leakage review, and feature dictionary.

## Setup

```bash
python -m pip install -r requirements.txt
```

Download the Kaggle House Prices files and place them here:

```text
data/raw/train.csv
data/raw/test.csv
data/raw/data_description.txt
```

## Run

```bash
python run_feature_pipeline.py
```

Generated outputs:

- `data/processed/feature_ready_train.csv`
- `data/processed/feature_ready_test.csv`
- `data/processed/target_train.csv`
- `reports/validation_report.md`
- `reports/feature_dictionary.md`
- `reports/leakage_review.md`

## Tests

```bash
python -m pytest
```

The tests use synthetic data, so they can run even before the Kaggle files are added.

## Key Assumptions

- `SalePrice` is the target and is excluded from the feature matrix.
- `Id` is retained only as an identifier in raw data and is excluded from final features.
- `MSSubClass` is treated as an unordered categorical code.
- Age features use `YrSold`, not the current calendar year.
- Encoders, imputers, rare-category rules, caps, and scalers are fit on training data only.
- Sale timing and sale-process fields are included under the assumption that scoring occurs when those values are known. If the prediction point is earlier, add those fields to `excluded_columns`.

## How to Add a Feature Safely

1. Add the calculation in `src/features.py`.
2. Ensure it uses columns available in both train and future/test data.
3. Add or update config entries in `config/feature_config.yaml`.
4. Add a test in `tests/test_features.py`.
5. Run `python -m pytest` and `python run_feature_pipeline.py`.
6. Update the feature dictionary notes if the feature introduces a new group or timing caveat.
