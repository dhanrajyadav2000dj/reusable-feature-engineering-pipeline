# Feature Dictionary

| Feature or group | Source | Type | Transformation | Missing handling | Meaning / caveat |
|---|---|---|---|---|---|
| Numeric feature columns | Original numeric columns plus documented derived numeric columns | Raw/derived numeric | Median imputation, capped/log variants for selected skewed fields, standard scaling | Median from training data only | Property size, age, quality, count, and amenity measures |
| Ordinal quality columns | Quality/condition fields | Encoded ordinal | Domain order from Ames documentation | `NA` maps to 0 where absence is meaningful | Ordered material or facility quality |
| One-hot categorical groups | Nominal categorical columns including `MSSubClass` | Encoded nominal | Rare categories grouped on training data; one-hot with unknown ignored | Structural missing values use `NA`; ordinary missing imputed | Unordered property categories; `MSSubClass` is not treated as continuous |
| Derived age features | `YrSold`, build/remodel/garage year columns | Derived numeric | Sale-year minus event year; impossible garage years set missing | Numeric imputation after derivation | Age at sale, never current-year age |
| Derived amenity flags | Garage, basement, fireplace, pool source fields | Derived indicator | Presence converted to 0/1 | Missing area/count treated as absent for flag only | Availability of major property amenities |
| `SaleSeason` group | `MoSold` | Derived categorical | Month bucketed into season then one-hot encoded | Imputed if missing | Sale timing; assumes prediction point includes sale timing fields |
| `HouseAgeAtSale` | `YrSold`, `YearBuilt` | Derived numeric | `YrSold - YearBuilt`, clipped at 0, scaled in final matrix | Median if missing after derivation | Property age at sale; future-available when sale year is known |
| `RemodelAgeAtSale` | `YrSold`, `YearRemodAdd` | Derived numeric | `YrSold - YearRemodAdd`, clipped at 0, scaled in final matrix | Median if missing after derivation | Years since remodel at sale; future-available when sale year is known |
| `GarageAgeAtSale` | `YrSold`, `GarageYrBlt` | Derived numeric | Invalid garage years set missing, then `YrSold - GarageYrBlt`, clipped at 0, scaled | Median if missing after derivation | Garage age at sale; source availability caveat for missing garage year |
| `TotalSquareFeet` | `TotalBsmtSF`, `1stFlrSF`, `2ndFlrSF` | Derived numeric | Sum of available floor-area fields, scaled | Missing source area treated as 0 for sum | Overall finished and basement area |
| `TotalBathrooms` | `FullBath`, `HalfBath`, `BsmtFullBath`, `BsmtHalfBath` | Derived numeric | Full baths plus 0.5 half baths, scaled | Missing source counts treated as 0 for sum | Total bathroom capacity |
| `TotalPorchArea` | `OpenPorchSF`, `EnclosedPorch`, `3SsnPorch`, `ScreenPorch` | Derived numeric | Sum of porch areas, scaled | Missing source area treated as 0 for sum | Outdoor/porch amenity size |

Final encoded feature count: 224
