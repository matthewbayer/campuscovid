import json
import datetime
from flask import Flask, request, render_template, abort, flash, redirect, url_for

application = Flask(__name__, static_url_path="/static")
application.secret_key = b"fgp2938fsdf?/"


def is_last_week(date_str):
    m, d, y = date_str.split("/")
    event_date = datetime.date(int(y) + 2000, int(m), int(d))
    time_since = datetime.date.today() - event_date
    return time_since.days <= 7


def get_data_index():
    with open("data/data.json", "r") as f:
        data = json.loads(f.read())

    schools = []
    for school_json in data:
        school_data = {}
        school_data["total_cases"] = 0
        school_data["cases_past_week"] = 0
        school_data["name"] = school_json["Name"]
        for event in school_json["Events"]:
            school_data["total_cases"] += dict(event).get("New Cases", 0)
            if is_last_week(event["Date"]):
                school_data["cases_past_week"] += dict(event).get("New Cases", 0)
        school_data["cases_today"] = 0
        schools.append(school_data)
    schools = sorted(schools, key=lambda s: s["total_cases"])
    schools.reverse()
    for rank, school in enumerate(schools):
        school["rank"] = rank + 1
    total = sum([school["total_cases"] for school in schools])
    return schools, total


def get_data_graph(school_name):
    with open("data/data.json", "r") as f:
        data = json.loads(f.read())

    schools = []
    for school_json in data:
        if (
            school_json["Name"].lower().replace(" ", "-").replace(",", "")
            == school_name
        ):
            return school_json
    return None


def get_names():
    with open("data/data.json", "r") as f:
        data = json.loads(f.read())
    return [d["Name"] for d in data]


@application.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        schools, total = get_data_index()
        return render_template(
            "index.html", schools=schools, total=total, names=get_names()
        )
    elif request.method == "POST":
        college = request.form.to_dict(flat=True)["name"]
        return redirect(f"colleges/{college}")


@application.route("/contribute", methods=["GET", "POST"])
def contribute():
    if request.method == "GET":
        return render_template("contribute.html", names=get_names())
    elif request.method == "POST":
        with open("/var/log/app-logs/contribute.json", "a") as f:
            json.dump(request.form.to_dict(flat=True), f)
            f.write("\n")
            flash("Successfully submitted.")
            return redirect(url_for("index"))
        return render_template("contribute.html", names=get_names())


@application.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html", names=get_names())
    elif request.method == "POST":
        with open("/var/log/app-logs/contact.json", "a") as f:
            json.dump(request.form.to_dict(flat=True), f)
            f.write("\n")
            flash("Successfully submitted.")
            return redirect(url_for("index"))
        return render_template("contact.html", names=get_names())


@application.route("/colleges/<name>")
def college(name):
    school = get_data_graph(name)
    if school is None:  # school not found in data
        abort(404)
    else:
        return render_template("college.html", school=school, names=get_names())


@application.errorhandler(404)
def not_found(e):
    return render_template("404.html", names=get_names())


if __name__ == "__main__":
    application.run()