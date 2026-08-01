from pathlib import Path

import numpy as np
import pandas as pd

from src.features import add_derived_features, apply_ordinal_mappings, clean_domain_missing, fix_suspicious_garage_year
from src.validation import inspect_raw, validate_outputs, validate_schema, write_report


class RareCategoryGrouper:
    def __init__(self, threshold: float = 0.01):
        self.threshold = threshold
        self.keep_: dict[str, set] = {}

    def fit(self, x: pd.DataFrame):
        for col in x.columns:
            freq = x[col].fillna("Missing").astype(str).value_counts(normalize=True)
            self.keep_[col] = set(freq[freq >= self.threshold].index)
        return self

    def transform(self, x: pd.DataFrame) -> pd.DataFrame:
        out = x.copy()
        for col, keep in self.keep_.items():
            values = out[col].fillna("Missing").astype(str)
            out[col] = values.where(values.isin(keep), "Rare")
        return out

    def fit_transform(self, x: pd.DataFrame) -> pd.DataFrame:
        return self.fit(x).transform(x)


def _prepare_frame(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    out = df.copy()
    if "MSSubClass" in out.columns:
        out["MSSubClass"] = out["MSSubClass"].astype(str)
    out = clean_domain_missing(out, config.get("domain_missing_as_none", []))
    out = fix_suspicious_garage_year(out)
    out = add_derived_features(out)
    out = apply_ordinal_mappings(out, config.get("ordinal_mappings", {}))
    return out


def _cap_and_log(train: pd.DataFrame, test: pd.DataFrame, config: dict) -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    report = []
    train_out, test_out = train.copy(), test.copy()
    for col, quantile in config.get("cap_quantiles", {}).items():
        if col in train_out.columns:
            cap = train_out[col].quantile(float(quantile))
            train_out[col] = train_out[col].clip(upper=cap)
            test_out[col] = test_out[col].clip(upper=cap)
            report.append(f"- `{col}` capped at training {quantile} quantile ({cap:.2f}) and reused for future data.")
    for col in config.get("skewed_numeric_features", []):
        if col in train_out.columns:
            new_col = f"Log1p_{col}"
            train_out[new_col] = np.log1p(train_out[col].clip(lower=0))
            test_out[new_col] = np.log1p(test_out[col].clip(lower=0))
            report.append(f"- `{new_col}` created to handle right skew in `{col}`.")
    return train_out, test_out, report


def _manual_preprocess(train: pd.DataFrame, test: pd.DataFrame, numeric_cols: list[str], categorical_cols: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    train_num = train[numeric_cols].apply(pd.to_numeric, errors="coerce").copy()
    test_num = test[numeric_cols].apply(pd.to_numeric, errors="coerce").copy()
    medians = train_num.median()
    train_num = train_num.fillna(medians)
    test_num = test_num.fillna(medians)
    means = train_num.mean()
    stds = train_num.std(ddof=0).replace(0, 1)
    train_num = (train_num - means) / stds
    test_num = (test_num - means) / stds

    train_cat = train[categorical_cols].fillna("Missing").astype(str).copy()
    test_cat = test[categorical_cols].fillna("Missing").astype(str).copy()
    encoded_train_parts = [train_num.reset_index(drop=True)]
    encoded_test_parts = [test_num.reset_index(drop=True)]
    for col in categorical_cols:
        categories = sorted(train_cat[col].unique())
        for category in categories:
            safe_category = str(category).replace(" ", "_").replace("/", "_")
            out_col = f"{col}_{safe_category}"
            encoded_train_parts.append((train_cat[col].reset_index(drop=True) == category).astype(int).rename(out_col).to_frame())
            encoded_test_parts.append((test_cat[col].reset_index(drop=True) == category).astype(int).rename(out_col).to_frame())
    return pd.concat(encoded_train_parts, axis=1), pd.concat(encoded_test_parts, axis=1)


def run_pipeline(config: dict) -> dict:
    train = pd.read_csv(config["paths"]["train_csv"])
    test = pd.read_csv(config["paths"]["test_csv"])
    raw_info = inspect_raw(train, test, config["target_column"])
    schema_messages = validate_schema(train, test, config["target_column"], config["id_column"], config)

    y_train = train[config["target_column"]].copy()
    train_features = train.drop(columns=[config["target_column"]])

    train_pre = _prepare_frame(train_features, config)
    test_pre = _prepare_frame(test, config)
    train_pre, test_pre, skew_report = _cap_and_log(train_pre, test_pre, config)

    excluded = set(config.get("excluded_columns", [])) | {config["id_column"], config["target_column"]}
    train_pre = train_pre.drop(columns=[c for c in excluded if c in train_pre.columns])
    test_pre = test_pre.drop(columns=[c for c in excluded if c in test_pre.columns])

    grouper = RareCategoryGrouper(config.get("rare_category_threshold", 0.01))
    categorical_cols = [c for c in train_pre.columns if train_pre[c].dtype == "object" or str(train_pre[c].dtype) == "category"]
    train_pre[categorical_cols] = grouper.fit_transform(train_pre[categorical_cols])
    test_pre[categorical_cols] = grouper.transform(test_pre[categorical_cols])
    numeric_cols = [c for c in train_pre.columns if c not in categorical_cols]

    x_train, x_test = _manual_preprocess(train_pre, test_pre, numeric_cols, categorical_cols)
    x_train.index = train.index
    x_test.index = test.index
    feature_names = list(x_train.columns)

    validation_messages = validate_outputs(x_train, x_test, y_train, config, len(train), len(test))
    processed_dir = Path(config["paths"]["processed_dir"])
    reports_dir = Path(config["paths"]["reports_dir"])
    processed_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    x_train.to_csv(processed_dir / "feature_ready_train.csv", index=False)
    x_test.to_csv(processed_dir / "feature_ready_test.csv", index=False)
    pd.DataFrame({config["target_column"]: y_train}).to_csv(processed_dir / "target_train.csv", index=False)

    report_lines = [
        f"- Raw train shape: {raw_info['train_shape']}",
        f"- Raw test shape: {raw_info['test_shape']}",
        f"- One row definition: {raw_info['one_row_definition']}",
        f"- Top train missing counts: {raw_info['train_missing']}",
        f"- Top test missing counts: {raw_info['test_missing']}",
        f"- Train column names: {raw_info['train_columns']}",
        f"- Test column names: {raw_info['test_columns']}",
        f"- Train data types: {raw_info['train_dtypes']}",
        f"- Test data types: {raw_info['test_dtypes']}",
        f"- Train duplicate rows: {raw_info['train_duplicates']}",
        f"- Test duplicate rows: {raw_info['test_duplicates']}",
        f"- Train duplicate IDs: {int(train[config['id_column']].duplicated().sum())}",
        f"- Test duplicate IDs: {int(test[config['id_column']].duplicated().sum())}",
        f"- Target column present in train: {config['target_column'] in train.columns}",
        f"- Target column absent from test: {config['target_column'] not in test.columns}",
        f"- Row count before preprocessing: train={len(train)}, test={len(test)}",
        f"- Row count after preprocessing: train={len(x_train)}, test={len(x_test)}",
        f"- Numeric source columns after derivation: {len(numeric_cols)}",
        f"- Categorical source columns after derivation: {len(categorical_cols)}",
        f"- Encoded final feature count: {x_train.shape[1]}",
        f"- Final train feature shape: {x_train.shape}",
        f"- Final test feature shape: {x_test.shape}",
        "",
        "## Schema and Output Checks",
        *[f"- {m}" for m in schema_messages + validation_messages],
        "",
        "## Skew and Outlier Handling",
        *skew_report,
        "- High `GrLivArea` records are retained but capped using the training-only quantile, plus a log feature is exported.",
        "- Garage year values after sale year or before 1800 are treated as missing before age calculation.",
        "",
        "## Year and Derived Feature Range Checks",
        "- Age features are computed from `YrSold`, never the current calendar year.",
        "- Negative age values are clipped to zero after suspicious garage years are set missing.",
        "- Area, bathroom, and binary flag derived features are validated by final numeric, missing, infinite, and row-count checks.",
    ]
    write_report(reports_dir / "validation_report.md", "Validation Report", report_lines)
    write_feature_dictionary(reports_dir / "feature_dictionary.md", feature_names, numeric_cols, categorical_cols)
    write_leakage_review(reports_dir / "leakage_review.md")
    return {"x_train": x_train, "x_test": x_test, "y_train": y_train, "feature_names": feature_names}


def write_feature_dictionary(path: Path, feature_names: list[str], numeric_cols: list[str], categorical_cols: list[str]) -> None:
    lines = [
        "| Feature or group | Source | Type | Transformation | Missing handling | Meaning / caveat |",
        "|---|---|---|---|---|---|",
        "| Numeric feature columns | Original numeric columns plus documented derived numeric columns | Raw/derived numeric | Median imputation, capped/log variants for selected skewed fields, standard scaling | Median from training data only | Property size, age, quality, count, and amenity measures |",
        "| Ordinal quality columns | Quality/condition fields | Encoded ordinal | Domain order from Ames documentation | `NA` maps to 0 where absence is meaningful | Ordered material or facility quality |",
        "| One-hot categorical groups | Nominal categorical columns including `MSSubClass` | Encoded nominal | Rare categories grouped on training data; one-hot with unknown ignored | Structural missing values use `NA`; ordinary missing imputed | Unordered property categories; `MSSubClass` is not treated as continuous |",
        "| Derived age features | `YrSold`, build/remodel/garage year columns | Derived numeric | Sale-year minus event year; impossible garage years set missing | Numeric imputation after derivation | Age at sale, never current-year age |",
        "| Derived amenity flags | Garage, basement, fireplace, pool source fields | Derived indicator | Presence converted to 0/1 | Missing area/count treated as absent for flag only | Availability of major property amenities |",
        "| `SaleSeason` group | `MoSold` | Derived categorical | Month bucketed into season then one-hot encoded | Imputed if missing | Sale timing; assumes prediction point includes sale timing fields |",
        "| `HouseAgeAtSale` | `YrSold`, `YearBuilt` | Derived numeric | `YrSold - YearBuilt`, clipped at 0, scaled in final matrix | Median if missing after derivation | Property age at sale; future-available when sale year is known |",
        "| `RemodelAgeAtSale` | `YrSold`, `YearRemodAdd` | Derived numeric | `YrSold - YearRemodAdd`, clipped at 0, scaled in final matrix | Median if missing after derivation | Years since remodel at sale; future-available when sale year is known |",
        "| `GarageAgeAtSale` | `YrSold`, `GarageYrBlt` | Derived numeric | Invalid garage years set missing, then `YrSold - GarageYrBlt`, clipped at 0, scaled | Median if missing after derivation | Garage age at sale; source availability caveat for missing garage year |",
        "| `TotalSquareFeet` | `TotalBsmtSF`, `1stFlrSF`, `2ndFlrSF` | Derived numeric | Sum of available floor-area fields, scaled | Missing source area treated as 0 for sum | Overall finished and basement area |",
        "| `TotalBathrooms` | `FullBath`, `HalfBath`, `BsmtFullBath`, `BsmtHalfBath` | Derived numeric | Full baths plus 0.5 half baths, scaled | Missing source counts treated as 0 for sum | Total bathroom capacity |",
        "| `TotalPorchArea` | `OpenPorchSF`, `EnclosedPorch`, `3SsnPorch`, `ScreenPorch` | Derived numeric | Sum of porch areas, scaled | Missing source area treated as 0 for sum | Outdoor/porch amenity size |",
        "",
        f"Final encoded feature count: {len(feature_names)}",
    ]
    write_report(path, "Feature Dictionary", lines)


def write_leakage_review(path: Path) -> None:
    lines = [
        "- `SalePrice` is separated before preprocessing and never enters the feature matrix.",
        "- `Id` is excluded from all final features.",
        "- Preprocessors are fit on training data only and then applied to future/test data.",
        "- Sale fields such as `SaleType`, `SaleCondition`, `MoSold`, and `YrSold` are included under the assumption that scoring occurs at listing/transaction-preparation time when these values are available. If scoring earlier, move them to `excluded_columns`.",
        "- Age features use `YrSold`, not the current calendar year.",
        "- Derived features use columns present in both train and future/test files.",
        "- High `GrLivArea` is not dropped; it is capped by a training-derived threshold and logged to keep scoring row counts stable.",
    ]
    write_report(path, "Leakage Review", lines)


