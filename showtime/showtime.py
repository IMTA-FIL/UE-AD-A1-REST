from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

with open('{}/databases/times.json'.format("."), "r") as jsf:
   schedule = json.load(jsf)["schedule"]

@app.route("/", methods=['GET'])
def home():
   return make_response("<h1 style='color:blue'>Welcome to the Showtime service!</h1>",200)

# Fonction pour retourner toute la base de données times : La liste des
# dates avec les films qui seraient projetés
@app.route("/showtimes", methods=['GET'])
def get_schedule():
       result = make_response({"schedule":schedule},200)
       return result

# Fonction pour retourner la liste des films projetés pour une date donnée
@app.route("/showmovies/<date>", methods=['GET'])
def get_movies_bydate(date):
      for showtime in schedule:
            if str(showtime["date"]) == str(date):
                    result = make_response(jsonify(showtime),200)
                    return result
      
      return make_response(jsonify({"error":"Date not available"}),400)
            

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
