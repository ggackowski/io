from datetime import datetime
from pymongo import MongoClient
from typing import List, Union, Callable, Dict
import numpy as np

client = MongoClient("mongodb+srv://admin:admin@cluster0.kvxff.mongodb.net/io?retryWrites=true&w=majority")
db = client.io

COLLECTION_MAPPING: Dict[str, str] = {
    "active_cases": "populationData",
    "deaths": "populationData",
    "cured": "populationData",
    "under_probation": "dataSource_hospitalizacja",
    "used_life_saving_kit": "respiratoryData",
    "d_szczepienia": "dataSource_szczepienia",
    "szczepienia": "dataSource_szczepienia",
}


STATISTIC_MAPPING: Dict[str, Callable[[List[Union[int, float]]], any]] = {
    "mean": np.mean,
    "standard_deviation": np.std,
    "minimal value": np.min,
    "maximal value": np.max,
}


def str_to_date(date: str):
    return datetime.strptime(date, '%d.%m.%Y')


def get_data_for_range(start_date, end_date, data_type: str) -> List[Union[int, float]]:
    start_date, end_date = str_to_date(start_date), str_to_date(end_date)
    data = db[COLLECTION_MAPPING[data_type]].find({"date" : {"$gte": start_date, "$lte": end_date}}, {data_type : 1})
    return [doc[data_type] for doc in data if doc[data_type] is not None]


def get_statistics_for_range(start_date: str, end_date: str, data_type: str, statistic: str) -> any:
    try:
        return STATISTIC_MAPPING[statistic](get_data_for_range(start_date, end_date, data_type))
    except ValueError:
        return None


print(get_statistics_for_range("04.03.2020", "04.05.2020", "deaths", "mean"))
