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
            { 'displayName': 'Active cases', 'type': 'bar', 'value': list(df['active_cases']) },
            { 'displayName': 'Running average', 'type': 'line', 'value': list(moving_average(df['active_cases'], avg)) },
            { 'displayName': 'Daily difference', 'type': 'bar', 'value': [0] + list(np.array(df['active_cases'])[1:] - np.array(df['active_cases'])[:-1]) },
        ],
        'stats': [
            { 'displayName': 'Mean', 'value': int(np.mean(df['active_cases'])) },
            { 'displayName': 'Min', 'value': int(np.min(df['active_cases'])) },
            { 'displayName': 'Max', 'value': int(np.max(df['active_cases'])) },
            { 'displayName': 'Std', 'value': int(np.std(df['active_cases'])) },
        ]
    })

@app.route('/api/data/deaths', methods=['POST'])
def get_infectionis():
    start = datetime.fromisoformat(request.json['start'].replace("Z", ""))
    end = datetime.fromisoformat(request.json['end'].replace("Z", ""))
    avg = int(request.json.get('avg', 3))

    df = pd.DataFrame(db.populationData.find({ "date": { "$gte": start, "$lte": end } }))

    return jsonify({
        'date': list(df['date']),
        'values': [
            { 'displayName': 'Deaths', 'type': 'bar', 'value': list(df['deaths']) },
            { 'displayName': 'Running average', 'type': 'line', 'value': list(moving_average(df['deaths'], avg)) },
            { 'displayName': 'Daily difference', 'type': 'bar', 'value': [0] + list(np.array(df['deaths'])[1:] - np.array(df['deaths'])[:-1]) },
        ],
        'stats': [
            { 'displayName': 'Mean', 'value': int(np.mean(df['deaths'])) },
            { 'displayName': 'Min', 'value': int(np.min(df['deaths'])) },
            { 'displayName': 'Max', 'value': int(np.max(df['deaths'])) },
            { 'displayName': 'Std', 'value': int(np.std(df['deaths'])) },
        ]
    })

@app.route('/api/data/quarantine', methods=['POST'])
def get_infectionis():
    start = datetime.fromisoformat(request.json['start'].replace("Z", ""))
    end = datetime.fromisoformat(request.json['end'].replace("Z", ""))
    avg = int(request.json.get('avg', 3))

    df = pd.DataFrame(db.dataSource_hospitalizacja.find({ "date": { "$gte": start, "$lte": end } }))

    return jsonify({
        'date': list(df['date']),
        'values': [
            { 'displayName': 'Quarantained', 'type': 'bar', 'value': list(df['quarantained']) },
            { 'displayName': 'Running average', 'type': 'line', 'value': list(moving_average(df['quarantained'], avg)) },
            { 'displayName': 'Daily difference', 'type': 'bar', 'value': [0] + list(np.array(df['quarantained'])[1:] - np.array(df['quarantained'])[:-1]) },
        ],
        'stats': [
            { 'displayName': 'Mean', 'value': int(np.mean(df['quarantained'])) },
            { 'displayName': 'Min', 'value': int(np.min(df['quarantained'])) },
            { 'displayName': 'Max', 'value': int(np.max(df['quarantained'])) },
            { 'displayName': 'Std', 'value': int(np.std(df['quarantained'])) },
        ]
    })

@app.route('/api/data/intense', methods=['POST'])
def get_infectionis():
    start = datetime.fromisoformat(request.json['start'].replace("Z", ""))
    end = datetime.fromisoformat(request.json['end'].replace("Z", ""))
    avg = int(request.json.get('avg', 3))

    df = pd.DataFrame(db.respiratoryData.find({ "date": { "$gte": start, "$lte": end } }))

    return jsonify({
        'date': list(df['date']),
        'values': [
            { 'displayName': 'Intense therapy', 'type': 'bar', 'value': list(df['used_life_saving_kit']) },
            { 'displayName': 'Running average', 'type': 'line', 'value': list(moving_average(df['used_life_saving_kit'], avg)) },
            { 'displayName': 'Daily difference', 'type': 'bar', 'value': [0] + list(np.array(df['used_life_saving_kit'])[1:] - np.array(df['used_life_saving_kit'])[:-1]) },
        ],
        'stats': [
            { 'displayName': 'Mean', 'value': int(np.mean(df['used_life_saving_kit'])) },
            { 'displayName': 'Min', 'value': int(np.min(df['used_life_saving_kit'])) },
            { 'displayName': 'Max', 'value': int(np.max(df['used_life_saving_kit'])) },
            { 'displayName': 'Std', 'value': int(np.std(df['used_life_saving_kit'])) },
        ]
    })

