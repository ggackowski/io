from datetime import datetime
from pymongo import MongoClient
from typing import List, Union, Callable, Dict
from scipy.stats import *
import numpy as np

client = MongoClient("mongodb+srv://admin:admin@cluster0.kvxff.mongodb.net/io?retryWrites=true&w=majority")
db = client.io

COLLECTION_MAPPING: Dict[str, str] = {
    "active_cases": "populationData",
    "deaths": "populationData",
    "cured": "populationData",
    "under_probation": "dataSource_hospitalizacja",
    "used_life_saving_kit": "respiratoryData",
    "vaccinated": "dataSource_szczepienia",
    "total_vaccinated": "dataSource_szczepienia",
}


STATISTIC_MAPPING: Dict[str, Callable[[List[Union[int, float]]], any]] = {
    "mean": np.mean,
    "standard_deviation": np.std,
    "minimal_value": np.min,
    "maximal_value": np.max,
}

CORRELATION_MAPPING: Dict[str, Callable[[np.ndarray, np.ndarray], float]] = {
    "Kendall": kendalltau,
    "Pearson": pearsonr,
    "Spearman": spearmanr
}


def str_to_date(date: str):
    return datetime.fromisoformat(date.replace("Z", ""))


def get_data_for_range(start_date, end_date, data_type: str) -> List[Union[int, float]]:
    start_date, end_date = str_to_date(start_date), str_to_date(end_date)
    data = db[COLLECTION_MAPPING[data_type]].find({"date" : {"$gte": start_date, "$lte": end_date}}, {data_type : 1})
    return [doc[data_type] for doc in data if doc[data_type] is not None]


def get_statistics_for_range(start_date: str, end_date: str, data_type: str, statistic: str) -> any:
    try:
        return STATISTIC_MAPPING[statistic](get_data_for_range(start_date, end_date, data_type))
    except ValueError:
        return None


def get_correlation_for_range(
    start_date: str, end_date: str, data1: str, data2: str, correlation: str
    ) -> Dict[str, float]:
    
    try:
        
        result = CORRELATION_MAPPING[correlation](
            get_data_for_range(start_date, end_date, data1),
            get_data_for_range(start_date, end_date, data2)
        )

        if isinstance(result, tuple):
            return {'correlation': result[0], 'p-value': result[1]}
        return {'correlation': result.correlation, 'p-value': result.pvalue}

    except ValueError:
        return None
