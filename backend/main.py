from flask import Flask, jsonify
from pymongo import MongoClient
from const import *

client = MongoClient("mongodb+srv://admin:admin@cluster0.kvxff.mongodb.net/io?retryWrites=true&w=majority")
db = client.io
app = Flask(__name__)

@app.route('/api/data/infections')
def infectionis():
    data = db.covid.find_one({ 'name': INFECTIONS })['data']
    return jsonify(data)