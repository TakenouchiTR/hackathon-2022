from flask import Flask, jsonify, request, render_template

from competiton import Competition

app = Flask(__name__)

competitions = {"name": Competition("name")}

@app.route("/")
def hello_world():
    return render_template("index.html", competition_names=competitions.keys())

@app.route("/api/competition", methods=["GET"])
def get_competition():
    name = request.args.get('name')
    if name is None:
        return jsonify({"success_code": 1, "error_message": "must provide name."})
    if name not in competitions:
        return jsonify({"success_code": 2, "error_message": "Competition not found"})
    return jsonify(competitions[name].to_dict())

@app.route("/api/competition/", methods=["PUT"])
def create_competition():
    name = request.form.get("name")
    if name is None:
        return jsonify({"success_code": 1, "error_message": "must provide name."})
    if name in competitions:
        return jsonify({"success_code": 1, "error_message": "name already exsists."})
    competitions[name] = Competition(name)
    print(competitions.keys())
    return jsonify({"success_code": 0})

@app.route("/api/competition/", methods=["DELETE"])
def delete_competition():
    name = request.form.get("name")
    if name is None:
        return jsonify({"success_code": 1, "error_message": "name must provide name."})
    if name not in competitions:
        return jsonify({"success_code": 1, "error_message": "competition does not exsist."})
    competitions.pop(name)
    return jsonify({"success_code": 0})

@app.route("/api/competition/", methods=["POST"])
def update_competition():
    name = request.form.get("name")
    new_name = request.form.get("new_name")
    judges_per_student = request.form.get("judges_per_student")

    if judges_per_student is not None:
        if not str.isnumeric(judges_per_student):
            return jsonify({"success_code": 1, "error_message": "judges_per_student must be a number."})
        judges_per_student = int(judges_per_student)

    if name is None:
        return jsonify({"success_code": 1, "error_message": "name must provide name."})
    if new_name is None and judges_per_student is None:
        return jsonify({"success_code": 1, "error_message": "must provide new_name or number_of_judges."})
    
    if name not in competitions:
        return jsonify({"success_code": 1, "error_message": "competition not found."})
    if new_name is not None and new_name in competitions:
        return jsonify({"success_code": 1, "error_message": "new_name already exsists."})
    if new_name is not None and new_name == "":
        return jsonify({"success_code": 1, "error_message": "new_name must not be empty."})
    if judges_per_student is not None and judges_per_student < 0:
        return jsonify({"success_code": 1, "error_message": "can not have a negative number of judges."})
    
    competition = competitions[name]
    if new_name is not None:
        competition.name = new_name
        competitions.pop(name)
        competitions[new_name] = competition
    if judges_per_student is not None:
        competition.judges_per_student = judges_per_student
    return jsonify({"success_code": 0})
