import twint
import logging
from pymongo import MongoClient

logging.basicConfig(level=logging.WARN)
client = MongoClient("mongodb+srv://admin:admin@cluster0.kvxff.mongodb.net/io?retryWrites=true&w=majority")
db = client.io

twint_criteria_dummy = [
    {"dateFrom": "2021-04-19", "dateTo": "2021-04-19", "hashtag": "SzczepimySie"},
    {"dateFrom": "2021-04-19", "dateTo": "2021-04-19", "hashtag": "KoronawirusWPolsce"},
]

twint_criteria = [
    {
        "hashtag": "lockdown"
    },
    {
        "hashtag": "coronavirus"
    },
    {
        "hashtag": "koronawirus"
    },
    {
        "hashtag": "COVID-19"
    },
    {
        "hashtag": "pandemia"
    },
    {
        "hashtag": "kwarantanna"
    },
    {
        "hashtag": "szzcepienia"
    },
    {
        "hashtag": "szczepienie"
    },
    {
        "hashtag": "obostrzenia"
    },
    {
        "hashtag": "SzczepimySię"
    },
    {
        "hashtag": "KoronawirusWPolsce"
    },
    {
        "hashtag": "MaskujSię"
    },
    {
    },
    {
    },
]


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
            config.Since = criteria["dateTo"]


def download_tweets(criteria_dict):
    for criteria in criteria_dict:
        c = twint.Config()

        @c.onTweet
        def onTweet(tweet):
            obj = {
                'username': tweet.username,
                'hashtags': tweet.hashtags,
                'likes_count': tweet.likes_count,
                'replies_count': tweet.replies_count,
                'retweets_count': tweet.retweets_count,
                'date': tweet.datetime,
            }
            db.tweets.update_one(obj, {"$set": obj}, True)

        apply_twint_criteria(c, criteria)
        # Example date: 2017-12-27
        # not retweets?
        twint.run.Search(c)


if __name__ == '__main__':
    download_tweets(twint_criteria_dummy)

    # add to DB; index by Tweet ID to avoid repeats
    # remove tweeets.json
