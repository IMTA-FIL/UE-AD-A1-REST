from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'
PATH_TIMES:str = "http://localhost:3202"

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

@app.route("/", methods=['GET'])
def home():
   """This function return the homepage of the API booking"""
   return make_response("<h1 style='color:blue'>Welcome to the Booking service!</h1>",200)

@app.route("/bookings",methods=["GET"])
def get_json():
   """This function return all the movie's reservations"""
   return make_response(jsonify(bookings),200)

@app.route("/bookings/<userid>",methods=["GET"])
def get_booking_for_user(userid:str):
   """This function get all the bookings made by the user user_id """
   for reservation in bookings:
      if userid == reservation["userid"]: # We found the good user
         return make_response({"dates":reservation["dates"],"userid":userid},200)
   # We didn't find the user so we return an error
   return make_response(jsonify({"error": "bad input parameter"}),400)

@app.route("/bookings/<userid>",methods=["POST"])
def add_booking_byuser(userid:str):
   """This function adds a booking at the bookings made by the user user_id"""
   # We check if the user gave a new movie

   if request.args:
      req = request.args
      # Firstly we check if the movie is available at the date req["date"]
      # We get the movies wich will be projected at the date req["date"]
      movies_available_response = requests.request('GET', PATH_TIMES + "/showmovies" + "/" + req["date"] )
      # The date doesn't exist
      if movies_available_response.status_code == 400:
         return make_response(jsonify({"error": "bad input parameter"}),201)
      else:
         # The movie ins't projected
         if req["movieid"] not in movies_available_response.json()["movies"]:
            return make_response(jsonify({"error": "bad input parameter"}),201)
      for reservation in bookings:
         if userid == reservation["userid"]: # We found the good user
               for date in reservation["dates"]:
                  if date["date"] == req["date"] :
                     # We need to check if the user didn't already book this movie
                     if req["movieid"] in date["movies"]:
                        return make_response(jsonify({"error": "an existing item already exists"}),409)
                     else:
                        # We add the movie 
                        date["movies"].append(req["movieid"])
                        # We write in the database
                        write(bookings)
                        
                        res = make_response({"userid":userid,"dates": date["movies"]},200) # We return the bookings of the day we add a booking
                        return res   
               #It is a new date
               reservation["dates"].append({"date":req["date"],"movies":[req["movieid"]]})
               # We write in the database
               write(bookings)
               # We return the bookings of the day we add a booking
               res = make_response({"userid":userid,"dates":[{"date":req["date"],"movies":[req["movieid"]]}]},200)
               return res
               
      # We didn't find the user so we need to add this user to our database
      bookings.append({
         "userid":userid,
         "dates": [{
            "date":req["date"],
            "movies":[req["movieid"]]
         }]
      })
      # We write in the database
      write(bookings)
      return make_response({"userid":userid,"dates":[{"date":req["date"],"movies":[req["movieid"]]}]},200)
   return make_response(jsonify({"error": "Wrong input"}),400)

@app.route("/movies_at_the_date/<date>",methods=["GET"])
def get_movie_at_date(date:str):
   """This function will get all the movies available at the date date"""
   # We ask the microservice times the movies available at date
   req = requests.request("GET", PATH_TIMES + f"/showmovies/{date}")
   if req.status_code == 200:
      # We have gotten the id of the movies
      return make_response(req.json(),200)
   # The request failed
   return make_response({"error":"There was a problem with the request"},400)

def write(book):
    with open('{}/databases/bookings.json'.format("."), 'w') as f:
        
        json.dump({"bookings" : book}, f)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
