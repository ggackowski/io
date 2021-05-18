from flask import Flask, jsonify, request, make_response
from pymongo import MongoClient
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import json

client = MongoClient("mongodb+srv://admin:admin@cluster0.kvxff.mongodb.net/io?retryWrites=true&w=majority")
db = client.io
app = Flask(__name__)

def moving_average(data_set, periods=3):
    weights = np.ones(periods) / periods
    return np.convolve(data_set, weights, mode='same')

def get_simpledata(req, collection, field):
    start = datetime.fromisoformat(req.json['start'].replace("Z", ""))
    end = datetime.fromisoformat(req.json['end'].replace("Z", ""))
    avg = int(req.json.get('avg', 3))

    df = pd.DataFrame(db[collection].find({"date": {"$gte": start, "$lte": end}}))
    data = df[field]

    return {
        'date': list(df['date']),
        'values': [
            { 'displayName': 'Active cases', 'type': 'bar', 'value': list(data) },
            { 'displayName': 'Running average', 'type': 'line', 'value': list(moving_average(data, avg)) },
            { 'displayName': 'Daily difference', 'type': 'bar', 'value': [0] + list(np.array(data)[1:] - np.array(data)[:-1]) },
        ],
        'stats': [
            { 'displayName': 'Mean', 'value': int(np.mean(data)) },
            { 'displayName': 'Min', 'value': int(np.min(data)) },
            { 'displayName': 'Max', 'value': int(np.max(data)) },
            { 'displayName': 'Std', 'value': int(np.std(data)) },
        ]
    }


@app.route('/api/data/active_cases', methods=['POST'])
def get_infectionis():
    return jsonify(get_simpledata(request, 'populationData', 'active_cases'))

@app.route('/api/data/deaths', methods=['POST'])
def get_deaths():
    return jsonify(get_simpledata(request, 'populationData', 'deaths'))

@app.route('/api/data/quarantine', methods=['POST'])
def get_quarantine():
    return jsonify(get_simpledata(request, 'dataSource_hospitalizacja', 'quarantained'))

@app.route('/api/data/intense', methods=['POST'])
def get_intense():
    return jsonify(get_simpledata(request, 'respiratoryData', 'used_life_saving_kit'))

@app.route('/api/data/vaccinated', methods=['POST'])
def get_vaccinated():
    return jsonify(get_simpledata(request, 'dataSource_szczepienia.', 'vaccinated'))

@app.route('/api/data/cured', methods=['POST'])
def get_cured():
    return jsonify(get_simpledata(request, 'populationData.', 'cured'))

@app.route('/api/data/hashtags')
def get_hashtags():
    return jsonify(hashtags)

@app.route('/api/data/tweets/count', methods=['POST'])
def get_tweets():
    start = datetime.fromisoformat(request.json['start'].replace("Z", ""))
    end = datetime.fromisoformat(request.json['end'].replace("Z", ""))
    avg = int(request.json.get('avg', 3))
    tags = request.json['tags']

    query = [
        {"$match": {"date" : {"$gte": start, "$lte": end}}},
    ]
    if tags:
        query += [
            {"$project": {"tags": {"$size": {"$setIntersection": ["$hashtags", tags] }}, "date": True}},
            {"$match": {"tags" : {"$ne": 0}}},
        ]
    query += [
        { "$group": { "_id": "$date", "count": { "$sum": 1 } } },
        { "$sort" : { "_id" : 1 } }
    ]
    df = pd.DataFrame(db.tweets.aggregate(query))
    data = df['count']

    return jsonify({
        'date': list(df['_id']),
        'values': [
            { 'displayName': 'Tweet count', 'type': 'bar', 'value': list(data) },
            { 'displayName': 'Running average', 'type': 'line', 'value': list(moving_average(data, avg)) },
            { 'displayName': 'Daily difference', 'type': 'bar', 'value': [0] + list(map(int, np.array(data)[1:] - np.array(data)[:-1])) }
        ],
        'stats': [
            { 'displayName': 'Mean', 'value': int(np.mean(data)) },
            { 'displayName': 'Min', 'value': int(np.min(data)) },
            { 'displayName': 'Max', 'value': int(np.max(data)) },
            { 'displayName': 'Std', 'value': int(np.std(data)) },
        ]
    })

hashtags = []
with open('./twint_criteria.json') as file:
    twint_criteria = json.load(file)
    hashtags = [criteria['hashtag'] for criteria in twint_criteria if 'hashtag' in criteria]
