from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import datetime
app = Flask(__name__)

app.config["MONGO_URI"]="mongodb+srv://lab3db:rSpFJI8hLVz0ZI5Y@cluster0.snfwm.mongodb.net/LAB3?retryWrites=true&w=majority"
mongo = PyMongo(app)

list_of_tanks=[]
id=0
person={}

@app.route('/', methods=['GET'])

@app.route('/profile',  methods=["GET", "POST","PATCH"])
def profile():
  if request.method == "POST":
    t=datetime.datetime.now()
    global person 
    person = {
        "last_updated":t,
        "username":request.json["username"],
        "role":request.json["role"],
        "color":request.json["color"]
    }
    return {"data":person}
  elif request.method == "GET":
    return person
  elif request.method == "PATCH":
    if "username" in request.json:
      person["username"] = request.json["username"]

    if "role" in request.json:
      person["role"] = request.json["role"]

    if "color" in request.json:
      person["color"] = request.json["color"]

    t = datetime.datetime.now()

    return {
      "data": person
    }

@app.route('/data', methods=["GET","POST"])
def data():
  if request.method == "GET":
    return jsonify(list_of_tanks)
  if request.method == "POST":
    global id
    id+=1
    tank={
        "location":request.json["location"],
        "lat":request.json["lat"],
        "long":request.json["long"],
        "percentage_full":request.json["percentage_full"],
        "id":id
    }
    list_of_tanks.append(tank)
    return jsonify(tank)


@app.route('/data/<int:id>', methods=["PATCH"])
def datapatch(id):
  for x in list_of_tanks:
    if id == x["id"]:
      if "location" in request.json:
        x["location"] = request.json["location"]    
      if "lat" in request.json:
        x["lat"] = request.json["lat"]
      if "long" in request.json:
        x["long"] = request.json["long"]
      if "percentage_full" in request.json:
        x["percentage_full"] = request.json["percentage_full"]
  return jsonify(list_of_tanks[int(id)-1])

@app.route('/data/<int:id>', methods=["DELETE"])
def deletank(id):
  for x in list_of_tanks:
    if id == x["id"]:
      list_of_tanks.remove(x);
  return {
    "success": True
    }

if __name__ =="__main__":
    app.run(debug=True,
    port=3000,
    host="0.0.0.0")