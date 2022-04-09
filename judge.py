class Judge:

    name: str
    students: list

    def __init__(self, name) -> None:
        self.name = name
        self.students = []

    def to_dict(self):
        return {
            "name": self.name,
            "students": self.students,
        }
