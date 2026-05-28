from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app)

@app.route('/usdmxn')
def get_price():
    try:
        ticker = yf.Ticker("USDMXN=X")
        data = ticker.history(period="2d", interval="1m")
        if data.empty:
            return jsonify({"error": "Sin datos"}), 500
        price = round(float(data['Close'].iloc[-1]), 4)
        prev_close = round(float(data['Close'].iloc[-2]), 4)
        change_pct = round(((price - prev_close) / prev_close) * 100, 2)
        return jsonify({
            "price": price,
            "prev_close": prev_close,
            "change_pct": change_pct,
            "is_up": change_pct >= 0
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/usdmxn/history')
def get_history():
    try:
        ticker = yf.Ticker("USDMXN=X")
        data = ticker.history(period="7d", interval="1d")
        if data.empty:
            return jsonify({"error": "Sin datos"}), 500
        result = []
        for date, row in data.iterrows():
            result.append({
                "date": date.strftime("%d %b"),
                "close": round(float(row['Close']), 4)
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
