from flask import Flask, request, jsonify
from redis import Redis
from request_model import NoteModel
from pydantic import ValidationError


app = Flask(__name__)
r = Redis(host="localhost", port=6379, decode_responses=True)

# Allowed expiration times
EXPIRATION_OPTIONS = [5, 10, 20, 30, 60, 120, 240, 360]



@app.route("/")
def home_page():
    return "<h1>Welcome to TakeNote</h1>"

@app.route("/create", methods=["POST"])
def create_note():
    try:
        data = NoteModel(**request.json)  # Here the process of validation takes place to ensure compliant entry
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    r.setex(data.note_name, data.expiration, data.note_value)
    return jsonify({
        "message": f"Note '{data.note_name}' created successfully",
        "expires_in": data.expiration
    })

@app.route("/notes/<name>", methods=["GET"])
def get_note(name):
    value = r.get(name)
    if value is None:
        return jsonify({"error": "Note not found or expired"}), 404
    return jsonify({"note_name": name, "note_value": value})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
