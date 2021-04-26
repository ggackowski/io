from flask import Flask, jsonify, request, make_response
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
from const import *
import json

client = MongoClient("mongodb+srv://admin:admin@cluster0.kvxff.mongodb.net/io?retryWrites=true&w=majority")
db = client.io
app = Flask(__name__)

@app.route('/api/data/active_cases')
def get_infectionis():
    start = datetime.fromisoformat(request.args.get('start').replace("Z", ""))
    end = datetime.fromisoformat(request.args.get('end').replace("Z", ""))

    df = pd.DataFrame(db.covid.find_one({ 'name': INFECTIONS })['data'])
    df = df.rename(columns={'active_cases': 'value'})[['date', 'value']]
    df = df[start <= df.date]
    df = df[df.date <= end]
    response = make_response(df.to_json())
    response.mimetype = 'application/json'
    return response

@app.route('/api/data/hashtags')
def get_hashtags():
    return jsonify(hashtags, ensure_ascii=False)

@app.route('/api/data/tweets/count')
def get_tweets():
    start = datetime.fromisoformat(request.args.get('start').replace("Z", ""))
    end = datetime.fromisoformat(request.args.get('end').replace("Z", ""))

    df = pd.DataFrame(db.tweets.aggregate([
        { "$match" : { "date" : { "$gte": start, "$lt": end } } },
        { "$group": { "_id": "$date", "count": { "$sum": 1 } } }
    ]))

    return jsonify({
        'date': list(df['_id']),
        'values': list(df['count'])
    })


hashtags = []
with open('./twint_criteria.json') as file:
    twint_criteria = json.load(file)
    hashtags = [criteria['hashtag'] for criteria in twint_criteria if 'hashtag' in criteria]
