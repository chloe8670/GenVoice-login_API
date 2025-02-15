from flask import Flask, jsonify, request, abort
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()


users = {
    "joel87": {"password": "pwjoel87", "role": "Senior"},
    "shiminh": {"password": "pwshiminh", "role": "Junior"},
    "rishiaw": {"password": "pwrishiaw", "role": "Junior"}
}

 
cases = [
    {"name": "Jonathan Lim", "description": "A 28-year-old software engineer who is experiencing intense anxiety during team meetings and is struggling to speak up, fearing judgment from colleagues."},
    {"name": "Angela Paolo", "description": "A 42-year-old teacher who is coping with the recent loss of a parent and is finding it difficult to concentrate on work and daily responsibilities."},
    {"name": "Xu Yaoming", "description": "A 16-year-old high school student who is feeling overwhelmed by academic pressure and is struggling to balance schoolwork, extracurriculars, and personal time."}
]


@auth.verify_password
def verify_password(username, password):
    if username in users and users[username]["password"] == password:
        return username
    return None

 
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username in users:
        return jsonify({"message": "Username already exists"}), 400
    users[username] = {"password": password, "role": "Junior"}
    return jsonify({"message": "User registered successfully"}), 201

 
@app.route('/login', methods=['POST'])
@auth.login_required
def login():
    username = auth.current_user()
    role = users[username]["role"]
    return jsonify({"message": f"Login successful, role: {role}"}), 200

 
@app.route('/promote', methods=['POST'])
@auth.login_required
def promote():
    username = auth.current_user()
    if users[username]["role"] == "Senior":
        return jsonify({"message": "User is already Senior"}), 200

@app.route('/demote', methods=['POST'])
@auth.login_required
def demote():
    username = auth.current_user()
    if users[username]["role"] == "Junior":
        return jsonify({"message": "User is already Junior"}), 200
    users[username]["role"] = "Junior"
    return jsonify({"message": "User demoted to Junior"}), 200

 
@app.route('/cases', methods=['GET'])
@auth.login_required
def get_cases():
    return jsonify(cases), 200

 
@app.route('/case', methods=['POST'])
@auth.login_required
def add_case():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    if not name or not description:
        return jsonify({"message": "Missing name or description"}), 400
    cases.append({"name": name, "description": description})
    return jsonify({"message": "Case added successfully"}), 201


if __name__ == '__main__':
    app.run(debug=True)
   