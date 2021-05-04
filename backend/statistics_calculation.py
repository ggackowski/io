from datetime import datetime
from pymongo import MongoClient
from typing import List, Union, Callable, Dict
import numpy as np

client = MongoClient("mongodb+srv://admin:admin@cluster0.kvxff.mongodb.net/io?retryWrites=true&w=majority")
db = client.io

COLLECTION_MAPPING = {
    "active_cases": "populationData",
    "deaths": "populationData",
    "cured": "populationData",
}


STATISTIC_MAPPING: Dict[str, Callable[[List[Union[int, float]]], any]]= {
    "mean": np.mean,
    "standard_deviation": np.std
}


def str_to_date(date: str):
    return datetime.strptime(date, '%d.%m.%Y')


def get_data_for_range(start_date, end_date, data_type: str) -> List[Union[int, float]]:
    start_date, end_date = str_to_date(start_date), str_to_date(end_date)
    data = db[COLLECTION_MAPPING[data_type]].find({"date" : {"$gte": start_date, "$lte": end_date}}, {data_type : 1})
    return [doc[data_type] for doc in data]


def get_statistics_for_range(start_date: str, end_date: str, data_type: str, statistic: str) -> any:
    return STATISTIC_MAPPING[statistic](get_data_for_range(start_date, end_date, data_type))


print(get_statistics_for_range("04.03.2020", "07.03.2020", "active_cases", "standard_deviation"))
