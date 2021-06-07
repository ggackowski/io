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
    "cases": "dataSource_przyrost",
    "life_saving_kit": "respiratoryData"
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
            return {'correlation': result[0], 'p_value': result[1]}
        return {'correlation': result.correlation, 'p_value': result.pvalue}
    except ValueError:
        return None

def get_correlation_for_matrix(data1, data2, correlation, idx1, idx2):
    try:
        result = CORRELATION_MAPPING[correlation](data1, data2)

        if isinstance(result, tuple):
            result =  {'correlation': result[0], 'p_value': result[1]}
        else: 
            result =  {'correlation': result.correlation, 'p_value': result.pvalue}

        if np.nan in list(result.values()) and idx1 == idx2:
            result = {'correlation': 1.0, 'p_value': 0.0}
        elif np.nan in list(result.values()):
            result = None
        return result

    except ValueError:
        return None

def correlation_matrix(start_date: str, end_date: str, correlation: str) -> Dict[str, List[any]]:
    idx_map = list(COLLECTION_MAPPING.keys())
    data = [get_data_for_range(start_date, end_date, statistic) for statistic in idx_map]
    mat = [[get_correlation_for_matrix(data1, data2, correlation, idx1, idx2) 
        for idx2, data2 in enumerate(data)] 
        for idx1, data1 in enumerate(data)]

    return {"index_mapping": idx_map, "correlation_matrix": mat}
