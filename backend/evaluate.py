from sklearn.metrics import classification_report
import joblib

from backend.train import model, X_test, y_test

probs = model.predict_proba(X_test)[:, 1]
preds = (probs >= 0.35).astype(int)
joblib.dump(model, "../model/rain_model.pkl")

print(classification_report(y_test, preds))
