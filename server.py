from flask import Flask

app = Flask(__name__)

num = [0]

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/temp/")
def temp():
    num[0] += 1
    return f"<p>This is a second routing! {num[0]}</p>"