from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
    bookings = json.load(jsf)["bookings"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

@app.route("/bookings", methods=['GET'])
def get_bookings():
    json = jsonify(bookings)
    response = make_response(json, 200)
    return response

@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_from_userid(userid):
    json = ""
    for booking in bookings:
        if booking['userid'] == userid:
            json = booking

    if not json:
        response = make_response(jsonify({"error" : "bad input parameter"}), 400)
    else :
        response = make_response(jsonify(json), 200)
    return response


def write(bookings):
    data = {"bookings": bookings}
    with open('./databases/bookings.json', 'w') as f:
        json.dump(data, f, indent=4)



if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
