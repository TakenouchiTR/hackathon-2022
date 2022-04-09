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
        return {
            "name": self.name,
            "judges_per_student": self.judges_per_student,
            "judges": self.judges,
            "students": self.students,
            "categories": self.categories
        }