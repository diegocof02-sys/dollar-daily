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
        open_price = round(float(data['Open'].iloc[0]), 4)
        prev_close = round(float(data['Close'].iloc[-2]), 4)
        change_pct = round(((price - prev_close) / prev_close) * 100, 2)
        
        return jsonify({
            "price": price,
            "open": open_price,
            "prev_close": prev_close,
            "change_pct": change_pct,
            "is_up": change_pct >= 0
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
