# Validation Report

- Raw train shape: (1460, 81)
- Raw test shape: (1459, 80)
- One row definition: One row represents one residential property sale or property record, not a time series or transaction log.
- Top train missing counts: {'PoolQC': 1453, 'MiscFeature': 1406, 'Alley': 1369, 'Fence': 1179, 'MasVnrType': 872, 'FireplaceQu': 690, 'LotFrontage': 259, 'GarageQual': 81, 'GarageFinish': 81, 'GarageType': 81, 'GarageYrBlt': 81, 'GarageCond': 81, 'BsmtFinType2': 38, 'BsmtExposure': 38, 'BsmtCond': 37, 'BsmtQual': 37, 'BsmtFinType1': 37, 'MasVnrArea': 8, 'Electrical': 1, 'Condition2': 0, 'BldgType': 0, 'Neighborhood': 0, 'LandSlope': 0, 'LotConfig': 0, 'Condition1': 0}
- Top test missing counts: {'PoolQC': 1456, 'MiscFeature': 1408, 'Alley': 1352, 'Fence': 1169, 'MasVnrType': 894, 'FireplaceQu': 730, 'LotFrontage': 227, 'GarageYrBlt': 78, 'GarageCond': 78, 'GarageFinish': 78, 'GarageQual': 78, 'GarageType': 76, 'BsmtCond': 45, 'BsmtQual': 44, 'BsmtExposure': 44, 'BsmtFinType1': 42, 'BsmtFinType2': 42, 'MasVnrArea': 15, 'MSZoning': 4, 'BsmtHalfBath': 2, 'Utilities': 2, 'Functional': 2, 'BsmtFullBath': 2, 'BsmtFinSF1': 1, 'Exterior1st': 1}
- Train duplicate rows: 0
- Test duplicate rows: 0
- Numeric source columns after derivation: 62
- Categorical source columns after derivation: 31
- Encoded final feature count: 224
- Final train feature shape: (1460, 224)
- Final test feature shape: (1459, 224)

## Schema and Output Checks
- PASS: schema columns, target placement, ID presence, and duplicate-column checks.
- PASS: train/test feature columns align (224 features).
- PASS: no SalePrice or Id in feature matrix.
- PASS: no missing values in final feature matrices.
- PASS: all final feature columns are numeric.
- PASS: target preserved with 1460 rows.

## Skew and Outlier Handling
- `GrLivArea` capped at training 0.995 quantile (3431.66) and reused for future data.
- `LotArea` capped at training 0.995 quantile (53422.28) and reused for future data.
- `Log1p_GrLivArea` created to handle right skew in `GrLivArea`.
- `Log1p_LotArea` created to handle right skew in `LotArea`.
- High `GrLivArea` records are retained but capped using the training-only quantile, plus a log feature is exported.
- Garage year values after sale year or before 1800 are treated as missing before age calculation.
