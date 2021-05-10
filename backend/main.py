from flask import Flask, jsonify, request, make_response
from pymongo import MongoClient
from datetime import datetime, timedelta
import pandas as pd
from const import *
import numpy as np
import json

client = MongoClient("mongodb+srv://admin:admin@cluster0.kvxff.mongodb.net/io?retryWrites=true&w=majority")
db = client.io
app = Flask(__name__)

def moving_average(data_set, periods=3):
    weights = np.ones(periods) / periods
    return np.convolve(data_set, weights, mode='valid')

@app.route('/api/data/active_cases', methods=['POST'])
def get_infectionis():
    start = datetime.fromisoformat(request.json['start'].replace("Z", ""))
    end = datetime.fromisoformat(request.json['end'].replace("Z", ""))
    avg = int(request.json.get('avg', 3))

    df = pd.DataFrame(db.populationData.find({ "date": { "$gte": start, "$lte": end } }))

    return jsonify({
        'date': list(df['date']),
        'values': [
            { 'displayname': 'Active cases', 'type': 'bar', 'value': list(df['active_cases']) },
            { 'displayname': 'Running average', 'type': 'line', 'value': list(moving_average(df['active_cases'], avg)) },
            { 'displayname': 'Daily difference', 'type': 'bar', 'value': [0] + list(np.array(df['active_cases'])[1:] - np.array(df['active_cases'])[:-1]) },
        ]
    })

@app.route('/api/data/hashtags')
def get_hashtags():
    return jsonify(hashtags)

@app.route('/api/data/tweets/count', methods=['POST'])
def get_tweets():
    start = datetime.fromisoformat(request.json['start'].replace("Z", ""))
    end = datetime.fromisoformat(request.json['end'].replace("Z", ""))
    avg = int(request.json.get('avg', 3))
    tags = request.json['tags']

    if tags:
        df = pd.DataFrame(db.tweets.aggregate([
            { "$match" : { "date" : { "$gte": start, "$lte": end } } },
            { "$project": { "tags": {"$size": {"$setIntersection": ["$hashtags", hashtags] }}, "date": True}},
            { "$match" : { "tags" : { "$ne": 0 } } },
            { "$group": { "_id": "$date", "count": { "$sum": 1 } } },
            { "$sort" : { "_id" : 1 } }
        ]))
    else:
        df = pd.DataFrame(db.tweets.aggregate([
            { "$match" : { "date" : { "$gte": start, "$lte": end } } },
            { "$group": { "_id": "$date", "count": { "$sum": 1 } } },
            { "$sort" : { "_id" : 1 } }
        ]))

    return jsonify({
        'date': list(df['_id']),
        'values': [
            { 'displayname': 'Tweet count', 'type': 'bar', 'value': list(df['count']) },
            { 'displayname': 'Running average', 'type': 'line', 'value': list(moving_average(df['count'], avg)) },
            { 'displayname': 'Daily difference', 'type': 'bar', 'value': [0] + list(np.array(df['count'])[1:] - np.array(df['count'])[:-1]) },
        ]
    })

hashtags = []
with open('./twint_criteria.json') as file:
    twint_criteria = json.load(file)
    hashtags = [criteria['hashtag'] for criteria in twint_criteria if 'hashtag' in criteria]
