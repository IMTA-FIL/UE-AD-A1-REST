from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/users", methods=['GET'])
def get_users():
    # return all users
    pass


@app.route("/users/<userid>", methods=['GET'])
def get_user(userid):
    # return user with id
    pass

# récupérer tous les bookings d'un user (lien avec booking)

# même chose mais en récupérant aussi les infos des films (lien avec booking et movie)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
