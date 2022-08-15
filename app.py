from datetime import datetime
from lesson import Lesson
import json
from zoneinfo import ZoneInfo
from ast import literal_eval
from flask import *


app = Flask(__name__)


def get_current_dt() -> datetime:
    pkt = ZoneInfo("Asia/Karachi")
    return datetime.now(pkt)


@app.route("/set_subjects", methods=["POST", "GET"])
def set_subjects():
    if request.method == "GET":
        return render_template("set_subjects.html")
    resp = make_response(redirect(url_for("index")))
    resp.set_cookie("subjects", json.dumps(dict(request.form)))
    return resp


@app.route("/")
def index():
    # Check if subject cookie has been set
    if not request.cookies.get("subjects"):
        return redirect(url_for("set_subjects"))

    lessons = Lesson.get_lessons(
        get_current_dt(),
        literal_eval(request.cookies["subjects"])["section"],
        [
            literal_eval(request.cookies["subjects"])[opt]
            for opt in ["OPT-A", "OPT-B", "OPT-C", "OPT-D"]
        ],
    )
    return render_template("index.html", lessons=lessons)
