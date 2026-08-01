# Feature Dictionary

| Feature or group | Source | Type | Transformation | Missing handling | Meaning / caveat |
|---|---|---|---|---|---|
| Numeric feature columns | Original numeric columns plus documented derived numeric columns | Raw/derived numeric | Median imputation, capped/log variants for selected skewed fields, standard scaling | Median from training data only | Property size, age, quality, count, and amenity measures |
| Ordinal quality columns | Quality/condition fields | Encoded ordinal | Domain order from Ames documentation | `NA` maps to 0 where absence is meaningful | Ordered material or facility quality |
| One-hot categorical groups | Nominal categorical columns including `MSSubClass` | Encoded nominal | Rare categories grouped on training data; one-hot with unknown ignored | Structural missing values use `NA`; ordinary missing imputed | Unordered property categories; `MSSubClass` is not treated as continuous |
| Derived age features | `YrSold`, build/remodel/garage year columns | Derived numeric | Sale-year minus event year; impossible garage years set missing | Numeric imputation after derivation | Age at sale, never current-year age |
| Derived amenity flags | Garage, basement, fireplace, pool source fields | Derived indicator | Presence converted to 0/1 | Missing area/count treated as absent for flag only | Availability of major property amenities |
| `SaleSeason` group | `MoSold` | Derived categorical | Month bucketed into season then one-hot encoded | Imputed if missing | Sale timing; assumes prediction point includes sale timing fields |

Final encoded feature count: 224
