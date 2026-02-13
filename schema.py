# schema.py

EXTRACTION_SCHEMA = {
  "datasets": ["Name of dataset 1", "Name of dataset 2"],
  "experiment": [
    {
      "model": "Name of the model (e.g., cSysGuard, LSTM, GRU)",
      "result": {
        "metric_name_1 (e.g., RMSE, Accuracy)": 0.0,
        "metric_name_2 (e.g., MAE, F1)": 0.0
      }
    }
  ]
}