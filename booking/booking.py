from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

with open("C:/ProgramData/Projets/ue-CONT/TP1/UE-AD-A1-REST/showtime/databases/times.json".format("."), "r") as jsf:
   schedule = json.load(jsf)["schedule"]

# We define a list of all the dates available in the schedule :
dates = []
for show in schedule : 
   dates.append(str(show["date"]))
print(dates)

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

@app.route("/bookings",methods=["GET"])
def get_json():
   """This function return all the movie's reservations"""
   return make_response(jsonify(bookings))

@app.route("/bookings/<userid>",methods=["GET"])
def get_booking_for_user(userid:str):
   """This function get all the bookings made by the user user_id """
   for reservation in bookings:
      if userid == reservation["userid"]: # We found the good user
         return make_response(jsonify(reservation["dates"]),200)
   # We didn't find the user so we return an error
   return make_response(jsonify({"error": "bad input parameter"}),400)

@app.route("/bookings/<userid>",methods=["POST"])
def add_booking_byuser(userid:str):
   """This function get all the bookings made by the user user_id """
   # We check if the user gave a new movie
   if request.args:
      req = request.args
      for reservation in bookings:
         if userid == reservation["userid"]: # We found the good user
            if req["date"] in dates : # Check if there are movies shown during that date
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
                        res = make_response(jsonify({"message":"Booking added"}),200)
                        return res   
               #It is a new date
               reservation["dates"].append({"date":req["date"],"movies":[req["movieid"]]})
               # We write in the database
               write(bookings)
               res = make_response(jsonify({"message":"Booking created"}),200)
               return res
            else :
               return make_response(jsonify({"error": "bad input : date is unavailable"}),202)
               
      # We didn't find the user so we return an error
      return make_response(jsonify({"error": "bad input parameter"}),201)
   return make_response(jsonify({"error": "Wrong input"}),400)

def write(movies):
    with open('{}/databases/bookings.json'.format("."), 'w') as f:
        
        json.dump({"movies" : movies}, f)
if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
