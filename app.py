from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS


#  MongoDB Configuration
MONGO_URI = "mongodb+srv://Femi:password_123@ecowheelsdublin.zpsyu.mongodb.net"
DB_NAME = "carrental"

#  Initialize MongoDB Connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
reviews_collection = db["reviews"]

#  Initialize Flask App
app = Flask(__name__)
CORS(app)

#  Route to fetch all reviews
@app.route("/api/reviews", methods=["GET"])
def get_reviews():
    try:
        reviews = list(reviews_collection.find({}, {"_id": 0}))  # Fetch all reviews without the MongoDB _id field
        return jsonify(reviews), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#  Route to submit a new review
@app.route("/api/reviews", methods=["POST"])
def add_review():
    try:
        data = request.get_json()
        name = data.get("name")
        vehicle = data.get("vehicle")
        rating = data.get("rating")
        comment = data.get("comment")

        if not name or not vehicle or not rating or not comment:
            return jsonify({"error": "All fields are required"}), 400

        new_review = {
            "name": name,
            "vehicle": vehicle,
            "rating": int(rating),
            "comment": comment
        }

        reviews_collection.insert_one(new_review)
        return jsonify({"message": "Review added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#  Run the Flask server
if __name__ == "__main__":
    app.run(debug=True, port=5000)

