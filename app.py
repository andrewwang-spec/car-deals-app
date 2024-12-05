from flask import Flask, render_template, request, jsonify
import requests
from config import API_KEY, BASE_URL

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")  # Home page for user inputs


@app.route("/search", methods=["GET"])
def search_year_make_model_trim():
    # Get query parameters from the user
    year = request.args.get("year")
    make = request.args.get("make")
    model = request.args.get("model")
    trim = request.args.get("trim")
    # zip_code = request.args.get("zip", "10001")  # Default to NYC
    # radius = request.args.get("radius", "50")  # Default to 50 miles
    if not all([year, make, model, trim]):
        return (
            jsonify({"error": "Missing required parameters"}),
            400,
        )  # Return 400 Bad Request
    # Build API request
    url = BASE_URL
    params = {
        "api_key": API_KEY,
        "year": year,
        "make": make,
        "model": model,
        "trim": trim,
    }

    # Call MarketCheck API
    response = requests.get(url, params=params)

    # Log request and response for debugging
    print("Request URL:", response.url)
    print("Response Status Code:", response.status_code)
    print("Response Body:", response.text)

    if response.status_code == 200:
        data = response.json()
        if data.get("num_found", 0) == 0:
            return jsonify({"message": "No listings found for the given parameters"})
        return jsonify(data)
    else:
        return (
            jsonify({"error": "Failed to fetch data", "details": response.text}),
            response.status_code,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)