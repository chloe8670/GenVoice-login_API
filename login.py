from flask import Flask, jsonify, request, abort
import json
import os
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()  # I want to add basic auth

# todo:encrypt password
 

USERS_FILE = "data/users.json"
CASES_FILE = "data/cases.json"

def read_json(file):
    with open(file, 'r') as f:
        return json.load(f)

def write_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)


@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Mental Health Institute API"}), 200


@auth.verify_password
def verify_password(username, password):
    print("verify:", username, password)
    users = read_json(USERS_FILE)
    user = next((user for user in users if user["username"] == username and user["password"] == password), None)
    if user:
        return username
    return None


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username, password = data.get('username'), data.get('password')
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    users = read_json(USERS_FILE)
    if any(user["username"] == username for user in users):
        return jsonify({"error": "Username already exists"}), 400

    new_user = {
        "username": username,
        "password": password,
        "role": "Junior"  # default
    }
    users.append(new_user)
    write_json(USERS_FILE, users)

    return jsonify({"message": "User registered successfully"}), 201

 
@app.route('/login', methods=['POST'])
@auth.login_required
def login():
    username = auth.current_user()
    users = read_json(USERS_FILE)
    user = next((user for user in users if user["username"] == username), None)
    return jsonify({"message": "Login successful", "role": user["role"]}), 200

 
@app.route('/promote', methods=['POST'])
@auth.login_required
def promote():
    username = auth.current_user()
    users = read_json(USERS_FILE)
    user = next((user for user in users if user["username"] == username), None)
    if user["role"] == "Senior":
        return jsonify({"message": "User is already Senior"}), 200
    user["role"] = "Senior"
    write_json(USERS_FILE, users)

    return jsonify({"message": "User promote to Senior"}), 200


@app.route('/demote', methods=['POST'])
@auth.login_required
def demote():
    username = auth.current_user()
    users = read_json(USERS_FILE)
    user = next((user for user in users if user["username"] == username), None)
    if user["role"] == "Junior":
        return jsonify({"message": "User is already Junior"}), 200
    user["role"] = "Junior"
    write_json(USERS_FILE, users)

    return jsonify({"message": "User demoted to Junior"}), 200

 
@app.route('/cases', methods=['GET'])
@auth.login_required
def get_cases():
    cases = read_json(CASES_FILE)
    return jsonify(cases), 200

 
@app.route('/case', methods=['POST'])
@auth.login_required
def add_case():
    data = request.json
    name = data.get('name')
    description = data.get('description')

    if not name or not description:
        return jsonify({"error": "Missing name or description"}), 400

    cases = read_json(CASES_FILE)
    new_case = {
        "name": name,
        "description": description
    }
    cases.append(new_case)
    write_json(CASES_FILE, cases)

    return jsonify({"message": "Case added successfully"}), 201


if __name__ == '__main__':
    app.run(debug=True)
   