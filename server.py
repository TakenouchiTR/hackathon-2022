import json
from flask import Flask, jsonify, request, render_template

from competiton import Competition
from student import Student
from judge import Judge

app = Flask(__name__)

competitions = {"name": Competition("name")}
competitions["name"].students.append(Student("shoon", "science"))
competitions["name"].students.append(Student("garrett", "cars"))
competitions["name"].categories.append("stuff")
competitions["name"].categories.append("things")
competitions["name"].judges.append(Judge("judge"))
competitions["name"].judges.append(Judge("a guy"))

@app.route("/")
def index():
    return render_template("judging_page.html", 
        competition_names=competitions.keys()
    )

@app.route("/app/<competition_name>", methods=["GET"])
def main_app(competition_name):
    return render_template("app.html", 
        competition_name=competition_name
    )

@app.route("/app/<competition_name>/judges", methods=["GET"])
def get_judges(competition_name):
    print(competitions[competition_name].judges)
    judge_names = list(map(lambda judge: judge.name, competitions[competition_name].judges))
    return render_template("add_judge.html", judge_names=judge_names, competition_name=competition_name)

@app.route("/app/<competition_name>/students", methods=["GET"])
def get_students_page(competition_name):
    judge_names = list(map(lambda judge: judge.name, competitions[competition_name].judges))
    student_names = list(map(lambda student: student.name, competitions[competition_name].students))
    categories = competitions[competition_name].categories
    return render_template("student_scores.html", judges=judge_names, categories=categories, student_names=student_names)

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
    name = request.get_json()["name"]
    if name is None:
        return jsonify({"success_code": 1, "error_message": "must provide name."})
    if name in competitions:
        return jsonify({"success_code": 1, "error_message": "name already exsists."})
    competitions[name] = Competition(name)
    print(competitions.keys())
    return jsonify({"success_code": 0})

@app.route("/api/competition/", methods=["DELETE"])
def delete_competition():
    name = request.get_json()["name"]
    if name is None:
        return jsonify({"success_code": 1, "error_message": "name must provide name."})
    if name not in competitions:
        return jsonify({"success_code": 1, "error_message": "competition does not exsist."})
    competitions.pop(name)
    return jsonify({"success_code": 0})

@app.route("/api/competition/", methods=["POST"])
def update_competition():
    name = request.get_json()["name"]
    new_name = request.get_json()["new_name"]
    judges_per_student = request.get_json()["judges_per_student"]

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
    name = request.get_json()["name"]
    if name is None:
        return jsonify({"success_code": 1, "error_message": "must provide name."})

    judge_name = request.get_json()["judge_name"]
    if judge_name is None:
        return jsonify({"success_code": 1, "error_message": "judge's name can not be empty."})
    competitions[name].judges.append(Judge(judge_name))
    return jsonify({"success_code": 0})

@app.route("/api/competition/judge/", methods=["GET"])
def get_judge():
    name = request.args.get('name')
    judge_index = request.args.get('judge')
    if name is None:
        return jsonify({"success_code": 1, "error_message": "must provide name."})
    if name not in competitions:
        return jsonify({"success_code": 2, "error_message": "Competition not found"})
    if judge_index is not None:
        if not str.isnumeric(judge_index):
            return jsonify({"success_code": 1, "error_message": "judge must be a number."})
        judge_index = int(judge_index)

    competition = competitions[name]
    if judge_index is None:
        judges = []
        for judge in competitions[name]:
            judges.append(judge.to_dict())
        return jsonify(judges)
    
    return jsonify(competition.judges[judge_index].to_dict())

@app.route("/api/competition/judge/", methods=["POST"])
def update_judge():
    name = request.get_json()["name"]
    judge_index = request.get_json()["judge"]
    student_index = request.get_json()["student"]

    if name is None:
        return jsonify({"success_code": 1, "error_message": "must provide name."})
    if name not in competitions:
        return jsonify({"success_code": 1, "error_message": "competition not found."})
    if judge_index is None:
        return jsonify({"success_code": 1, "error_message": "must provide judge."})
    if not str.isnumeric(judge_index):
        return jsonify({"success_code": 1, "error_message": "judge must be a number."})
    if student_index is None:
        return jsonify({"success_code": 1, "error_message": "must provide student."})
    if not str.isnumeric(student_index):
        return jsonify({"success_code": 1, "error_message": "student must be a number."})

    judge_index = int(judge_index)
    student_index = int(student_index)
    competition = competitions[name]

    if judge_index < 0 or judge_index >= len(competition.judges):
        return jsonify({"success_code": 1, "error_message": "judge does not exsist."})
    if student_index < 0 or student_index >= len(competition.students):
        return jsonify({"success_code": 1, "error_message": "student does not exsist."})

    judge = competition.judges[judge_index]

    if student_index in judge.students:
        return jsonify({"success_code": 1, "error_message": "student already assigned to judge."})
    
    judge.students.append(student_index)
    return jsonify({"success_code": 0})

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
    name = request.get_json()["name"]
    criteria = request.get_json()["criteria"]
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
                lambda student_index: competition.students[student_index].to_dict(student_index), 
                competition.judges[judge].students
            )
        )
    )

@app.route("/api/competition/student/", methods=["PUT"])
def add_student():
    name = request.get_json()["name"]
    student_name = request.get_json()["student_name"]
    topic = request.get_json()["topic"]

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

@app.route("/api/competition/student/", methods=["POST"])
def update_student():
    name = request.get_json()["name"]
    student_index = request.get_json()["student"]
    category = request.get_json()["category"]
    score = request.get_json()["score"]

    if name is None:
        return jsonify({"success_code": 1, "error_message": "name must be provided."})
    if student_index is None:
        return jsonify({"success_code": 1, "error_message": "student must be provided."})
    if category is None:
        return jsonify({"success_code": 1, "error_message": "category must be provided."})
    if score is None:
        return jsonify({"success_code": 1, "error_message": "score must be provided."})
    if not str.isnumeric(student_index):
        return jsonify({"success_code": 1, "error_message": "student must be a number."})
    if not str.isnumeric(score):
        return jsonify({"success_code": 1, "error_message": "score must be a number."})
    if name not in competitions:
        return jsonify({"success_code": 1, "error_message": "competition not found."})
    
    competition = competitions[name]
    student_index = int(student_index)
    score = int(score)

    if student_index < 0 or student_index >= len(competition.students):
        return jsonify({"success_code": 1, "error_message": "student does not exsist."})
    if category not in competition.categories:
        return jsonify({"success_code": 1, "error_message": "category does not exsist."})
    if score < 0 or score > 5:
        return jsonify({"success_code": 1, "error_message": "score must be between 0 and 5."})
    
    competition.students[student_index].scores[category] = score
    return jsonify({"success_code": 0})
