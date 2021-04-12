from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import date
import pandas as pd
from const import *

client = MongoClient("mongodb+srv://admin:admin@cluster0.kvxff.mongodb.net/io?retryWrites=true&w=majority")
db = client.io
app = Flask(__name__)

@app.route('/api/data/infections')
def infectionis():
    start = date.fromisoformat(request.args.get('start').replace("Z", ""))
    end = date.fromisoformat(request.args.get('end').replace("Z", ""))

    df = pd.DataFrame(db.covid.find_one({ 'name': INFECTIONS })['data'])
    return df[start < df.data < end].to_json()