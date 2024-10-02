from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

with open('{}/databases/times.json'.format("."), "r") as jsf:
    schedules = json.load(jsf)["schedule"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"


@app.route("/showtimes", methods=['GET'])
def get_schedules():
    json = jsonify(schedules)
    res = make_response(json, 200)
    return res

def is_invalide_date(date):
    """
    only basic validation are made here
    we don't check is the date is a valid date, only if it's a valid string
    """
    if len(date) != 8:
        return True
    if not date.isdigit():
        return True
    return False


@app.route("/showmovies/<date>")
def get_schedules_by_date(date):
    if is_invalide_date(date):
        error_text = {"error": "bad input parameter"}
        response = make_response(jsonify(error_text), 400)
        return response

    json = []
    for schedule in schedules:
        if schedule["date"] == date:
            json.append(schedule)
    res = make_response(jsonify(json), 200)
    return res


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
