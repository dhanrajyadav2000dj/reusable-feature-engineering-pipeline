from pathlib import Path

import pandas as pd
import pytest

from src.features import add_derived_features
from src.pipeline import run_pipeline
from src.validation import validate_schema


def sample_train_test(runtime_dir):
    cols = {
        "Id": [1, 2, 3, 4],
        "MSSubClass": [60, 20, 60, 70],
        "MSZoning": ["RL", "RL", "RM", "RL"],
        "LotArea": [8450, 9600, 11250, 20000],
        "OverallQual": [7, 6, 7, 5],
        "OverallCond": [5, 8, 5, 5],
        "YearBuilt": [2003, 1976, 2001, 1915],
        "YearRemodAdd": [2003, 1976, 2002, 1970],
        "YrSold": [2008, 2007, 2008, 2006],
        "MoSold": [2, 5, 9, 12],
        "GarageYrBlt": [2003, 1976, 2001, 2207],
        "GarageArea": [548, 460, 608, 0],
        "TotalBsmtSF": [856, 1262, 920, 756],
        "1stFlrSF": [856, 1262, 920, 961],
        "2ndFlrSF": [854, 0, 866, 756],
        "FullBath": [2, 2, 2, 1],
        "HalfBath": [1, 0, 1, 0],
        "BsmtFullBath": [1, 0, 1, 1],
        "BsmtHalfBath": [0, 1, 0, 0],
        "OpenPorchSF": [61, 0, 42, 35],
        "EnclosedPorch": [0, 0, 0, 272],
        "3SsnPorch": [0, 0, 0, 0],
        "ScreenPorch": [0, 0, 0, 0],
        "Fireplaces": [0, 1, 1, 1],
        "PoolArea": [0, 0, 0, 0],
        "ExterQual": ["Gd", "TA", "Gd", "TA"],
        "BsmtQual": ["Gd", "Gd", "Gd", "TA"],
        "GarageType": ["Attchd", "Attchd", "Attchd", None],
        "Neighborhood": ["CollgCr", "Veenker", "CollgCr", "OldTown"],
        "SaleType": ["WD", "WD", "WD", "COD"],
        "SaleCondition": ["Normal", "Normal", "Normal", "Abnorml"],
    }
    train = pd.DataFrame(cols)
    train["SalePrice"] = [208500, 181500, 223500, 140000]
    test = pd.DataFrame(cols).drop(index=[3]).reset_index(drop=True)
    test["Id"] = [101, 102, 103]
    runtime_dir.mkdir(parents=True, exist_ok=True)
    train_path = runtime_dir / "train.csv"
    test_path = runtime_dir / "test.csv"
    train.to_csv(train_path, index=False)
    test.to_csv(test_path, index=False)
    return train_path, test_path


def config_for(runtime_dir, train_path, test_path):
    return {
        "paths": {"train_csv": str(train_path), "test_csv": str(test_path), "processed_dir": str(runtime_dir / "processed"), "reports_dir": str(runtime_dir / "reports")},
        "target_column": "SalePrice",
        "id_column": "Id",
        "excluded_columns": ["Id", "SalePrice"],
        "rare_category_threshold": 0.25,
        "cap_quantiles": {"GrLivArea": 0.995, "LotArea": 0.995},
        "skewed_numeric_features": ["LotArea"],
        "domain_missing_as_none": ["GarageType", "BsmtQual"],
        "ordinal_mappings": {"ExterQual": {"TA": 3, "Gd": 4}, "BsmtQual": {"NA": 0, "TA": 3, "Gd": 4}},
        "nominal_as_categorical": ["MSSubClass", "MSZoning", "Neighborhood", "SaleType", "SaleCondition", "GarageType"],
    }


def test_derived_feature_calculation():
    df = pd.DataFrame({"YrSold": [2008], "YearBuilt": [2003], "YearRemodAdd": [2004], "TotalBsmtSF": [100], "1stFlrSF": [200], "2ndFlrSF": [50]})
    result = add_derived_features(df)
    assert result.loc[0, "HouseAgeAtSale"] == 5
    assert result.loc[0, "RemodelAgeAtSale"] == 4
    assert result.loc[0, "TotalSquareFeet"] == 350


def test_schema_validation_behavior():
    train = pd.DataFrame({"Id": [1], "A": [1], "SalePrice": [10]})
    test = pd.DataFrame({"Id": [2], "B": [1]})
    with pytest.raises(ValueError, match="schema mismatch"):
        validate_schema(train, test, "SalePrice", "Id")


def test_schema_rejects_duplicate_id():
    train = pd.DataFrame({"Id": [1, 1], "A": [1, 2], "SalePrice": [10, 20]})
    test = pd.DataFrame({"Id": [3, 4], "A": [1, 2]})
    with pytest.raises(ValueError, match="Duplicate IDs"):
        validate_schema(train, test, "SalePrice", "Id")


def test_schema_rejects_target_in_future():
    train = pd.DataFrame({"Id": [1], "A": [1], "SalePrice": [10]})
    test = pd.DataFrame({"Id": [2], "A": [1], "SalePrice": [9]})
    with pytest.raises(ValueError, match="must not include target"):
        validate_schema(train, test, "SalePrice", "Id")


def test_schema_rejects_dtype_mismatch():
    train = pd.DataFrame({"Id": [1], "A": [1], "SalePrice": [10]})
    test = pd.DataFrame({"Id": [2], "A": ["one"]})
    with pytest.raises(ValueError, match="data type mismatch"):
        validate_schema(train, test, "SalePrice", "Id")


def test_full_pipeline_alignment_and_no_leakage():
    runtime_dir = Path("test_runtime/full_pipeline")
    train_path, test_path = sample_train_test(runtime_dir)
    config = config_for(runtime_dir, train_path, test_path)
    result = run_pipeline(config)
    assert list(result["x_train"].columns) == list(result["x_test"].columns)
    assert "SalePrice" not in result["x_train"].columns
    assert "Id" not in result["x_train"].columns
    assert "MSSubClass" not in [c for c in result["x_train"].columns if c == "MSSubClass"]
    assert result["x_train"].isna().sum().sum() == 0
    assert result["x_test"].isna().sum().sum() == 0
    assert all(pd.api.types.is_numeric_dtype(result["x_train"][c]) for c in result["x_train"].columns)
    assert len(result["x_train"]) == 4
    assert len(result["x_test"]) == 3
    assert Path(config["paths"]["processed_dir"], "feature_ready_train.csv").exists()
    assert Path(config["paths"]["processed_dir"], "feature_ready_test.csv").exists()
    assert Path(config["paths"]["processed_dir"], "target_train.csv").exists()
    exported_train = pd.read_csv(Path(config["paths"]["processed_dir"], "feature_ready_train.csv"))
    assert "SalePrice" not in exported_train.columns
    assert "Id" not in exported_train.columns


def test_unknown_category_handling():
    runtime_dir = Path("test_runtime/unknown_category")
    train_path, test_path = sample_train_test(runtime_dir)
    test = pd.read_csv(test_path)
    test.loc[0, "Neighborhood"] = "NeverSeen"
    test.to_csv(test_path, index=False)
    result = run_pipeline(config_for(runtime_dir, train_path, test_path))
    assert result["x_test"].shape[1] == result["x_train"].shape[1]

