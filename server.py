from flask import Flask, jsonify, request

from competiton import Competition

app = Flask(__name__)

competitions = {"name": Competition("name")}

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/competition/<name>", methods=["GET"])
def get_competition(name):
    if name not in competitions:
        return jsonify({"success_code": 2, "error_message": "Competition not found"})
    return jsonify(competitions[name].to_dict())

@app.route("/api/competition/", methods=["PUT"])
def create_competition():
    name = request.form.get("name")
    if name is not None:
        return jsonify({"success_code": 1, "error_message": "must provide name."})
    if name in competitions:
        return jsonify({"success_code": 1, "error_message": "name already exsists."})
    competitions[name] = Competition(name)
    return jsonify({"success_code": 0})

@app.route("/api/competition/", methods=["DELETE"])
def delete_competition():
    name = request.form.get("name")
    if name is not None:
        return jsonify({"success_code": 1, "error_message": "must provide name."})
    if name not in competitions:
        return jsonify({"success_code": 1, "error_message": "competition does not exsist."})
    competitions.pop(name)
    return jsonify({"success_code": 0})

@app.route("/api/competion/", methods=["POST"])
def update_competition():
    name = request.form.get("name")
    new_name = request.form.get("new_name")
    number_of_judges = request.form.get("number_of_judges")
    if name in competitions:
        return jsonify({"success_code": 1, "error_message": "competition with name already exsists."})
    if number_of_judges < 0:
        return jsonify({"success_code": 1, "error_message": "can not have a negative number of judges."})
    competitions[name]
