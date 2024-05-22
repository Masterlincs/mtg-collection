from flask import Flask, request, jsonify, render_template
from main import fetch_and_store_cards  # Make sure this function accepts set_codes and card_nums as arguments
import asyncio


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/fetch_and_store_cards', methods=['POST'])
def fetch_and_store_cards_route():
    data = request.get_json()
    set_codes = data.get('set_codes', [])
    card_nums = data.get('card_nums', [])
    asyncio.run(fetch_and_store_cards(set_codes, card_nums))
    return jsonify({"message": "Cards fetched and stored successfully."})

if __name__ == '__main__':
    app.run(debug=True)