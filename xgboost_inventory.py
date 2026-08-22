import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

# ==========================================
# 1. GENERATE SYNTHETIC ELECTRONICS DATA
# ==========================================
np.random.seed(42)
n_samples = 1000

# Features typical for an electronics inventory
data = {
    "product_category": np.random.choice(
        [0, 1, 2], size=n_samples
    ),  # 0: Laptops, 1: Smartphones, 2: Audio
    "unit_price_usd": np.random.uniform(50, 1500, size=n_samples),
    "discount_percent": np.random.uniform(0, 0.30, size=n_samples),
    "lead_time_days": np.random.randint(2, 21, size=n_samples),
    "historical_lag_7d_sales": np.random.randint(10, 300, size=n_samples),
    "historical_lag_30d_sales": np.random.randint(50, 1200, size=n_samples),
    "is_holiday_season": np.random.choice([0, 1], size=n_samples, p=[0.8, 0.2]),
}

df = pd.DataFrame(data)

# Simulate target variable: Units Demanded (Demand = function of features + noise)
df["units_demanded"] = (
    (df["historical_lag_7d_sales"] * 0.4)
    + (df["historical_lag_30d_sales"] * 0.1)
    + (df["is_holiday_season"] * 80)
    + (df["discount_percent"] * 200)
    - (df["unit_price_usd"] * 0.05)
    + np.random.normal(0, 15, size=n_samples)
).clip(
    lower=0
)  # Ensure non-negative demand

# ==========================================
# 2. TRAIN / TEST SPLIT
# ==========================================
X = df.drop(columns=["units_demanded"])
y = df["units_demanded"]

# For time-ordered inventory, split sequentially or by random split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ==========================================
# 3. BUILD & TRAIN XGBOOST REGRESSOR
# ==========================================
model = xgb.XGBRegressor(
    objective="reg:squarederror",  # Continuous regression objective
    n_estimators=150,  # Number of boosted trees
    learning_rate=0.05,  # Step size shrinkage
    max_depth=5,  # Maximum tree depth
    subsample=0.8,  # Fraction of samples used per tree
    colsample_bytree=0.8,  # Fraction of features used per tree
    reg_alpha=0.1,  # L1 regularization
    reg_lambda=1.0,  # L2 regularization
    random_state=42,
)

model.fit(X_train, y_train)

# ==========================================
# 4. PREDICTIONS & EVALUATION
# ==========================================
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"Mean Absolute Error (MAE): {mae:.2f} units")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f} units")

# ==========================================
# 5. INVENTORY REORDER LEVEL CALCULATION
# ==========================================
# Combine predicted demand with lead times to calculate safety stock & reorder point
sample_item = X_test.iloc[0].copy()
predicted_daily_demand = model.predict(sample_item.to_frame().T)[0]

lead_time = sample_item["lead_time_days"]
safety_stock = 1.65 * np.std(y_test - y_pred)  # ~95% service level buffer
reorder_point = (predicted_daily_demand * lead_time) + safety_stock

print("\n--- Operational Inventory Decision ---")
print(f"Predicted Daily Demand: {predicted_daily_demand:.0f} units")
print(f"Lead Time: {lead_time} days")
print(f"Safety Stock Buffer: {safety_stock:.0f} units")
print(f"Reorder Point: Trigger purchase order when stock <= {reorder_point:.0f} units")