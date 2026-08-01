# Supplemental Test Plan

- Run the pipeline against the full Kaggle `train.csv` and `test.csv`.
- Review `reports/validation_report.md` for raw shapes, missing-value summaries, schema checks, final shapes, and feature counts.
- Confirm `data/processed/feature_ready_train.csv` includes `SalePrice` only as the final target artifact column and not inside the transformed feature matrix used internally.
- Confirm `data/processed/feature_ready_test.csv` has the same feature columns as the training feature matrix, excluding the training target.
- Spot-check high `GrLivArea` rows and suspicious `GarageYrBlt` values in raw data against the validation report decisions.
- If prediction timing changes, review `SaleType`, `SaleCondition`, `MoSold`, and `YrSold` for availability before scoring.
