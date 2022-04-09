class Judge:

    name: str

    def __init__(self, name) -> None:
        self.name = name
    
    def to_dict(self):
        return {"name": self.name}