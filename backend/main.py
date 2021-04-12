from flask import Flask, jsonify, request, make_response
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
from const import *

client = MongoClient("mongodb+srv://admin:admin@cluster0.kvxff.mongodb.net/io?retryWrites=true&w=majority")
db = client.io
app = Flask(__name__)

@app.route('/api/data/active_cases')
def infectionis():
    start = datetime.fromisoformat(request.args.get('start').replace("Z", ""))
    end = datetime.fromisoformat(request.args.get('end').replace("Z", ""))

    df = pd.DataFrame(db.covid.find_one({ 'name': INFECTIONS })['data'])
    df = df.rename(columns={'active_cases': 'value'})[['date', 'value']]
    df = df[start <= df.date]
    df = df[df.date <= end]
    response = make_response(df.to_json())
    response.mimetype = 'application/json'
    return response