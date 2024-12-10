from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound
import sys

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
   req = requests.request("GET", MOVIE_PATH +"/movies_per_ratings")
   if req.status_code == 200:
      list_movies = req.json()["list_movies_sorted"]
      # We format the text to create a list in the html screen
      body_text = ""
      for elem in list_movies:
         body_text += f"<li>{elem[1]} : {elem[0]} </li>\n" #elem[1] = movie_name & elem[2] = rating
      return make_response(render_template('movies_per_ratings.html', body_text=body_text),200)
   # The request failed
   return make_response({"error": "There was a problem during the request"},400)

@app.route("/movies_available/<date>",methods=["GET"])
def get_movies_available_at_date(date:str):
   """This function shows what are the movies (their name) available at the date date"""
   # We get the ids of the movies available
   req = requests.request("GET", BOOKING_PATH + f"/movies_at_the_date/{date}")
   if req.status_code==200:
      # Now we get all the dict which link the movie id with their title
      print("req.json() : ", req.json())
      req2 = requests.request("GET", MOVIE_PATH + "/movieid_linked_movietitle")
      if req2.status_code == 200:
         list_name = []
         dict_id_title = req2.json() # With this dict, we can convert an id into a title
         print("dict_id_title : ", dict_id_title)
         for movieid in req.json()["movies"]:
            print("")
            list_name.append(dict_id_title[movieid])
         body_text = ""
         for elem in list_name:
            body_text += f"<li>{elem} </li>\n" #elem[1] = movie_name & elem[2] = rating
         print("body_text = ", body_text)
         return make_response(render_template('get_movies_available_at_date.html',body_text=body_text,date=f"{date[0:4]}/{date[4:6]}/{date[6:]}"))
      return make_response({"error":"There was a problem during the request"},400)
      
   return make_response({"error":"There was a problem during the request"},400)

@app.route("/book_a_movie",methods=["POST"])
def book_the_movie(): 
   if request.get_json():
      """This function books the movie name moviename for the user username"""
      # We get the informations we want
      request_json = request.get_json()
      moviename, date, username = request_json["moviename"], request_json["date"],request_json["username"]
      # We need to convert the moviename into a movie_id
      req = requests.request("GET", MOVIE_PATH + "/movieid_linked_movietitle")
      if req.status_code == 200:
         print("Req a finit ")
         dict_id_to_name = req.json()
         # We seek the id corresponding to the title moviename
         for key in dict_id_to_name.keys():
            if moviename == dict_id_to_name[key]:
               # The id of the movie is key
               new_movie = {"date":date,"movieid":key}
               req2 = requests.request("POST",BOOKING_PATH + f"/bookings/{convert_username_id(username)}",
                                       params=new_movie)
               if req2.status_code==200:
                  print("movie name : ", moviename)
                  return make_response(render_template('booking_made.html',username=username),200)
               else: 
                  return make_response({"message":"We couldn't book the date, Sadge :'("},205)
      return make_response({"error": "Bad argument"},400)
   print("request.args : ", request)
   return make_response({"error":"Bad argument"},400)

@app.route("/booking_made/<username>",methods=["GET"]) # TO DO : ajouter l'utilisateur au lieu de lever une erreur ???
def get_booking_made(username:str):
   """This function will get all the booking already made by username"""
   # We check if the user is register in the user database
   for user_registered in users:
      if user_registered["name"] == username:
         print("username : ", username)
         # The user is in the database
         # We ask the api booking to give us all the booking of username
         req = requests.request("GET", BOOKING_PATH + "/bookings/" + convert_username_id(username)) #list_json
         if req.status_code==200:    
            if len(req.json()["dates"]) > 0:
               # The user made reservations
               # We get the dict which allow us to convert the id into a movie title
               req2 = requests.request("GET", MOVIE_PATH + "/movieid_linked_movietitle") # return a list
               if req2.status_code == 200:
                  dict_id_to_name = req2.json()
                  body_text = ""
                  for elem in req.json()["dates"]:
                     body_text+= f"<li> The {elem['date'][0:4]}/{elem['date'][4:6]}/{elem['date'][6:]}: \n<ul>"
                     for movieid in elem["movies"]:
                        body_text += "<li>"+dict_id_to_name[movieid] + "</li>\n"
                     body_text += "</ul></li>\n"
               return make_response(render_template('booking_made.html',body_text=body_text,username=username))
         # If we are here, it means that the user didn't book any movies
         return make_response(render_template('error_get_booking_per_user.html',body_text=f"Zero booking was made with the user {username}",error="301"),301)
   return make_response(render_template('error_get_booking_per_user.html',body_text=f"The user {username} doesn't exist",error="300"),300)

def convert_username_id(username:str):
   """This get the id corresponding to the user username"""
   for user in users:
      if user["name"]==username:
         return user["id"]


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   if len(sys.argv) > 1 and sys.argv[1] == "docker":
      print("Image loaded with docker")
      BOOKING_PATH = "http://booking:3201"
      MOVIE_PATH = "http://movie:3200"
   app.run(host=HOST, port=PORT)