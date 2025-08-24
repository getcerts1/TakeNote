from flask import Flask, request, jsonify

from rate_limit import is_rate_limited
from request_model import NoteModel
from pydantic import ValidationError
from database import r


app = Flask(__name__)


# Allowed expiration times
EXPIRATION_OPTIONS = [5, 10, 20, 30, 60, 120, 240, 360]


"""
@app.route("/")
def home_page():
    return "<h1>Welcome to TakeNote</h1>"
"""

@app.before_request
def limit_request():
    client_ip = request.remote_addr
    if is_rate_limited(client_ip):
        return jsonify({"error": "Too Many Requests"}), 429


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
    time_remaining = r.ttl(name)
    if value is None:
        return jsonify({"error": "Note not found or expired"}), 404
    return jsonify({"note_name": name, "note_value": value, "expires_in": time_remaining})


@app.route("/limit", methods=["GET"])
def get_limit():
    client_ip = request.remote_addr
    key = f"rate_limit:{client_ip}"
    value = r.get(key)

    if value is None:
        return {"requests_this_window": 0}

    return {"requests_this_window": int(value)}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)




