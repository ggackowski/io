import json
import twint
import logging
import sys
import datetime
from pymongo import MongoClient
from datetime import datetime, timedelta

logging.basicConfig(level=logging.WARN)
client = MongoClient("mongodb+srv://admin:admin@cluster0.kvxff.mongodb.net/io?retryWrites=true&w=majority")
db = client.io


def apply_twint_criteria(config, criteria):
    config.Lang = "pl"
    config.Store_json = True
    config.Output = "tweets.json"

    if criteria:
        config.Search = ""
        if "hashtags" in criteria:
            for hashtag in criteria["hashtags"]:
                config.Search += "\"#" + hashtag + "\""

        if "hashtag" in criteria:
            config.Search += "\"#" + criteria["hashtag"] + "\""

        if "username" in criteria:
            config.Username = criteria["username"]

        if "keywords" in criteria:
            for keyword in criteria["keywords"]:
                config.Search += "\"" + keyword + "\""

        if "keyword" in criteria:
            config.Search += "\"" + criteria["keyword"] + "\""

        if "dateFrom" in criteria:
            config.Since = criteria["dateFrom"]

        if "dateTo" in criteria:
            config.Until = criteria["dateTo"]


def date_to_twint_string(date):
    return str(date)[:10]


def download_tweets_until(date, criteria=None):
    if criteria is None:
        criteria = {}
    else:
        criteria = {"criteria": criteria}

    search_res = db.tweetsCriteriaStatus.find(criteria)
    for criteriaStatus in search_res:
        if "dateTo" in criteriaStatus:
            date = max(date, criteriaStatus["dateTo"])
        if "downloadedFrom" in criteriaStatus:
            while criteriaStatus["downloadedFrom"] > criteriaStatus["dateFrom"]:
                download_daily_tweets(criteriaStatus["downloadedFrom"] - timedelta(days=1), criteriaStatus)
            while criteriaStatus["downloadedTo"] < date:
                download_daily_tweets(criteriaStatus["downloadedTo"] + timedelta(days=1), criteriaStatus)
        else:
            date_to_download = criteriaStatus["dateFrom"]
            while date_to_download <= date:
                download_daily_tweets(date_to_download, criteriaStatus)


def download_daily_tweets(date, criteria=None):
    dateFrom = criteria["dateFrom"]
    if "dateTo" in criteria:
        dateTo = criteria["dateTo"]
    else:
        dateTo = None

    if "downloadedTo" in criteria:
        downloadedTo = criteria["downloadedTo"]
    else:
        downloadedTo = None

    if "downloadedFrom" in criteria:
        downloadedFrom = criteria["downloadedFrom"]
    else:
        downloadedFrom = None

    if date >= dateFrom and (dateTo is None or date <= dateTo) and ( (downloadedFrom is None or date < downloadedFrom) or (downloadedTo is None or date > downloadedTo) ):
        c = twint.Config()

        @c.onTweet
        def onTweet(tweet):
            obj = {
                'tweetid': tweet.id,
                'username': tweet.username,
                'hashtags': tweet.hashtags,
                'likes_count': tweet.likes_count,
                'replies_count': tweet.replies_count,
                'retweets_count': tweet.retweets_count,
                'date': datetime.fromisoformat(tweet.datetime.split(" ")[0]),
            }
            db.tweets.update_one({ "tweetid": tweet.id }, {"$set": obj}, True)

        apply_twint_criteria(c, criteria["criteria"])
        # Example date format: "2017-12-27"
        c.Since = date_to_twint_string(date)
        c.Until = date_to_twint_string(date + timedelta(days=1))
        twint.run.Search(c)
        if "downloadedFrom" in criteria:
            criteria["downloadedFrom"] = min(criteria["downloadedFrom"], date)
        else:
            criteria["downloadedFrom"] = date

        if "downloadedTo" in criteria:
            criteria["downloadedTo"] = max(criteria["downloadedTo"], date)
        else:
            criteria["downloadedTo"] = date
        db.tweetsCriteriaStatus.update_one({"criteria": criteria["criteria"]}, {"$set": criteria}, True)


if __name__ == '__main__':
    # specify end date as arguments: [filename] year month day
    # otherwise download until yesterday
    if len(sys.argv) >= 3:
        year = int(sys.argv[1])
        month = int(sys.argv[2])
        day = int(sys.argv[3])
        date = datetime(year, month, day)
    else:
        date = datetime.today() - timedelta(days=1)
    download_tweets_until(date)
