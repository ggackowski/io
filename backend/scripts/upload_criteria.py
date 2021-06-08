# adds twint criteria from file passed as parameter

import json
import logging
import sys
from pymongo import MongoClient
from datetime import datetime

logging.basicConfig(level=logging.WARN)
client = MongoClient("mongodb+srv://admin:admin@cluster0.kvxff.mongodb.net/io?retryWrites=true&w=majority")
db = client.io


def upload_criteria(criteria_dict):
    for criteria in criteria_dict:
        print(criteria)
        update = {"criteria": criteria}
        if "dateFrom" in criteria:
            update["dateFrom"] = datetime.fromisoformat(criteria["dateFrom"])
        else:
            update["dateFrom"] = datetime.fromisoformat("2020-03-01")
        db.tweetsCriteriaStatus.update_one({ "criteria": criteria }, {"$set": update}, True)


with open(sys.argv[1], "r", encoding="utf-8") as file:
    twint_criteria = json.load(file)
    upload_criteria(twint_criteria)

