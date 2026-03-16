
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import load_model
import datetime as dt
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
import os
import plotly.graph_objs as go
from plotly.offline import plot

# --------------------------------------------
# Flask & SQLAlchemy Setup
# --------------------------------------------
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# --------------------------------------------
# User Model
# --------------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=dt.datetime.utcnow)


# --------------------------------------------
# Load Trained Model
# --------------------------------------------
model = load_model("stock_dl_model_new.keras")
plt.style.use("fivethirtyeight")

# --------------------------------------------
# Routes: Register / Login / Logout
# --------------------------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user'] = user.username
            return redirect(url_for('index'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully.')
    return redirect(url_for('login'))
@app.route('/feedback', methods=['POST'])
def feedback():
    if 'user' not in session:
        return redirect(url_for('login'))
    message = request.form.get('feedback')
    if message:
        entry = Feedback(user=session['user'], message=message)
        db.session.add(entry)
        db.session.commit()
        flash("✅ Thank you for your feedback!")
    return redirect(url_for('index'))


# --------------------------------------------
# Main Stock Prediction Route (Protected)
# --------------------------------------------

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user' not in session:
        return redirect(url_for('login'))

    stock_name = None
    sector = None
    website = "#"
    ceo = "N/A"
    country = "N/A"
    market_cap = 0
    ipo_date = "N/A"

    if request.method == 'POST':
        stock = request.form.get('stock') or 'POWERGRID.NS'
        import datetime as dt
        today = dt.datetime.today()
        start = dt.datetime(2023, 1, 1) 
        end = today



        df = yf.download(stock, start=start, end=end)

        if df.empty or 'Close' not in df.columns:
            return render_template('index.html', error=f"No data found for {stock}")

        # Company Info
        try:
            stock_info = yf.Ticker(stock).info
            stock_name = stock_info.get("longName", "N/A")
            sector = stock_info.get("sector", "N/A")
            website = stock_info.get("website", "#")
            ceo = stock_info.get("companyOfficers", [{}])[0].get("name", "N/A")
            country = stock_info.get("country", "N/A")
            market_cap = stock_info.get("marketCap", 0)
            ipo_date = stock_info.get("ipoDate", "N/A")
        except Exception as e:
            print("Error fetching company info:", e)

        # EMAs
        ema20 = df.Close.ewm(span=20).mean()
        ema50 = df.Close.ewm(span=50).mean()
        ema100 = df.Close.ewm(span=100).mean()
        ema200 = df.Close.ewm(span=200).mean()
        data_desc = df.describe()

        # Scaling and Prediction
        data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
        data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70):])
        scaler = MinMaxScaler(feature_range=(0, 1))
        data_training_array = scaler.fit_transform(data_training)
        past_100_days = data_training.tail(100)
        final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
        input_data = scaler.fit_transform(final_df)
        x_test, y_test = [], []
        for i in range(100, input_data.shape[0]):
            x_test.append(input_data[i - 100:i])
            y_test.append(input_data[i, 0])
        x_test, y_test = np.array(x_test), np.array(y_test)
        y_predicted = model.predict(x_test)
        scale_factor = 1 / scaler.scale_[0]
        y_predicted *= scale_factor
        y_test *= scale_factor

        # Charts
        fig1, ax1 = plt.subplots(figsize=(12, 6))
        ax1.plot(df.Close, 'y', label='Closing Price')
        ax1.plot(ema20, 'g', label='EMA 20')
        ax1.plot(ema50, 'r', label='EMA 50')
        ax1.set_title("Closing Price vs Time (20 & 50 Days EMA)")
        ax1.legend()
        ema_chart_path = "static/ema_20_50.png"
        fig1.savefig(ema_chart_path)
        plt.close(fig1)

        fig2, ax2 = plt.subplots(figsize=(12, 6))
        ax2.plot(df.Close, 'y', label='Closing Price')
        ax2.plot(ema100, 'g', label='EMA 100')
        ax2.plot(ema200, 'r', label='EMA 200')
        ax2.set_title("Closing Price vs Time (100 & 200 Days EMA)")
        ax2.legend()
        ema_chart_path_100_200 = "static/ema_100_200.png"
        fig2.savefig(ema_chart_path_100_200)
        plt.close(fig2)

        fig3, ax3 = plt.subplots(figsize=(12, 6))
        ax3.plot(y_test, 'g', label="Original Price", linewidth=1)
        ax3.plot(y_predicted, 'r', label="Predicted Price", linewidth=1)
        ax3.set_title("Prediction vs Original Trend")
        ax3.legend()
        prediction_chart_path = "static/stock_prediction.png"
        fig3.savefig(prediction_chart_path)
        plt.close(fig3)

        fig_vol, ax_vol = plt.subplots(figsize=(12, 4))
        ax_vol.plot(df.index, df['Volume'], color='purple')
        ax_vol.set_title('📦 Volume Traded Over Time')
        volume_chart_path = "static/volume_chart.png"
        fig_vol.savefig(volume_chart_path)
        plt.close(fig_vol)

        exp1 = df.Close.ewm(span=12, adjust=False).mean()
        exp2 = df.Close.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        fig_macd, ax_macd = plt.subplots(figsize=(12, 4))
        ax_macd.plot(macd, label='MACD', color='blue')
        ax_macd.plot(signal, label='Signal Line', color='red')
        fig_macd.savefig("static/macd_chart.png")
        plt.close(fig_macd)

        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        fig_rsi, ax_rsi = plt.subplots(figsize=(12, 4))
        ax_rsi.plot(rsi, color='orange')
        ax_rsi.axhline(70, linestyle='--', color='red')
        ax_rsi.axhline(30, linestyle='--', color='green')
        rsi_chart_path = "static/rsi_chart.png"
        fig_rsi.savefig(rsi_chart_path)
        plt.close(fig_rsi)



        csv_file_path = f"static/{stock}_dataset.csv"
        df.to_csv(csv_file_path)
        data01=pd.read_csv(csv_file_path)

        fig_candle = go.Figure(data=[go.Candlestick(
            x=data01.index,
            open=data01['Open'],
            high=data01['High'],
            low=data01['Low'],
            close=data01['Close'],
            increasing_line_color='green',
            decreasing_line_color='red'
        )])
        fig_candle.update_layout(
            title='🕯️ Candlestick Chart',
            xaxis_title='Date',
            yaxis_title='Price',
            xaxis_rangeslider_visible=False,
            template='plotly_white',
            height=600
        )
        candlestick_html = plot(fig_candle, output_type='div', include_plotlyjs='cdn')


        return render_template(
            'index.html',
            plot_path_ema_20_50=ema_chart_path,
            plot_path_ema_100_200=ema_chart_path_100_200,
            plot_path_prediction=prediction_chart_path,
            plot_path_volume=volume_chart_path,
            plot_path_MACD="static/macd_chart.png",
            plot_path_rsi=rsi_chart_path,
            candlestick_plot=candlestick_html,
            data_desc=data_desc.to_html(classes='table table-bordered table-striped'),
            dataset_link=csv_file_path,
            stock_name=stock_name,
            sector=sector,
            website=website,
            ceo=ceo,
            country=country,
            market_cap=market_cap,
            ipo_date=ipo_date,
            username=session['user']
        )

    return render_template('index.html', username=session.get('user'))

# File download route
@app.route('/download/<filename>')
def download_file(filename):
    return send_file(f"static/{filename}", as_attachment=True)

# --------------------------------------------
# Run App
# --------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
