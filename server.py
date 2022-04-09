from flask import Flask, jsonify

from competiton import Competition

app = Flask(__name__)

competitions = {}

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/competition/<name>", methods=["PUT"])
def create_competition(name):
    if name in competitions:
        return jsonify({"success_code": 1, "error_message": "name already exsists"})
    competitions[name] = Competition(name)
    return jsonify({"success_code": 0})

@app.route("/api/competition/<name>", methods = ["DELETE"])
def delete_competition(name):
    if name not in competitions:
        return jsonify({"success_code": 1, "error_message": "competition does not exsist"})
    competitions.pop(name)
    return jsonify({"success_code": 0})