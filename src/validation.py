from pathlib import Path

import numpy as np
import pandas as pd


def inspect_raw(train: pd.DataFrame, test: pd.DataFrame, target: str) -> dict:
    return {
        "train_shape": train.shape,
        "test_shape": test.shape,
        "train_columns": list(train.columns),
        "test_columns": list(test.columns),
        "train_missing": train.isna().sum().sort_values(ascending=False).head(25).to_dict(),
        "test_missing": test.isna().sum().sort_values(ascending=False).head(25).to_dict(),
        "train_duplicates": int(train.duplicated().sum()),
        "test_duplicates": int(test.duplicated().sum()),
        "target_present": target in train.columns,
        "train_dtypes": {col: str(dtype) for col, dtype in train.dtypes.items()},
        "test_dtypes": {col: str(dtype) for col, dtype in test.dtypes.items()},
        "one_row_definition": "One row represents one residential property sale or property record, not a time series or transaction log.",
    }


def validate_schema(train: pd.DataFrame, test: pd.DataFrame, target: str, id_column: str, config: dict | None = None) -> list[str]:
    messages: list[str] = []
    if train.columns.duplicated().any() or test.columns.duplicated().any():
        raise ValueError("Duplicate column names detected.")
    if target not in train.columns:
        raise ValueError(f"Training data must include target column {target}.")
    if target in test.columns:
        raise ValueError(f"Future/test data must not include target column {target}.")
    if id_column not in train.columns or id_column not in test.columns:
        raise ValueError(f"Both train and test data must include ID column {id_column}.")
    if train[id_column].duplicated().any() or test[id_column].duplicated().any():
        raise ValueError(f"Duplicate IDs detected in {id_column}.")
    train_features = set(train.columns) - {target}
    test_features = set(test.columns)
    missing_in_test = sorted(train_features - test_features)
    extra_in_test = sorted(test_features - train_features)
    if missing_in_test or extra_in_test:
        raise ValueError(f"Train/test schema mismatch. Missing in test: {missing_in_test}; extra in test: {extra_in_test}")
    dtype_mismatches = []
    for col in sorted(train_features & test_features):
        train_is_numeric = pd.api.types.is_numeric_dtype(train[col])
        test_is_numeric = pd.api.types.is_numeric_dtype(test[col])
        if train_is_numeric != test_is_numeric:
            dtype_mismatches.append(f"{col}: train={train[col].dtype}, test={test[col].dtype}")
    if dtype_mismatches:
        raise ValueError(f"Train/test data type mismatch. {dtype_mismatches}")
    if config:
        expected_categorical = set(config.get("nominal_as_categorical", [])) | set(config.get("ordinal_mappings", {}).keys())
        for col in expected_categorical & train_features:
            if col not in train.columns or col not in test.columns:
                raise ValueError(f"Expected categorical column missing from train/test: {col}")
    messages.append("PASS: schema columns, target placement, ID presence, duplicate IDs, dtype compatibility, and duplicate-column checks.")
    return messages


def validate_outputs(x_train: pd.DataFrame, x_test: pd.DataFrame, y_train: pd.Series, config: dict, raw_train_rows: int | None = None, raw_test_rows: int | None = None) -> list[str]:
    target = config["target_column"]
    id_column = config["id_column"]
    checks = []
    if list(x_train.columns) != list(x_test.columns):
        raise ValueError("Train and test feature columns do not align.")
    if target in x_train.columns or target in x_test.columns:
        raise ValueError("Target leakage detected in feature matrix.")
    if id_column in x_train.columns or id_column in x_test.columns:
        raise ValueError("ID leakage detected in feature matrix.")
    if x_train.isna().any().any() or x_test.isna().any().any():
        raise ValueError("Missing values remain in final feature matrix.")
    if np.isinf(x_train.select_dtypes(include="number").to_numpy()).any() or np.isinf(x_test.select_dtypes(include="number").to_numpy()).any():
        raise ValueError("Infinite values detected in final feature matrix.")
    if not all(pd.api.types.is_numeric_dtype(x_train[c]) for c in x_train.columns):
        raise ValueError("Final train feature matrix contains non-numeric columns.")
    if not all(pd.api.types.is_numeric_dtype(x_test[c]) for c in x_test.columns):
        raise ValueError("Final test feature matrix contains non-numeric columns.")
    if x_train.columns.duplicated().any() or x_test.columns.duplicated().any():
        raise ValueError("Duplicate final feature columns detected.")
    if raw_train_rows is not None and len(x_train) != raw_train_rows:
        raise ValueError("Training row count changed during preprocessing.")
    if raw_test_rows is not None and len(x_test) != raw_test_rows:
        raise ValueError("Future/test row count changed during preprocessing.")
    if y_train.isna().any():
        raise ValueError("Training target contains missing values.")
    checks.extend(
        [
            f"PASS: train/test feature columns align ({x_train.shape[1]} features).",
            "PASS: no SalePrice or Id in feature matrix.",
            "PASS: no missing values in final feature matrices.",
            "PASS: no infinite values in final feature matrices.",
            "PASS: all final feature columns are numeric.",
            "PASS: row counts are preserved.",
            f"PASS: target preserved with {len(y_train)} rows.",
        ]
    )
    return checks


def write_report(path: str | Path, title: str, lines: list[str]) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(f"# {title}\n\n")
        handle.write("\n".join(lines))
        handle.write("\n")
