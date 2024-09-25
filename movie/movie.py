from flask import Flask, render_template, request, jsonify, make_response
import json
import sys
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

with open('{}/databases/movies.json'.format("."), 'r') as jsf:
   movies = json.load(jsf)["movies"]

# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>",200)

@app.route("/template", methods=['GET'])
def template():
    return make_response(render_template('index.html', body_text='This is my HTML template for Movie service'),200)

@app.route("/json", methods=['GET'])
def get_json():
    res = make_response(jsonify(movies), 200)
    return res

@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            res = make_response(jsonify(movie),200)
            return res
    return make_response(jsonify({"error":"Movie ID not found"}),400)

@app.route("/moviesbytitle", methods=['GET'])
def get_movie_bytitle():
    json = ""
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["title"]) == str(req["title"]):
                json = movie

    if not json:
        res = make_response(jsonify({"error":"movie title not found"}),400)
    else:
        res = make_response(jsonify(json),200)
    return res

{
  "title": "Test",
  "rating": 1.2,
  "director": "Someone",
  "id":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"
}

@app.route("/addmovie/<movieid>", methods=['POST'])
def add_movie(movieid):
    req = request.get_json()
    print("req : ", req)
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error":"movie ID already exists"}),409)

    movies.append(req)
    write(movies)
    res = make_response(jsonify({"message":"movie added"}),200)
    return res

@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie["rating"] = rate
            res = make_response(jsonify(movie),200)
            return res

    res = make_response(jsonify({"error":"movie ID not found"}),201)
    return res

@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movies.remove(movie)
            return make_response(jsonify(movie),200)

    res = make_response(jsonify({"error":"movie ID not found"}),400)
    return res

def write(movies):
    with open('{}/databases/movies.json'.format("."), 'w') as f:
        
        json.dump({"movies" : movies}, f)

#####################################
#####          ADDED            #####
#####################################
all_methods = {
    "GET": ["/","/help","/template","/json","/movies/<movieid>","/moviesbytitle","/movies_per_ratings","/directors"],
    "POST": ["/addmovie/<movieid>"],
    "PUT": ["/movies/<movieid>/<rate>","/directors/<movie_id>/<director_name>"],
    "DELETE": ["/movies/<movieid>"]
}

@app.route("/help",methods=["GET"])
def help():
    return all_methods

@app.route("/movies_per_ratings",methods=["GET"])
def get_movies_classify_per_ratings():
    """Function which sort the movies by ratings"""
    list_movies:list = []

    # We get the list of movies associated with there ranking
    for movie in movies:
        list_movies.append([movie["rating"],movie["title"]])
    list_movies.sort()
    body_text = ""
    # We format the text to create a list in the html screen
    for elem in list_movies:
        body_text += f"<li>{elem[1]} : {elem[0]} </li>\n"
    return make_response(render_template('movies_per_ratings.html', body_text=body_text),200)

@app.route("/directors",methods=["GET"])
def get_all_directors():
    """This function get the directors of all movies"""
    list_directors = []
    for movie in movies:
        list_directors.append(movie["director"])
    return jsonify({"list_directors" : list_directors})

@app.route("/directors/<movie_id>/<director_name>",methods=["PUT"])
def update_director_movie(director_name:str,movie_id:str):
    """This function change the director name of the movie whixh has as id movie_id"""
    for movie in movies:
        if str(movie["id"])==movie_id:
            movie["director"] = director_name
            res = make_response(jsonify(movie),200)
            return res
    return make_response(jsonify({"error":"movie ID not found"}),201)

if __name__ == "__main__":
    #p = sys.argv[1]
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)
