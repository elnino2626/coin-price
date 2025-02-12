from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

ALLOWED_CURRENCIES = {'EUR', 'GBP', 'USD', 'JPY'}

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/<currency>')
def get_spot_price(currency):
    currency = currency.upper()
    if currency not in ALLOWED_CURRENCIES:
        return jsonify({"error": "Currency not supported"}), 400

    try:
        headers = {'User-Agent': 'CoinbaseSpotPriceService/1.0'}
        response = requests.get(
            f'https://api.coinbase.com/v2/prices/spot?currency={currency}',
            headers=headers
        )
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as err:
        return jsonify({"error": str(err)}), 500
    except requests.exceptions.RequestException as err:
        return jsonify({"error": "Failed to connect to Coinbase API"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
