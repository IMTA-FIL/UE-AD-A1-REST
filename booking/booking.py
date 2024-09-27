from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'
TIMES_HOST = 'http:localhost:3202/showtimes'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
	bookings = json.load(jsf)["bookings"]

@app.route("/", methods=['GET'])
def home():
	return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

@app.route("/bookings", methods=['GET'])
def get_all():
	return make_response(jsonify(bookings), 200)

@app.route('/bookings/<userid>', methods=['GET'])
def bookings_user(userid):
	for b in bookings:
		if str(b['userid']) == str(userid):
			return make_response(jsonify(b), 200)
	return make_response(jsonify({'error': 'bad input parameter'}), 400)

@app.route('/bookings/<userid>', methods=['POST'])
def add_booking(userid):
	# TODO appeler Times pour vérifier
	req = request.get_json()
	booking = None
	for b in bookings:
		if str(b['userid']) == str(userid):
			booking = b
	if booking == None:
		booking = {"userid": str(userid), "dates": []}
		bookings.append(booking)
	need_new = True
	for d in booking["dates"]:
		if d["date"] == req["date"]:
			if any([m == req["movieid"] for m in d["movies"]]):
				return make_response(jsonify({'error': 'booking already exists'}), 409)
			d["movies"].append(req["movieid"])
			need_new = False
	if need_new:
		booking["dates"].append({"date": req["date"], "movies": [req["movieid"]]})
	write(bookings)
	return make_response(jsonify(booking), 200)

def write(bookings):
	with open('{}/databases/bookings.json'.format("."), 'w') as f:
		json.dump({'bookings':bookings}, f, indent=4)

if __name__ == "__main__":
	print("Server running in port %s"%(PORT))
	app.run(host=HOST, port=PORT)
