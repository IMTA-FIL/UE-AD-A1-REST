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
    return make_response("<h1 style='color:blue'>Welcome to the Movie service! :groalex:</h1>",200)

@app.route("/json", methods=['GET'])
def get_json():
    res = make_response(jsonify(movies), 200)
    return res

@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_by_id(movieid):
    for m in movies:
        if str(m['id']) == str(movieid):
            res = make_response(jsonify(m), 200)
            return res
    return make_response(jsonify({'error': 'Movie ID not found'}), 400)


@app.route('/addmovie/<movieid>', methods=['POST'])
def add_movie(movieid):
    req = request.get_json()
    for m in movies:
        if str(m['id']) == str(movieid):
            return make_response(jsonify({'error': 'Movie ID already exists'}), 409)
    movies.append(req)
    write(movies)
    res = make_response(jsonify({"message":"movie added"}),200)
    return res

@app.route('/movies/<movieid>/<rating>', methods=['PUT'])
def update_rating(movieid, rating):
    for m in movies:
        if str(m['id']) == str(movieid):
            m['rating'] = rating
            write(movies)
            return make_response(jsonify({'message': 'Success'}), 200)
    return make_response(jsonify({'error': 'Movie ID not found'}), 400)

@app.route('/movies/<movieid>', methods=['DELETE'])
def delete_movie(movieid):
    for m in movies:
        if str(m['id']) == str(movieid):
            movies.remove(m)
            write(movies)
            return make_response(jsonify({'message': 'Deleted successfully'}), 200)
    return make_response(jsonify({'error': 'Movie not found'}), 400)

def write(movies):
    with open('{}/databases/movies.json'.format("."), 'w') as f:
        json.dump({'movies':movies}, f, indent=4)

if __name__ == "__main__":
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)
