import os

from flask import Flask, request, jsonify

from rate_limit import is_rate_limited
from request_model import NoteModel, SignIn
from pydantic import ValidationError
from database import r, connect
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt, JWTManager, jwt_required
from config import load_config
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)


# Allowed expiration times
EXPIRATION_OPTIONS = [5, 10, 20, 30, 60, 120, 240, 360]

@app.before_request
def limit_request():
    client_ip = request.remote_addr
    if is_rate_limited(client_ip):
        return jsonify({"error": "Too Many Requests"}), 429


@app.route("/")
def home_page():
    return jsonify("endpoint reached")

@app.route("/signin", methods=["POST"])
def sign_in():
    try:
        data = SignIn(**request.json) #retrieve client data and validate with pydantic
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    username = data.username
    password = data.password

    try:
        conn = connect(load_config()) #establish connection
        if conn is None: #if connection fails, return code 500
            return jsonify({"error": "Database connection failed"}), 500

        with conn.cursor() as cur: #else use cursor, with block automatically closes the connection in the end
            cur.execute("SELECT id, password_hash FROM users WHERE username=%s", (username,))
            user = cur.fetchone() #fetch the first result

            if user:
                return jsonify({"error": "User already exists"}), 401

            else:
                # Create new user
                hashed_pw = generate_password_hash(password)
                cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id",
                            (username, hashed_pw))
                new_id = cur.fetchone()[0]
                conn.commit()


                return jsonify({"message": "User created", "user_id": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/login", methods=["POST"])
def login():
    data = SignIn(**request.json)
    username = data.username
    password = data.password

    try:
        conn = connect(load_config())
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cur = conn.cursor()
        try:
            cur.execute("SELECT password_hash FROM users WHERE username=%s", (username,))
            password_hash = cur.fetchone()[0]  # fetch the first result

        except Exception as error:
            return {"possible_error": "user does not exist",
                    "error": "error" }

        check = check_password_hash(password_hash, password)

        if check:
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token)
        else:
            return jsonify({"error": "your password was incorrect"})




    except Exception as e:
        return jsonify({"error": {e}})



@app.route("/create", methods=["POST"])
@jwt_required()
def create_note():
    current_user = get_jwt_identity() #checks the header for a code to authenticate
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
@jwt_required()

def get_note(name):
    current_user = get_jwt_identity()
    value = r.get(name)
    time_remaining = r.ttl(name)
    if value is None:
        return jsonify({"error": "Note not found or expired"}), 404
    return jsonify({"note_name": name, "note_value": value, "expires_in": time_remaining})


@app.route("/limit", methods=["GET"])
@jwt_required()
def get_limit():
    current_user = get_jwt_identity()
    client_ip = request.remote_addr
    key = f"rate_limit:{client_ip}"
    value = r.get(key)

    if value is None:
        return {"requests_this_window": 0}

    return {"requests_this_window": int(value)}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)




