from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route("/")
def index():
    query = (request.args.get("q") or "").strip()
    return render_template("index.html", query=query)

if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        print("* Search demo running at http://127.0.0.1:5002", flush=True)
    app.run(host="0.0.0.0", port=5002, debug=True)
