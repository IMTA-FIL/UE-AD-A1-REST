from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'
BOOKING_PATH="http://localhost:3201"
MOVIE_PATH="http://localhost:3200"

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/movies_per_ratings",methods=["GET"])
def get_movies_per_ratings():
   """This function will get all the movies available sorted by rating"""
   return requests.request("GET", MOVIE_PATH +"/movies_per_ratings")

@app.route("/movies_available/<date>",methods=["GET"])
def get_movies_available_at_date(date:str):
   """This function shows what are the movies available at the date date"""
   pass

@app.route("/book_a_movie/<moviename>/<username>")
def book_the_movie(moviename:str,username:str):
   """This function books the movie name moviename for the user username"""
   pass

@app.route("/booking_made/<username>",methods=["GET"])
def get_booking_made(username:str):
   """This function will get all the booking already made by username"""
   return requests.request("GET", BOOKING_PATH + "/bookings/" + convert_username_id(username))

def convert_username_id(username:str):
   """This get the id corresponding to the user username"""
   for user in users:
      if user["name"]==username:
         return user["id"]

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
