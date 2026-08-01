# Reusable Feature Engineering Pipeline

Author: Dhanraj Yadav

## Purpose and Business Problem

This project prepares the Kaggle House Prices / Ames Housing data for future price modeling and analytics. Earlier one-off preprocessing can create inconsistent feature columns, missing-value rules, encodings, and leakage risk. This repository provides a reusable feature engineering layer that can be reviewed, rerun, tested, and extended.

This project does not train, compare, tune, or submit predictive models.

One row represents one residential property sale or property record. It is not a time series or transaction log.

## Dataset

Use the Kaggle House Prices files:

```text
data/raw/train.csv
data/raw/test.csv
data/raw/data_description.txt
```

Raw Kaggle files are intentionally ignored by Git. The processed assignment outputs are committed and can be regenerated from the raw files.

## Folder Structure

- `config/feature_config.yaml` - project-relative paths, target/ID columns, feature handling rules, missing-value controls, skew/outlier settings, and derived feature switches.
- `src/config.py` - config loading.
- `src/features.py` - cleaning and derived-feature functions.
- `src/pipeline.py` - train-fitted preprocessing, encoding, scaling, export, and documentation outputs.
- `src/validation.py` - raw inspection, schema validation, output validation, and report writing.
- `tests/test_features.py` - executable tests for schema failures, leakage, alignment, unknown categories, derived features, and output files.
- `data/raw/` - local raw Kaggle files.
- `data/processed/` - generated feature-ready outputs.
- `reports/` - validation report, leakage review, feature dictionary, supplemental test plan, and pre-submission audit.

## Environment

Tested with Python 3.12 on Windows. Install dependencies with:

```bash
python -m pip install -r requirements.txt
```

## Run Pipeline

```bash
python run_feature_pipeline.py
```

Generated outputs:

- `data/processed/feature_ready_train.csv` - numeric feature matrix for training rows, no `SalePrice`, no `Id`.
- `data/processed/feature_ready_test.csv` - numeric feature matrix for future/test rows with identical columns and order.
- `data/processed/target_train.csv` - separate `SalePrice` target artifact.
- `reports/validation_report.md`
- `reports/feature_dictionary.md`
- `reports/leakage_review.md`

## Run Tests

```bash
python -m pytest -v
```

## Missing-Value Strategy

Structural missing categorical values for garage, basement, fireplace, pool, alley, fence, and miscellaneous-feature fields are filled with `NA` before encoding. Ordinary categorical missingness uses an explicit `Missing` category before one-hot encoding. Numeric fields use training-fitted median imputation. No rows are silently dropped.

## Encoding Strategy

`MSSubClass` is converted to string and treated as nominal. Nominal features such as `Neighborhood`, `SaleType`, and `SaleCondition` are one-hot encoded. Rare-category grouping is fitted on training data only and then applied to future/test data. Unknown future categories do not crash transformation; they encode to all zeros for that source group unless grouped as `Rare` by the training-fitted rules. Ordinal quality fields use documented Ames domain orderings from config.

## Numeric, Skew, and Outlier Strategy

Numeric features are median-imputed and standard-scaled using training statistics only. `GrLivArea` and `LotArea` are capped at training-only 99.5th percentile thresholds and also exported as `log1p` features. The high `GrLivArea` records are retained to preserve row counts and future scoring consistency, with capping/log transformation used instead of target-dependent row removal.

## Assumptions and Limitations

Sale timing/process fields such as `SaleType`, `SaleCondition`, `MoSold`, and `YrSold` are included under the assumption that scoring occurs when those values are known. If scoring happens earlier, add those fields to `excluded_columns` in config and rerun the pipeline. The fitted preprocessing state is not serialized to disk; rerunning the script fits on the current training file and applies those rules to the current test file.

## How to Add a Feature Safely

1. Add the calculation in `src/features.py`.
2. Ensure it uses columns available in both train and future/test data.
3. Add or update config entries in `config/feature_config.yaml`.
4. Add tests in `tests/test_features.py`.
5. Run `python run_feature_pipeline.py` and `python -m pytest -v`.
6. Update the feature dictionary notes if the feature introduces a new group or timing caveat.
