import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, mean_absolute_error

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

# Load drought data
df_drought = pd.read_csv("drought_prediction.csv")

# Feature engineering for drought
df_drought["rainfall_3m"] = df_drought["rainfall_mm"]
df_drought["avg_temp_3m"] = df_drought["avg_temp_c"]
df_drought["resv_pop_ratio"] = df_drought["reservoir_level"] / (df_drought["population"] + 1e-6)
df_drought["consumption_lag1"] = df_drought["past_month_consumption"]

feature_cols = [
    "rainfall_mm", "avg_temp_c", "soil_moisture", "reservoir_level",
    "rainfall_3m", "avg_temp_3m", "resv_pop_ratio", "consumption_lag1", "population"
]

X_drought = df_drought[feature_cols]
y_drought = df_drought["drought_event"]

X_train, X_test, y_train, y_test = train_test_split(X_drought, y_drought, test_size=0.2, random_state=42)

clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)
print("=== Drought Classifier Report ===")
print(classification_report(y_test, clf.predict(X_test)))

joblib.dump({"model": clf, "features": feature_cols}, os.path.join(MODEL_DIR, "drought_clf.joblib"))


# Load water demand/supply data
df_ws = pd.read_csv("water_demand_supply.csv")

df_ws["rainfall_3m"] = df_ws["rainfall_mm"]
df_ws["avg_temp_3m"] = df_ws["avg_temp_c"]
df_ws["resv_pop_ratio"] = df_ws["reservoir_level"] / (df_ws["population"] + 1e-6)
df_ws["consumption_lag1"] = df_ws["past_month_consumption"]

X_ws = df_ws[feature_cols]
y_demand = df_ws["water_demand_m3"]
y_supply = df_ws["water_supply_m3"]

reg_demand = RandomForestRegressor(random_state=42)
reg_demand.fit(X_ws, y_demand)
print("Demand MAE:", mean_absolute_error(y_demand, reg_demand.predict(X_ws)))
joblib.dump({"model": reg_demand, "features": feature_cols}, os.path.join(MODEL_DIR, "demand_reg.joblib"))

reg_supply = RandomForestRegressor(random_state=42)
reg_supply.fit(X_ws, y_supply)
print("Supply MAE:", mean_absolute_error(y_supply, reg_supply.predict(X_ws)))
joblib.dump({"model": reg_supply, "features": feature_cols}, os.path.join(MODEL_DIR, "supply_reg.joblib"))

print(f"✅ Models saved in {MODEL_DIR}/")

