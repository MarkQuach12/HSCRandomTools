import matplotlib.pyplot as plt
import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from controllers.predict_controller import predict_bp
from controllers.band6_controller import band6_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(predict_bp)
app.register_blueprint(band6_bp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)