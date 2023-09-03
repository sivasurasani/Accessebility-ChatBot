from flask import Flask
app = Flask(__name__)
@app.route("/")
def intitiate():
    return "home"
if __name__  == "__main__":
    app.run(debug=True)