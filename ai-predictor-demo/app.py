from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)
API_ENDPOINT = "https://ai-predictor-api.raise.openstax.org/predict/"


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        response = requests.post(API_ENDPOINT, json=data)
        prediction_data = response.json()

        labels = prediction_data.get("labels", [])
        scores = prediction_data.get("scores", [])

        result = [{"label": label, "score": score} for label, score in zip(labels, scores)]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
