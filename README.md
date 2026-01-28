# 🌍 AQI Vision PRO - Air Quality Prediction System

![AQI Vision Banner](https://img.shields.io/badge/AQI%20Vision-PRO-00d4ff?style=for-the-badge&logo=leaf&logoColor=white) 
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com) 
[![XGBoost](https://img.shields.io/badge/XGBoost-EB212E?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

> **Advanced real-time Air Quality Index (AQI) prediction and analytics platform powered by Machine Learning.**

---

## 🚀 Features

- **🔮 Precision AI Prediction**: Utilizes a trained `XGBoost` pipeline to predict AQI values based on pollutant data (CO, Ozone, NO2, PM2.5).
- **🎨 Professional UI**: A stunning, responsive "Eco-Cyber" interface featuring glassmorphism, smooth animations, and interactive elements.
- **🗺️ Global Monitoring**: Integrated interactive map visualizing air quality data points across the globe.
- **📊 Real-time Analytics**: Dynamic charts and statistical breakdowns of dataset trends.
- **⚡ High Performance**: Built on **FastAPI** for lightning-fast inference and response times.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.9+, FastAPI, Uvicorn
- **Machine Learning**: XGBoost, Scikit-Learn, Pandas, NumPy
- **Frontend**: HTML5, Jinja2 Templates, Modern CSS3 (Variables, Flexbox/Grid), JavaScript (ES6+)
- **Visualization**: Chart.js, Leaflet.js

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/AQI-Vision-Pro.git
   cd AQI-Vision-Pro
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn src.main:app --reload
   ```

5. **Access the Dashboard**
   Open your browser and navigate to: `http://127.0.0.1:8000`

---

## 🧪 Usage

1. **Input Data**: Enter values for Carbon Monoxide (CO), Ozone, Nitrogen Dioxide (NO2), and Particulate Matter (PM2.5).
2. **Quick Fill**: Use the "Generic Good/Moderate/Bad" buttons to auto-fill sample data for testing.
3. **Analyze**: Click **"Analyze Air Quality"** to get an instant prediction.
4. **Visualize**: View the result card for AQI category, color-coded health warnings, and explore the global map and distribution charts.

---

## 📂 Project Structure

```
AQI-Vision-Pro/
├── data/                   # Dataset storage
├── src/
│   ├── static/             # Assets (CSS, JS, Images)
│   ├── templates/          # Jinja2 HTML Templates
│   ├── main.py             # FastAPI Application Entry
│   └── train.py            # ML Training Script
├── requirements.txt        # Python Dependencies
├── vercel.json             # Vercel Deployment Config
└── README.md               # Documentation
```

---

## 🚀 Deployment

### Vercel (Recommended)
This project is configured for seamless deployment on Vercel.

1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in the project root.
3. Follow the prompts to deploy.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**© 2026 AQI Vision Team** | Powered by *Antigravity*
