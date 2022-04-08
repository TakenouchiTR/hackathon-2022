class Competition:

    judges_per_student: int
    judges: list
    students: list
    catigories: list

    def __init__(self) -> None:
        self.judges_per_student = 1
        self.judges = []
        self.students = []
        self.catigories = []