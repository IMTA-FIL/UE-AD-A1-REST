from http.client import responses

import yaml
from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

# A VOIR POUR METTRE DANS UN .ENV ?
PORT = 3203
HOST = '0.0.0.0'
BOOKING_SERVICE_URL = "http://localhost:3201/bookings/"
MOVIE_SERVICE_URL = "http://localhost:3200/movies/"

with open('{}/databases/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]
with open("UE-archi-distribuees-User-1.0.0-resolved.yaml", "r") as f:
    openapi_spec = yaml.safe_load(f)

@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/users", methods=['GET'])
def get_users():
    json = jsonify(users)
    response = make_response(json, 200)
    return response


@app.route("/users/<userid>", methods=['GET'])
def get_user_byid(userid):
    for user in users:
        if str(user['id']) == str(userid):
            res = make_response(json.dumps(user), 200)
            return res
    return make_response(jsonify({'error': 'User not found'}), 404)


@app.route("/users/<userid>", methods=['POST'])
def add_user_byid(userid):
    req = request.get_json()

    for user in users:
        if str(user['id']) == str(userid):
            return make_response(jsonify({'error': 'User ID already exists'}), 409)

    users.append(req)
    write(users)

    return make_response(jsonify({"message": "user added"}), 200)


@app.route("/users/<userid>", methods=['UPDATE'])
def update_user_byid(userid):
    req = request.get_json()

    for user in users:
        if str(user['id']) == str(userid):
            users.remove(user)
            users.append(req)
            write(users)
            return make_response(jsonify({"message": "user updated"}), 200)
    return make_response(jsonify({'error': 'User not found'}), 404)

@app.route("/users/<userid>", methods=['DELETE'])
def del_user_byid(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            users.remove(user)
            return make_response(jsonify(user),200)

    res = make_response(jsonify({"error":"user ID not found"}),400)
    return res


# récupérer tous les bookings d'un user (lien avec booking)
@app.route("/users/<userid>/booking", methods=['GET'])
def get_bookings_of_user_byuserid(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            try:
                response = requests.get(f"{BOOKING_SERVICE_URL}{userid}")
                if response.status_code != 200:
                    return make_response(jsonify({"error": "item not found"}), 400)

                bookings = response.json().get("", [])
                return make_response(jsonify({"dates": bookings}), 200)
            except requests.RequestException as e:
                return make_response(jsonify({"error": "Error contacting Booking service", "details": str(e)}), 500)

    return


# même chose, mais en récupérant aussi les infos des films (lien avec booking et movie)
# TO DO


@app.route("/help", methods=['GET'])
def get_help():
    paths = openapi_spec.get("paths", {})
    help_info = []

    for path, path_data in paths.items():
        for method, method_data in path_data.items():
            help_info.append({
                "url": path,
                "method": method.upper(),
                "summary": method_data.get("summary", "No summary available"),
                "description": method_data.get("description", "No description available")
            })
    return jsonify({"endpoints": help_info})


def write(users):
    data = {"users": users}
    with open('./databases/users.json', 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
