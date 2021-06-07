from flask import Flask, jsonify, request, make_response
from pymongo import MongoClient
from datetime import datetime, timedelta
from statistics_calculation import get_correlation_for_range, correlation_matrix

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
    return jsonify(get_simpledata(request, 'dataSource_szczepienia', 'vaccinated'))

@app.route('/api/data/cured', methods=['POST'])
def get_cured():
    return jsonify(get_simpledata(request, 'populationData', 'cured'))

@app.route('/api/data/<first_statistic>/correlation', methods=['POST'])
def get_correlation(first_statistic):
    start_date = request.json['start']
    end_date = request.json['end']
    second_statistic = request.json['second']
    correlation = request.json['correlation']

    return jsonify(get_correlation_for_range(start_date, end_date, first_statistic, second_statistic, correlation))

@app.route('/api/data/hashtags')
def get_hashtags():
    return jsonify(hashtags)

@app.route('/api/data/correlation_matrix', methods=['POST'])
def get_correlation_matrix():
    start_date = request.json['start']
    end_date = request.json['end']
    correlation = request.json['correlation']

    return correlation_matrix(start_date, end_date, correlation)
    
@app.route('/api/data/tweets/count', methods=['POST'])
def get_tweets():
    start = datetime.fromisoformat(request.json['start'].replace("Z", ""))
    end = datetime.fromisoformat(request.json['end'].replace("Z", ""))
    avg = int(request.json.get('avg', 3))
    tags = request.json['tags']

    query = [{"$match": {"date" : {"$gte": start, "$lte": end}}}]
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

@app.route('/api/data/users/top', methods=['POST'])
def get_top_users():
    start = datetime.fromisoformat(request.json['start'].replace("Z", ""))
    end = datetime.fromisoformat(request.json['end'].replace("Z", ""))
    tags = request.json['tags']

    query = [{"$match" : {"date" : {"$gte": start, "$lte": end }}}]
    if tags:
        query += [
            {"$project": {"tags": {"$size": {"$setIntersection": ["$hashtags", tags] }}, "username": True, "likes_count": True, "replies_count": True, "retweets_count": True}},
            {"$match"  : {"tags" : {"$ne": 0}}},
        ]
    query += [
        {"$group" : {
            "_id": "$username", 
            "count": {"$sum": 1}, 
            "likes": {"$sum": "$likes_count"},
            "replies": {"$sum": "$replies_count"},
            "retweets": {"$sum": "$retweets_count"},
        }},
        {"$sort"   : {"count" : -1}},
        {"$limit": 20}
    ]

    df = pd.DataFrame(db.tweets.aggregate(query))

    return jsonify([
        { 
            'Username': data[0],
            'Count': data[1],
            'Likes': data[2],
            'Replies': data[3],
            'Retweets': data[4]
        } for data in zip(df['_id'], df['count'], df['likes'], df['replies'], df['retweets'])
    ])

@app.route('/api/data/tags/top', methods=['POST'])
def get_top_tags():
    start = datetime.fromisoformat(request.json['start'].replace("Z", ""))
    end = datetime.fromisoformat(request.json['end'].replace("Z", ""))
    tags = request.json['tags']

    query = [{"$match" : {"date" : {"$gte": start, "$lte": end }}}]
    if tags:
        query += [{"$project": {"tags": {"$setIntersection": ["$hashtags", tags] }}}]
    else:
        query += [{"$project": {"tags": "$hashtags" }}]

    query += [
        {"$unwind": "$tags" },
        {"$group" : {"_id": "$tags", "count": {"$sum": 1}} },
        {"$sort"  : {"count" : -1}}
    ]

    df = pd.DataFrame(db.tweets.aggregate(query))
    return jsonify({ 
        'username': list(df['_id']),
        'value': list(df['count'])
    })

hashtags = []
with open('./twint_criteria.json') as file:
    twint_criteria = json.load(file)
    hashtags = [criteria['hashtag'] for criteria in twint_criteria if 'hashtag' in criteria]
