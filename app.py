import json
import datetime
from flask import Flask, request, render_template, abort, flash, redirect, url_for

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = b"fgp2938fsdf?/"


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


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        schools, total = get_data_index()
        return render_template(
            "index.html", schools=schools, total=total, names=get_names()
        )
    elif request.method == "POST":
        college = request.form.to_dict(flat=True)["name"]
        return redirect(f"colleges/{college}")


@app.route("/contribute", methods=["GET", "POST"])
def contribute():
    if request.method == "GET":
        return render_template("contribute.html")
    elif request.method == "POST":
        with open("data/contribute.json", "a") as f:
            json.dump(request.form.to_dict(flat=True), f)
            f.write("\n")
            flash("Successfully submitted.")
            return redirect(url_for("index"))
        return render_template("contribute.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html")
    elif request.method == "POST":
        with open("data/contact.json", "a") as f:
            json.dump(request.form.to_dict(flat=True), f)
            f.write("\n")
            flash("Successfully submitted.")
            return redirect(url_for("index"))
        return render_template("contact.html")


@app.route("/colleges/<name>")
def college(name):
    school = get_data_graph(name)
    if school is None:  # school not found in data
        abort(404)
    else:
        return render_template("college.html", school=school)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run()
