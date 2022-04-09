class Competition:

    name: str
    judges_per_student: int
    judges: list
    students: list
    catigories: list

    def __init__(self, name) -> None:
        self.name = name
        self.judges_per_student = 2
        self.judges = []
        self.students = []
        self.categories = []
    
    def to_dict(self) -> dict:
        judges = []
        for judge in self.judges:
            judges.append(judge.to_dict())
        students = []
        for i in range(len(self.students)):
            students.append(self.students[i].to_dict(i))
        return {
            "name": self.name,
            "judges_per_student": self.judges_per_student,
            "judges": judges,
            "students": students,
            "categories": self.categories
        }