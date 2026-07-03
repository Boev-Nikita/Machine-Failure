from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import pandas as pd
import numpy as np
import joblib
import uvicorn
import io
from sklearn.base import BaseEstimator, TransformerMixin

# 0. ОБЯЗАТЕЛЬНО: Класс-генератор (и хак для Jupyter)
class FeatureGenerator(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        X = X.copy()
        X['HDF_temp'] = X['Process temperature [K]'] - X['Air temperature [K]']
        X['AT_cat'] = np.where(X['Air temperature [K]'] < 301.6, 0, 1)
        X['HDF_cat'] = np.where((X['HDF_temp'] < 8.7) & (X['Rotational speed [rpm]'] < 1380), 0, 1)
        X['OSF_n'] = X['Torque [Nm]'] * X['Tool wear [min]']
        X['OSF_cat'] = np.where(X['OSF_n'] < 11000.0, 0, 1)
        X['PWF_n'] = X['Torque [Nm]'] * X['Rotational speed [rpm]'] / 60
        X['PWF_cat'] = np.where((X['PWF_n'] > 885.5) & (X['PWF_n'] < 1112.3), 0, 1)
        return X

import sys
sys.modules['__main__'] = sys.modules[__name__]

app = FastAPI(title="Machine Failure API (CSV & JSON)")
MODEL_PATH = r"C:\projects\machine_failure\MF_model5.pkl"
model = joblib.load(MODEL_PATH)

# --- 1. СТАРЫЙ ЭНДПОИНТ ДЛЯ ОДИНОЧНОГО JSON (оставляем на всякий случай) ---
class MachineDataInput(BaseModel):
    Type: str = Field(..., alias="Air temperature [K]")
    # ... (оставляю его, чтобы не усложнять, он работает как раньше)
    pass 

# --- 2. НОВЫЙ ЭНДПОИНТ ДЛЯ CSV ФАЙЛОВ ---
@app.post("/predict_csv")
async def predict_csv_file(file: UploadFile = File(..., description="Загрузите CSV файл с данными оборудования")):
    # 1. Читаем загруженный файл прямо в Pandas DataFrame
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    
    # 2. Делаем предсказания для ВСЕХ строк разом (очень быстро)
    preds = model.predict(df)
    probs = model.predict_proba(df)
    
    # 3. Приклеиваем новые колонки к исходному датафрейму
    df['Prediction_Code'] = preds
    df['Prediction_Label'] = np.where(preds == 0, 'Норма', 'Отказ')
    df['Probability_Normal'] = probs[:, 0].round(4)
    df['Probability_Failure'] = probs[:, 1].round(4)
    
    # 4. Конвертируем обратно в JSON формат, чтобы браузер мог это отобразить
    result = df.to_dict(orient="records")
    
    return JSONResponse(content=result)