@app.route('/api/data/vaccinated', methods=['POST'])
def get_infectionis():
    start = datetime.fromisoformat(request.json['start'].replace("Z", ""))
    end = datetime.fromisoformat(request.json['end'].replace("Z", ""))
    avg = int(request.json.get('avg', 3))

    df = pd.DataFrame(db.dataSource_szczepienia.find({ "date": { "$gte": start, "$lte": end } }))

    return jsonify({
        'date': list(df['date']),
        'values': [
            { 'displayName': 'Vaccinated', 'type': 'bar', 'value': list(df['vaccinated']) },
            { 'displayName': 'Running average', 'type': 'line', 'value': list(moving_average(df['vaccinated'], avg)) },
            { 'displayName': 'Daily difference', 'type': 'bar', 'value': [0] + list(np.array(df['vaccinated'])[1:] - np.array(df['vaccinated'])[:-1]) },
        ],
        'stats': [
            { 'displayName': 'Mean', 'value': int(np.mean(df['vaccinated'])) },
            { 'displayName': 'Min', 'value': int(np.min(df['vaccinated'])) },
            { 'displayName': 'Max', 'value': int(np.max(df['vaccinated'])) },
            { 'displayName': 'Std', 'value': int(np.std(df['vaccinated'])) },
        ]
    })

@app.route('/api/data/cured', methods=['POST'])
def get_infectionis():
    start = datetime.fromisoformat(request.json['start'].replace("Z", ""))
    end = datetime.fromisoformat(request.json['end'].replace("Z", ""))
    avg = int(request.json.get('avg', 3))

    df = pd.DataFrame(db.populationData.find({ "date": { "$gte": start, "$lte": end } }))

    return jsonify({
        'date': list(df['date']),
        'values': [
            { 'displayName': 'Cured', 'type': 'bar', 'value': list(df['cured']) },
            { 'displayName': 'Running average', 'type': 'line', 'value': list(moving_average(df['cured'], avg)) },
            { 'displayName': 'Daily difference', 'type': 'bar', 'value': [0] + list(np.array(df['cured'])[1:] - np.array(df['cured'])[:-1]) },
        ],
        'stats': [
            { 'displayName': 'Mean', 'value': int(np.mean(df['cured'])) },
            { 'displayName': 'Min', 'value': int(np.min(df['cured'])) },
            { 'displayName': 'Max', 'value': int(np.max(df['cured'])) },
            { 'displayName': 'Std', 'value': int(np.std(df['cured'])) },
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
            { 'displayName': 'Tweet count', 'type': 'bar', 'value': list(df['count']) },
            { 'displayName': 'Running average', 'type': 'line', 'value': list(moving_average(df['count'], avg)) },
            { 'displayName': 'Daily difference', 'type': 'bar', 'value': [0] + list(map(int, np.array(df['count'])[1:] - np.array(df['count'])[:-1])) }
        ],
        'stats': [
            { 'displayName': 'Mean', 'value': int(np.mean(df['count'])) },
            { 'displayName': 'Min', 'value': int(np.min(df['count'])) },
            { 'displayName': 'Max', 'value': int(np.max(df['count'])) },
            { 'displayName': 'Std', 'value': int(np.std(df['count'])) },
        ]
    })

hashtags = []
with open('./twint_criteria.json') as file:
    twint_criteria = json.load(file)
    hashtags = [criteria['hashtag'] for criteria in twint_criteria if 'hashtag' in criteria]
