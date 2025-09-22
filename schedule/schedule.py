from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

with open('{}/databases/times.json'.format("."), "r") as jsf:
   schedule = json.load(jsf)["schedule"]

def write(schedule_data):
    with open('{}/databases/times.json'.format("."), 'w') as f:
        full = {"schedule": schedule_data}
        json.dump(full, f, indent=2)

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"

@app.route("/schedule/<schedule_date>", methods=['GET'])
def get_schedule(schedule_date):
    for s in schedule:
        if str(s["date"]) == str(schedule_date):
            return make_response(jsonify(s),200)
            
    return make_response(jsonify({"error":"schedule not found"}),404)


@app.route("/schedule", methods=['POST'])
def create_schedule():
    req = request.get_json()
    
    date = req["date"]
    movie_id = req["movie_id"]
    
    for s in schedule:
        if s["date"] == date:
            if movie_id not in s["movies"]:
                s["movies"].append(movie_id)
                write(schedule)
                return make_response(jsonify({"message": "movie added to existing date"}), 200)
    
    new_schedule = {
        "date": date,
        "movies": [movie_id]
    }
    schedule.append(new_schedule)
    write(schedule)
    return make_response(jsonify({"message": "new schedule created"}), 201)


@app.route("/schedule/<schedule_date>", methods=['DELETE'])
def delete_schedule(schedule_date):
    req = request.get_json()
    
    movie_id = req["movie_id"]
    
    for s in schedule:
        if s["date"] == schedule_date:
            if movie_id in s["movies"]:
                s["movies"].remove(movie_id)
                
                if not s["movies"]:
                    schedule.remove(s)
                    write(schedule)
                    return make_response(jsonify({"message": "schedule date removed (no movies left)"}), 200)
                else:
                    write(schedule)
                    return make_response(jsonify({"message": "movie removed from schedule"}), 200)
            else:
                return make_response(jsonify({"error": "movie not found in this date"}), 404)
    
    return make_response(jsonify({"error": "schedule date not found"}), 404)
   


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
