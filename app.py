from flask import Flask, jsonify, request,json
from flask_pymongo import PyMongo
import datetime
from bson.json_util import dumps
from json import loads
import os
from dotenv import load_dotenv
from marshmallow import Schema,fields, ValidationError
app = Flask(__name__)

load_dotenv()

app.config["MONGO_URI"]=os.getenv("MONGO_CONNECTION_STRING")
mongo = PyMongo(app)

class TankSchema(Schema):
    location = fields.String(required=True)
    lat = fields.Float(required=True)
    long = fields.Float(required=True)
    percentage_full = fields.Integer(required=True)

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
        tanks = mongo.db.tanks.find()
        return jsonify(loads(dumps(tanks)))
  if request.method == "POST":
      try:
        newtank=TankSchema().load(request.json)
        tank_id = mongo.db.tanks.insert_one(newtank).inserted_id
        tank = mongo.db.tanks.find_one(tank_id)
        return loads(dumps(tank))
      except ValidationError as ve:
        return ve.messages, 400


@app.route('/data/<ObjectId:id>', methods=["PATCH"])
def datapatch(id):
    mongo.db.tanks.update_one({"_id":id},{"$set":request.data})
    tank = mongo.db.tanks.find_one(id)
    return loads(dumps(tank))

@app.route('/data/<ObjectId:id>', methods=["DELETE"])
def deletank(id):
    result = mongo.db.tanks.delete_one({"_id": id})
    if result.deleted_count == 1:
        return {
      "success": True
    }
    else:
        return {
      "success": False
    }, 400

if __name__ =="__main__":
    app.run(debug=True,
    port=3000,
    host="0.0.0.0")