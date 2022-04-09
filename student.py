class Student:

    name: str
    topic: str
    scores: dict

    def __init__(self, name, topic) -> None:
        self.name = name
        self.topic = topic
        self.scores = {}
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "topic": self.topic,
            "scores": self.scores
        }