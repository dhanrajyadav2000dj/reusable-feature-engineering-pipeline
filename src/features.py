import numpy as np
import pandas as pd


def clean_domain_missing(df: pd.DataFrame, none_columns: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in none_columns:
        if col in out.columns:
            out[col] = out[col].fillna("NA")
    return out


def fix_suspicious_garage_year(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "GarageYrBlt" in out.columns:
        invalid = (out["GarageYrBlt"] < 1800) | (out["GarageYrBlt"] > out.get("YrSold", 9999))
        out.loc[invalid.fillna(False), "GarageYrBlt"] = np.nan
    return out


def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if {"YrSold", "YearBuilt"}.issubset(out.columns):
        out["HouseAgeAtSale"] = (out["YrSold"] - out["YearBuilt"]).clip(lower=0)
    if {"YrSold", "YearRemodAdd"}.issubset(out.columns):
        out["RemodelAgeAtSale"] = (out["YrSold"] - out["YearRemodAdd"]).clip(lower=0)
    if {"YrSold", "GarageYrBlt"}.issubset(out.columns):
        out["GarageAgeAtSale"] = (out["YrSold"] - out["GarageYrBlt"]).clip(lower=0)
    sqft_cols = [c for c in ["TotalBsmtSF", "1stFlrSF", "2ndFlrSF"] if c in out.columns]
    if sqft_cols:
        out["TotalSquareFeet"] = out[sqft_cols].fillna(0).sum(axis=1)
    bath_cols = {"FullBath", "HalfBath", "BsmtFullBath", "BsmtHalfBath"}
    if bath_cols.issubset(out.columns):
        out["TotalBathrooms"] = (
            out["FullBath"].fillna(0)
            + 0.5 * out["HalfBath"].fillna(0)
            + out["BsmtFullBath"].fillna(0)
            + 0.5 * out["BsmtHalfBath"].fillna(0)
        )
    porch_cols = [c for c in ["OpenPorchSF", "EnclosedPorch", "3SsnPorch", "ScreenPorch"] if c in out.columns]
    if porch_cols:
        out["TotalPorchArea"] = out[porch_cols].fillna(0).sum(axis=1)
    if "GarageArea" in out.columns:
        out["HasGarage"] = (out["GarageArea"].fillna(0) > 0).astype(int)
    if "TotalBsmtSF" in out.columns:
        out["HasBasement"] = (out["TotalBsmtSF"].fillna(0) > 0).astype(int)
    if "Fireplaces" in out.columns:
        out["HasFireplace"] = (out["Fireplaces"].fillna(0) > 0).astype(int)
    if "PoolArea" in out.columns:
        out["HasPool"] = (out["PoolArea"].fillna(0) > 0).astype(int)
    if {"OverallQual", "OverallCond"}.issubset(out.columns):
        out["QualityConditionInteraction"] = out["OverallQual"] * out["OverallCond"]
    if "MoSold" in out.columns:
        out["SaleSeason"] = pd.cut(
            out["MoSold"],
            bins=[0, 2, 5, 8, 11, 12],
            labels=["Winter", "Spring", "Summer", "Fall", "Winter"],
            ordered=False,
        ).astype("object")
    return out


def apply_ordinal_mappings(df: pd.DataFrame, mappings: dict[str, dict]) -> pd.DataFrame:
    out = df.copy()
    for col, mapping in mappings.items():
        if col in out.columns:
            out[col] = out[col].fillna("NA").map(mapping).astype(float)
    return out
