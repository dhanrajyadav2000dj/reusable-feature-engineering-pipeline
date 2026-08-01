# Leakage Review

- `SalePrice` is separated before preprocessing and does not enter the feature matrix.
- `Id` is excluded from all final features.
- Imputers, scalers, encoders, rare-category rules, and outlier caps are fit on training data only.
- Age features use `YrSold`, not the current calendar year.
- `MSSubClass` is treated as categorical because it is a building-class code.
- Sale fields such as `SaleType`, `SaleCondition`, `MoSold`, and `YrSold` are included only under the assumption that scoring occurs at transaction-preparation time. If scoring happens earlier, exclude these fields in config.
- Derived features are built from fields present in both train and future/test data.
