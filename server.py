from flask import Flask, jsonify, request, render_template

from competiton import Competition
from student import Student
from judge import Judge

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


@app.route("/api/competition/judge/", methods=["PUT"])
def create_judge():
    name = request.form.get("name")
    if name is None:
        return jsonify({"success_code": 1, "error_message": "must provide name."})

    judge_name = request.form.get("judge_name")
    if judge_name is None:
        return jsonify({"success_code": 1, "error_message": "judge's name can not be empty."})
    competitions[name].judges.append(Judge(judge_name))

@app.route("/api/competition/judge/", methods=["GET"])
def get_judge():
    name = request.args.get('name')
    if name is None:
        return jsonify({"success_code": 1, "error_message": "must provide name."})
    if name not in competitions:
        return jsonify({"success_code": 2, "error_message": "Competition not found"})
    
    judges = []
    for judge in competitions[name]:
        judges.append(judge.to_dict())
    return jsonify(judges)

@app.route("/api/competition/criteria/", methods=["GET"])
def get_criteria():
    name = request.args.get('name')
    if name is None:
        return jsonify({"success_code": 1, "error_message": "name must provide name."})
    if name not in competitions:
        return jsonify({"success_code": 1, "error_message": "competition not found."})
    return jsonify(competitions[name].categories)

@app.route("/api/competition/criteria/", methods=["POST"])
def add_criteria():
    name = request.form.get("name")
    criteria = request.form.get("criteria")
    if name is None:
        return jsonify({"success_code": 1, "error_message": "name must be provided."})
    if criteria is None:
        return jsonify({"success_code": 1, "error_message": "criteria must be provided."})
    if name not in competitions:
        return jsonify({"success_code": 1, "error_message": "competition not found."})
    competition = competitions[name]

    if criteria in competition.categories:
        return jsonify({"success_code": 1, "error_message": "criteria already exsists."})
    competition.categories.append(criteria)
    for student in competition.students:
        student.scores[criteria] = 0
    return jsonify({"success_code": 0})

@app.route("/api/competition/student/", methods=["GET"])
def get_students():
    name = request.args.get('name')
    judge = request.args.get('judge')
    if name is None:
        return jsonify({"success_code": 1, "error_message": "name must be provided."})
    if name not in competitions:
        return jsonify({"success_code": 1, "error_message": "competition not found."})
    if judge is not None:
        if not str.isnumeric(judge):
            return jsonify({"success_code": 1, "error_message": "judge must be a number."})
        judge = int(judge)
        if judge < 0 or judge >= len(competitions[name].judges):
            return jsonify({"success_code": 1, "error_message": "judge must be between 0 and number of judges."})
    
    competition = competitions[name]
    if judge is None:
        return jsonify(
            list(
                map(
                    lambda student: student.to_dict(), 
                    competition.students
                )
            )
        )
    return jsonify(
        list(
            map(
                lambda student: student.to_dict(), 
                filter(lambda student: student in competition.judges[judge].students)
            )
        )
    )

@app.route("/api/competition/student/", methods=["POST"])
def add_student():
    name = request.form.get("name")
    student_name = request.form.get("student_name")
    topic = request.form.get("topic")

    if name is None:
        return jsonify({"success_code": 1, "error_message": "name must be provided."})
    if student_name is None:
        return jsonify({"success_code": 1, "error_message": "student must be provided."})
    if topic is None:
        return jsonify({"success_code": 1, "error_message": "topic must be provided."})
    if name not in competitions:
        return jsonify({"success_code": 1, "error_message": "competition not found."})
    competition = competitions[name]

    student = Student(student_name, topic)
    competition.students.append(student)
    for criteria in competition.categories:
        competition.students[-1].scores[criteria] = 0
    return jsonify({"success_code": 0})
    return jsonify({"success_code": 0})
