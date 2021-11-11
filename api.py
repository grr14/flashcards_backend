import time
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello les pds!"

@app.route('/time')
def get_current_time():
    return {'time': time.time()}