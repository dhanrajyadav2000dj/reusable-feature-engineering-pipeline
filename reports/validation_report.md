# Validation Report

- Raw train shape: (1460, 81)
- Raw test shape: (1459, 80)
- One row definition: One row represents one residential property sale or property record, not a time series or transaction log.
- Top train missing counts: {'PoolQC': 1453, 'MiscFeature': 1406, 'Alley': 1369, 'Fence': 1179, 'MasVnrType': 872, 'FireplaceQu': 690, 'LotFrontage': 259, 'GarageQual': 81, 'GarageFinish': 81, 'GarageType': 81, 'GarageYrBlt': 81, 'GarageCond': 81, 'BsmtFinType2': 38, 'BsmtExposure': 38, 'BsmtCond': 37, 'BsmtQual': 37, 'BsmtFinType1': 37, 'MasVnrArea': 8, 'Electrical': 1, 'Condition2': 0, 'BldgType': 0, 'Neighborhood': 0, 'LandSlope': 0, 'LotConfig': 0, 'Condition1': 0}
- Top test missing counts: {'PoolQC': 1456, 'MiscFeature': 1408, 'Alley': 1352, 'Fence': 1169, 'MasVnrType': 894, 'FireplaceQu': 730, 'LotFrontage': 227, 'GarageYrBlt': 78, 'GarageCond': 78, 'GarageFinish': 78, 'GarageQual': 78, 'GarageType': 76, 'BsmtCond': 45, 'BsmtQual': 44, 'BsmtExposure': 44, 'BsmtFinType1': 42, 'BsmtFinType2': 42, 'MasVnrArea': 15, 'MSZoning': 4, 'BsmtHalfBath': 2, 'Utilities': 2, 'Functional': 2, 'BsmtFullBath': 2, 'BsmtFinSF1': 1, 'Exterior1st': 1}
- Train column names: ['Id', 'MSSubClass', 'MSZoning', 'LotFrontage', 'LotArea', 'Street', 'Alley', 'LotShape', 'LandContour', 'Utilities', 'LotConfig', 'LandSlope', 'Neighborhood', 'Condition1', 'Condition2', 'BldgType', 'HouseStyle', 'OverallQual', 'OverallCond', 'YearBuilt', 'YearRemodAdd', 'RoofStyle', 'RoofMatl', 'Exterior1st', 'Exterior2nd', 'MasVnrType', 'MasVnrArea', 'ExterQual', 'ExterCond', 'Foundation', 'BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinSF1', 'BsmtFinType2', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF', 'Heating', 'HeatingQC', 'CentralAir', 'Electrical', '1stFlrSF', '2ndFlrSF', 'LowQualFinSF', 'GrLivArea', 'BsmtFullBath', 'BsmtHalfBath', 'FullBath', 'HalfBath', 'BedroomAbvGr', 'KitchenAbvGr', 'KitchenQual', 'TotRmsAbvGrd', 'Functional', 'Fireplaces', 'FireplaceQu', 'GarageType', 'GarageYrBlt', 'GarageFinish', 'GarageCars', 'GarageArea', 'GarageQual', 'GarageCond', 'PavedDrive', 'WoodDeckSF', 'OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'PoolArea', 'PoolQC', 'Fence', 'MiscFeature', 'MiscVal', 'MoSold', 'YrSold', 'SaleType', 'SaleCondition', 'SalePrice']
- Test column names: ['Id', 'MSSubClass', 'MSZoning', 'LotFrontage', 'LotArea', 'Street', 'Alley', 'LotShape', 'LandContour', 'Utilities', 'LotConfig', 'LandSlope', 'Neighborhood', 'Condition1', 'Condition2', 'BldgType', 'HouseStyle', 'OverallQual', 'OverallCond', 'YearBuilt', 'YearRemodAdd', 'RoofStyle', 'RoofMatl', 'Exterior1st', 'Exterior2nd', 'MasVnrType', 'MasVnrArea', 'ExterQual', 'ExterCond', 'Foundation', 'BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinSF1', 'BsmtFinType2', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF', 'Heating', 'HeatingQC', 'CentralAir', 'Electrical', '1stFlrSF', '2ndFlrSF', 'LowQualFinSF', 'GrLivArea', 'BsmtFullBath', 'BsmtHalfBath', 'FullBath', 'HalfBath', 'BedroomAbvGr', 'KitchenAbvGr', 'KitchenQual', 'TotRmsAbvGrd', 'Functional', 'Fireplaces', 'FireplaceQu', 'GarageType', 'GarageYrBlt', 'GarageFinish', 'GarageCars', 'GarageArea', 'GarageQual', 'GarageCond', 'PavedDrive', 'WoodDeckSF', 'OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'PoolArea', 'PoolQC', 'Fence', 'MiscFeature', 'MiscVal', 'MoSold', 'YrSold', 'SaleType', 'SaleCondition']
- Train data types: {'Id': 'int64', 'MSSubClass': 'int64', 'MSZoning': 'object', 'LotFrontage': 'float64', 'LotArea': 'int64', 'Street': 'object', 'Alley': 'object', 'LotShape': 'object', 'LandContour': 'object', 'Utilities': 'object', 'LotConfig': 'object', 'LandSlope': 'object', 'Neighborhood': 'object', 'Condition1': 'object', 'Condition2': 'object', 'BldgType': 'object', 'HouseStyle': 'object', 'OverallQual': 'int64', 'OverallCond': 'int64', 'YearBuilt': 'int64', 'YearRemodAdd': 'int64', 'RoofStyle': 'object', 'RoofMatl': 'object', 'Exterior1st': 'object', 'Exterior2nd': 'object', 'MasVnrType': 'object', 'MasVnrArea': 'float64', 'ExterQual': 'object', 'ExterCond': 'object', 'Foundation': 'object', 'BsmtQual': 'object', 'BsmtCond': 'object', 'BsmtExposure': 'object', 'BsmtFinType1': 'object', 'BsmtFinSF1': 'int64', 'BsmtFinType2': 'object', 'BsmtFinSF2': 'int64', 'BsmtUnfSF': 'int64', 'TotalBsmtSF': 'int64', 'Heating': 'object', 'HeatingQC': 'object', 'CentralAir': 'object', 'Electrical': 'object', '1stFlrSF': 'int64', '2ndFlrSF': 'int64', 'LowQualFinSF': 'int64', 'GrLivArea': 'int64', 'BsmtFullBath': 'int64', 'BsmtHalfBath': 'int64', 'FullBath': 'int64', 'HalfBath': 'int64', 'BedroomAbvGr': 'int64', 'KitchenAbvGr': 'int64', 'KitchenQual': 'object', 'TotRmsAbvGrd': 'int64', 'Functional': 'object', 'Fireplaces': 'int64', 'FireplaceQu': 'object', 'GarageType': 'object', 'GarageYrBlt': 'float64', 'GarageFinish': 'object', 'GarageCars': 'int64', 'GarageArea': 'int64', 'GarageQual': 'object', 'GarageCond': 'object', 'PavedDrive': 'object', 'WoodDeckSF': 'int64', 'OpenPorchSF': 'int64', 'EnclosedPorch': 'int64', '3SsnPorch': 'int64', 'ScreenPorch': 'int64', 'PoolArea': 'int64', 'PoolQC': 'object', 'Fence': 'object', 'MiscFeature': 'object', 'MiscVal': 'int64', 'MoSold': 'int64', 'YrSold': 'int64', 'SaleType': 'object', 'SaleCondition': 'object', 'SalePrice': 'int64'}
- Test data types: {'Id': 'int64', 'MSSubClass': 'int64', 'MSZoning': 'object', 'LotFrontage': 'float64', 'LotArea': 'int64', 'Street': 'object', 'Alley': 'object', 'LotShape': 'object', 'LandContour': 'object', 'Utilities': 'object', 'LotConfig': 'object', 'LandSlope': 'object', 'Neighborhood': 'object', 'Condition1': 'object', 'Condition2': 'object', 'BldgType': 'object', 'HouseStyle': 'object', 'OverallQual': 'int64', 'OverallCond': 'int64', 'YearBuilt': 'int64', 'YearRemodAdd': 'int64', 'RoofStyle': 'object', 'RoofMatl': 'object', 'Exterior1st': 'object', 'Exterior2nd': 'object', 'MasVnrType': 'object', 'MasVnrArea': 'float64', 'ExterQual': 'object', 'ExterCond': 'object', 'Foundation': 'object', 'BsmtQual': 'object', 'BsmtCond': 'object', 'BsmtExposure': 'object', 'BsmtFinType1': 'object', 'BsmtFinSF1': 'float64', 'BsmtFinType2': 'object', 'BsmtFinSF2': 'float64', 'BsmtUnfSF': 'float64', 'TotalBsmtSF': 'float64', 'Heating': 'object', 'HeatingQC': 'object', 'CentralAir': 'object', 'Electrical': 'object', '1stFlrSF': 'int64', '2ndFlrSF': 'int64', 'LowQualFinSF': 'int64', 'GrLivArea': 'int64', 'BsmtFullBath': 'float64', 'BsmtHalfBath': 'float64', 'FullBath': 'int64', 'HalfBath': 'int64', 'BedroomAbvGr': 'int64', 'KitchenAbvGr': 'int64', 'KitchenQual': 'object', 'TotRmsAbvGrd': 'int64', 'Functional': 'object', 'Fireplaces': 'int64', 'FireplaceQu': 'object', 'GarageType': 'object', 'GarageYrBlt': 'float64', 'GarageFinish': 'object', 'GarageCars': 'float64', 'GarageArea': 'float64', 'GarageQual': 'object', 'GarageCond': 'object', 'PavedDrive': 'object', 'WoodDeckSF': 'int64', 'OpenPorchSF': 'int64', 'EnclosedPorch': 'int64', '3SsnPorch': 'int64', 'ScreenPorch': 'int64', 'PoolArea': 'int64', 'PoolQC': 'object', 'Fence': 'object', 'MiscFeature': 'object', 'MiscVal': 'int64', 'MoSold': 'int64', 'YrSold': 'int64', 'SaleType': 'object', 'SaleCondition': 'object'}
- Train duplicate rows: 0
- Test duplicate rows: 0
- Train duplicate IDs: 0
- Test duplicate IDs: 0
- Target column present in train: True
- Target column absent from test: True
- Row count before preprocessing: train=1460, test=1459
- Row count after preprocessing: train=1460, test=1459
- Numeric source columns after derivation: 62
- Categorical source columns after derivation: 31
- Encoded final feature count: 224
- Final train feature shape: (1460, 224)
- Final test feature shape: (1459, 224)

## Schema and Output Checks
- PASS: schema columns, target placement, ID presence, duplicate IDs, dtype compatibility, and duplicate-column checks.
- PASS: train/test feature columns align (224 features).
- PASS: no SalePrice or Id in feature matrix.
- PASS: no missing values in final feature matrices.
- PASS: no infinite values in final feature matrices.
- PASS: all final feature columns are numeric.
- PASS: row counts are preserved.
- PASS: target preserved with 1460 rows.

## Skew and Outlier Handling
- `GrLivArea` capped at training 0.995 quantile (3431.66) and reused for future data.
- `LotArea` capped at training 0.995 quantile (53422.28) and reused for future data.
- `Log1p_GrLivArea` created to handle right skew in `GrLivArea`.
- `Log1p_LotArea` created to handle right skew in `LotArea`.
- High `GrLivArea` records are retained but capped using the training-only quantile, plus a log feature is exported.
- Garage year values after sale year or before 1800 are treated as missing before age calculation.

## Year and Derived Feature Range Checks
- Age features are computed from `YrSold`, never the current calendar year.
- Negative age values are clipped to zero after suspicious garage years are set missing.
- Area, bathroom, and binary flag derived features are validated by final numeric, missing, infinite, and row-count checks.
