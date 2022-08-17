from datetime import datetime
from lesson import Lesson
import json
from zoneinfo import ZoneInfo
from ast import literal_eval
from flask import *
from werkzeug.middleware.proxy_fix import ProxyFix


with open("data.json") as f:
    data = json.load(f)

app = Flask(__name__)
app.jinja_env.globals.update(zip=zip)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)


def get_current_dt() -> datetime:
    pkt = ZoneInfo("Asia/Karachi")
    return datetime.now(pkt)


@app.route("/set_subjects", methods=["POST", "GET"])
def set_subjects():
    if request.method == "GET":
        return render_template("set_subjects.html")
    resp = make_response(redirect(url_for("index")))
    resp.set_cookie(
        "subjects", json.dumps(dict(request.form)), max_age=60 * 60 * 24 * 90
    )
    return resp


@app.route("/")
def index():
    dt = get_current_dt()
    day = request.args.get("day", dt.strftime("%a").upper())
    if day.upper() not in ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]:
        day = dt.strftime("%a").upper()

    if day.upper() in ["SAT", "SUN"]:
        day = "MON"

    # Check if subject cookie has been set
    if not request.cookies.get("subjects"):
        return redirect(url_for("set_subjects"))

    lessons = Lesson.get_lessons(
        day,
        literal_eval(request.cookies["subjects"])["section"],
        [
            literal_eval(request.cookies["subjects"])[opt]
            for opt in ["OPT-A", "OPT-B", "OPT-C", "OPT-D"]
        ],
        bool(literal_eval(request.cookies.get("subjects")).get("remedial-urdu", False)),
    )
    with open("data.json") as f:
        data = json.load(f)

    times = data["Timings"]["Regular"] if day != "FRI" else data["Timings"]["Friday"]
    t = []
    for start, end in times:
        t.append(f"{start}\n{end}")

    full_day = {
        "MON": "Monday",
        "TUE": "Tuesday",
        "WED": "Wednesday",
        "THU": "Thursday",
        "FRI": "Friday",
        "SAT": "Saturday",
        "SUN": "Sunday",
    }[day]

    return render_template("index.html", lessons=lessons, day=full_day, times=t)


@app.route("/favicon.png")
def favicon():
    return app.send_static_file("favicon.png")
