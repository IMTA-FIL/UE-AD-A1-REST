from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'
BOOKING_HOST = 'http://localhost:3201/bookings/'
MOVIES_HOST = 'http://localhost:3200/movies/'

with open('{}/databases/users.json'.format("."), "r") as jsf:
	users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
	return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/users", methods=['GET'])
def user():
	return make_response(jsonify(users), 200)

@app.route("/users/<userid>", methods=['POST'])
def add_user(userid):
    req = request.get_json()
    for u in users:
        if str(u['id']) == str(userid):
            return make_response(jsonify({'error': 'User ID already exists'}), 409)
    users.append(req)
    write(users)
    res = make_response(jsonify({"message":"user added"}),200)
    return res

@app.route('/users/<userid>', methods=['DELETE'])
def delete_movie(userid):
    for u in users:
        if str(u['id']) == str(userid):
            users.remove(u)
            write(users)
            return make_response(jsonify({'message': 'Deleted successfully'}), 200)
    return make_response(jsonify({'error': 'User not found'}), 400)

def write(users):
    with open('{}/databases/users.json'.format("."), 'w') as f:
        json.dump({'users':users}, f, indent=4)

if __name__ == "__main__":
	print("Server running in port %s"%(PORT))
	app.run(host=HOST, port=PORT)
