import os

from flask import Flask, render_template, request, jsonify
from twitter_scraper import TwitterTrendsScraper


app = Flask(__name__)

@app.route('/')
def index():
    print("Flask server started... :)")
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    scraper = TwitterTrendsScraper(username, password)
    try:
        result = scraper.scrape_trends()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
