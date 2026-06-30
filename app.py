from flask import Flask, render_template, request, send_file, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return "JiraExtractor running"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
