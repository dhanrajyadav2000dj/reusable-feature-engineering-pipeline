# Leakage Review

- `SalePrice` is separated before preprocessing and never enters the feature matrix.
- `Id` is excluded from all final features.
- Preprocessors are fit on training data only and then applied to future/test data.
- Sale fields such as `SaleType`, `SaleCondition`, `MoSold`, and `YrSold` are included under the assumption that scoring occurs at listing/transaction-preparation time when these values are available. If scoring earlier, move them to `excluded_columns`.
- Age features use `YrSold`, not the current calendar year.
- Derived features use columns present in both train and future/test files.
- High `GrLivArea` is not dropped; it is capped by a training-derived threshold and logged to keep scoring row counts stable.
