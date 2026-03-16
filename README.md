# stock_price_prediction

# 📈 Stock Price Prediction System (LSTM + Flask)

This project is a **Stock Price Prediction Web Application** that uses **Machine Learning (LSTM Deep Learning model)** to predict future stock prices based on historical market data.

The system allows users to **register, login, view stock data, and generate predictions with interactive charts** through a web interface.

It combines **Python, Deep Learning, and Flask Web Development** to create an intelligent financial analysis tool.

---

# 🚀 Features

* 📊 **Stock Price Prediction using LSTM**
* 📉 **Technical Indicators Visualization**

  * EMA (Exponential Moving Average)
  * RSI (Relative Strength Index)
  * MACD Indicator
  * Volume Analysis
* 🔐 **User Authentication System**

  * Login
  * Register
* 📂 **Multiple Stock Datasets**

  * Reliance
  * PowerGrid
  * Tata Motors
  * Tata Steel
  * Apple
  * Tesla
* 🌐 **Interactive Web Interface using Flask**
* 📈 **Graphical Visualization of Predictions**

---

# 🏗️ Project Structure

```id="tree1"
stock_price_prediction
│
├── app.py
├── app13.py
├── Stock Price Prediction.ipynb
├── stock_dl_model_new.keras
│
├── instance
│   └── users.db
│
├── static
│   ├── stock_prediction.png
│   ├── ema_20_50.png
│   ├── ema_100_200.png
│   ├── macd_chart.png
│   ├── rsi_chart.png
│   ├── volume_chart.png
│   └── datasets
│
├── templates
│   ├── index.html
│   ├── login.html
│   └── register.html
│
└── README.md
```

---

# ⚙️ Technologies Used

* **Python**
* **Flask**
* **TensorFlow / Keras**
* **LSTM (Long Short-Term Memory Neural Network)**
* **Pandas**
* **NumPy**
* **Matplotlib**
* **HTML / CSS**

---

# 🧠 Machine Learning Model

The project uses a **Deep Learning LSTM model** for time-series forecasting.

Steps involved:

1. Collect historical stock market data
2. Preprocess data using normalization
3. Train LSTM neural network
4. Predict future stock prices
5. Visualize predictions using charts

The trained model is stored as:

```
stock_dl_model_new.keras
```

---

# 🚀 Installation

## 1️⃣ Clone the Repository

```id="clone1"
git clone https://github.com/yourusername/stock-price-prediction.git
cd stock-price-prediction
```

---

## 2️⃣ Create Virtual Environment

```id="venv1"
python -m venv venv
```

Activate environment

**Windows**

```id="venv2"
venv\Scripts\activate
```

**Linux / Mac**

```id="venv3"
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```id="install1"
pip install -r requirements.txt
```

If requirements file is not available install manually:

```id="install2"
pip install flask tensorflow pandas numpy matplotlib scikit-learn
```

---

## 4️⃣ Run the Application

```id="run1"
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

---

# 📊 Supported Stocks

The system currently supports datasets for:

* Apple (AAPL)
* Tesla (TSLA)
* Reliance
* Tata Motors
* Tata Steel
* PowerGrid

Users can analyze historical data and generate predictions for these stocks.

---

# 🔮 Future Improvements

* Real-time stock data integration (Yahoo Finance API)
* Advanced prediction models
* Portfolio recommendation system
* Interactive dashboards
* Cloud deployment

---

# 👨‍💻 Author

**Sahil Salunke**
Student – Information Technology & Artificial Intelligence

---

# ⭐ Contributing

Contributions are welcome.
Fork the repository and submit a pull request to improve the project.

---

# ⚠️ Disclaimer
This project is for educational and research purposes only.
Stock market predictions may not always be accurate and should not be used as financial advice
This project is for **educational and research purposes only**.
Stock market predictions may not always be accurate and should not be used as financial advice.
