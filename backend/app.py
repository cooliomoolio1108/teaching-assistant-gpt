from flask import Flask, jsonify, request
from database import get_feedback, check_connection, get_feedback_details, submit_feedback  # Import database functions
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/status", methods=["GET"])
def status():
    return jsonify(check_connection())

@app.route("/get_feedback", methods=["GET"])
def fetch_feedback():
    feedback_data = get_feedback()  # Fetch from MongoDB
    return jsonify(feedback_data)

@app.route("/get_feedback_details", methods=["GET"])
def fetch_feedback_details():
    feedback_details = get_feedback_details()
    return jsonify(feedback_details)

@app.route("/submit_feedback", methods=["POST"])
def receive_feedback():
    data = request.json
    stars = data.get("stars")
    comments = data.get("comments")

    # ADD VALIDATION HEREE
    #
    #
    #

    feedback_data = {
        "comments": comments,
        "stars": stars
    }

    result = submit_feedback(feedback_data)
    
    return jsonify({"message": "Feedback submitted", "feedbackId": str(result.inserted_id)})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
