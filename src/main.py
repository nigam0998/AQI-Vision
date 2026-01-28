from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
import os
import json

app = FastAPI(title="Real-Time AQI Prediction Service")

# Mount Static Files
static_path = os.path.join(os.path.dirname(__file__), 'static')
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Templates Configuration
templates_path = os.path.join(os.path.dirname(__file__), 'templates')
templates = Jinja2Templates(directory=templates_path)

# Load Model
model_path = os.path.join(os.path.dirname(__file__), '..', 'aqi_pipeline_v1.pkl')
model = joblib.load(model_path)

# Load Dataset (with fallback)
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'AQI-and-Lat-Long-of-Countries.csv')

try:
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    else:
        fallback_path = os.path.join(os.path.dirname(__file__), '..', 'AQI-and-Lat-Long-of-Countries.csv')
        if os.path.exists(fallback_path):
            df = pd.read_csv(fallback_path)
            df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
        else:
             print(f"Warning: Data file not found. Using mock data.")
             raise FileNotFoundError
except Exception:
    print("Initializing with mock data...")
    df = pd.DataFrame({
        'country': ['Mock Country'] * 100,
        'city': ['Mock City'] * 100,
        'aqi_value': np.random.randint(20, 350, 100),
        'co_aqi_value': np.random.randint(1, 10, 100),
        'ozone_aqi_value': np.random.randint(20, 100, 100),
        'no2_aqi_value': np.random.randint(0, 50, 100),
        'pm2.5_aqi_value': np.random.randint(10, 200, 100),
        'lat': np.random.uniform(-50, 50, 100),
        'lng': np.random.uniform(-180, 180, 100)
    })
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]

class AirQualityMetrics(BaseModel):
    co_aqi: float
    ozone_aqi: float
    no2_aqi: float
    pm25_aqi: float

def get_aqi_category(aqi: float) -> dict:
    if aqi <= 50:
        return {"category": "Good", "color": "#00e400", "message": "Air quality is satisfactory."}
    elif aqi <= 100:
        return {"category": "Moderate", "color": "#ffff00", "message": "Air quality is acceptable."}
    elif aqi <= 150:
        return {"category": "Sensitive Groups", "color": "#ff7e00", "message": "Sensitive groups may experience health effects."}
    elif aqi <= 200:
        return {"category": "Unhealthy", "color": "#ff0000", "message": "Everyone may begin to experience health effects."}
    elif aqi <= 300:
        return {"category": "Very Unhealthy", "color": "#8f3f97", "message": "Health alert: serious health effects."}
    else:
        return {"category": "Hazardous", "color": "#7e0023", "message": "Health warning: emergency conditions."}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Stats
    total_records = len(df)
    avg_aqi = round(df['aqi_value'].mean(), 1)
    min_aqi = int(df['aqi_value'].min())
    max_aqi = int(df['aqi_value'].max())
    
    # Map Data
    map_sample = df.sample(min(500, len(df)))
    map_data = [{"lat": row['lat'], "lng": row['lng'], "aqi": row['aqi_value']} 
                for _, row in map_sample.iterrows()]
    
    # Chart Data
    chart_data = [
        len(df[df['aqi_value'] <= 50]),
        len(df[(df['aqi_value'] > 50) & (df['aqi_value'] <= 100)]),
        len(df[(df['aqi_value'] > 100) & (df['aqi_value'] <= 150)]),
        len(df[(df['aqi_value'] > 150) & (df['aqi_value'] <= 200)]),
        len(df[(df['aqi_value'] > 200) & (df['aqi_value'] <= 300)]),
        len(df[df['aqi_value'] > 300])
    ]
    
    context = {
        "request": request,
        "total_records": f"{total_records:,}",
        "avg_aqi": avg_aqi,
        "min_aqi": min_aqi,
        "max_aqi": max_aqi,
        "map_data": json.dumps(map_data),
        "chart_data": json.dumps(chart_data)
    }
    
    return templates.TemplateResponse("index.html", context)

@app.post("/predict")
def predict_aqi(metrics: AirQualityMetrics):
    input_data = pd.DataFrame([{
        'co_aqi_value': metrics.co_aqi,
        'ozone_aqi_value': metrics.ozone_aqi,
        'no2_aqi_value': metrics.no2_aqi,
        'pm2.5_aqi_value': metrics.pm25_aqi
    }])
    
    prediction = model.predict(input_data)
    aqi_value = float(prediction[0])
    aqi_info = get_aqi_category(aqi_value)
    
    return {
        "predicted_aqi": aqi_value,
        "category": aqi_info["category"],
        "color": aqi_info["color"],
        "message": aqi_info["message"],
        "status": "success"
    }
