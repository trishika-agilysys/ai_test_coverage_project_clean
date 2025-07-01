import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Load the processed test log data
df = pd.read_csv("ai_model/data/history_logs.csv")

# Drop any rows missing critical data
df = df.dropna(subset=["method", "url", "status_code", "latency_ms"])

# Convert categorical features into numeric format
X = pd.get_dummies(df[["method", "url", "latency_bucket"]])

# Target: Whether the test failed
y = df["is_error"]

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train an XGBoost classifier
model = xgb.XGBClassifier(
    objective="binary:logistic", 
    eval_metric="logloss", 
    use_label_encoder=False,
    base_score=0.5
)

model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print("\nClassification Report ")
print(classification_report(y_test, y_pred))

# Predict risk score for all test cases
df["risk_score"] = model.predict_proba(X)[:, 1]

# Save prioritized test cases
df[["method", "url", "risk_score"]].sort_values(by="risk_score", ascending=False).to_json(
    "ai_model/data/prioritized_tests.json", orient="records", indent=2
)

print("\n Model trained and prioritized_tests.json saved")