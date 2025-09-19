from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound
from datetime import datetime

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)


########################################################################################
#                                                                                      #
#                                FONCTIONS UTILITAIRES                                 #
#                                                                                      #
########################################################################################

def save_users(new_users: dict) -> None:
   with open('{}/databases/users.json'.format("."), "w") as jsf:
      json.dump(new_users, jsf, indent=2)


def get_user_by_id(user_id: str) -> dict | None:
   for u in users:
      if u["id"] == user_id:
         return u
   return None

def get_current_timestamp() -> int:
   return int(datetime.now().timestamp())


########################################################################################
#                                                                                      #
#                                        ROUTES                                        #
#                                                                                      #
########################################################################################

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/users/<user_id>", methods=["GET"])
def route_get_user_by_id(user_id: str):
   user = get_user_by_id(user_id)
   if user is None:
      return make_response(jsonify({"error":"User not found"}), 404)
   user["last_active"] = get_current_timestamp()
   save_users(users)
   return make_response(jsonify(user),200)


@app.route("/users/<user_id>/<user_name>", methods=["POST"])
def route_add_user(user_id: str, user_name: str):
   user = get_user_by_id(user_id)
   if user is not None:
      return make_response(jsonify({"error":"User already exists"}), 400)
   user = {
      "id": user_id,
      "name": user_name,
      "last_active": get_current_timestamp(),
      "admin": False
   }
   users.append(user)
   save_users(users)
   return make_response(jsonify({"message":"User created", "user":user}), 201)


@app.route("/users/<user_id>/<new_name>", methods=["PUT"])
def route_edit_user_name(user_id: str, new_name: str):
   user = get_user_by_id(user_id)
   if user is None:
      return make_response(jsonify({"error":"User not found"}), 404)
   user["name"] = new_name
   user["last_active"] = get_current_timestamp()
   save_users(users)
   return make_response(jsonify(user),200)


@app.route("/users/<user_id>/admin/yes", methods=["PUT"])
def route_edit_user_promote_admin(user_id: str):
   user = get_user_by_id(user_id)
   if user is None:
      return make_response(jsonify({"error":"User not found"}), 404)
   user["admin"] = True
   user["last_active"] = get_current_timestamp()
   save_users(users)
   return make_response(jsonify({"message":"User is now admin", "user_id":user_id}), 200)


@app.route("/users/<user_id>/admin/no", methods=["PUT"])
def route_edit_user_demote_admin(user_id: str):
   user = get_user_by_id(user_id)
   if user is None:
      return make_response(jsonify({"error":"User not found"}), 404)
   user["admin"] = False
   user["last_active"] = get_current_timestamp()
   save_users(users)
   return make_response(jsonify({"message":"User is no longer admin", "user_id":user_id}), 200)


@app.route("/users/<user_id>", methods=["DELETE"])
def route_delete_user(user_id: str):
   user = get_user_by_id(user_id)
   if user is None:
      return make_response(jsonify({"error":"User not found"}), 404)
   users.remove(user)
   save_users(users)
   return make_response(jsonify({"message":"User deleted", "user":user}), 200)


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
