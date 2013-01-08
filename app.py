import os
from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def answer():
    q = request.args.get("q", "")
    return "Flask"

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 8080))
    # app.run(host='0.0.0.0', port=port)
    app.run(host='127.0.0.1', port=port, debug=True)
