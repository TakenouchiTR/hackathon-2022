class Judge:

    name: str
    students: list

    def __init__(self) -> None:
        self.name = ""
        self.students = []

    def to_dict(self):
        return {"name": self.name}
