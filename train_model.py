
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib


df = pd.read_csv("dataset.csv")


df = df.drop(columns=['Country', 'predicted_risk', 'confidence'])


le = LabelEncoder()
df['risk_label'] = le.fit_transform(df['risk_label'])


X = df.drop('risk_label', axis=1)
y = df['risk_label']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)


model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)


joblib.dump(model, "hunger_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(le, "label_encoder.pkl")

print("✅ All files saved successfully!")