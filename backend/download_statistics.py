from lxml import html
from collections import defaultdict
from datetime import datetime
from pymongo import MongoClient

import requests


client = MongoClient("mongodb+srv://admin:admin@cluster0.kvxff.mongodb.net/io?retryWrites=true&w=majority")
db = client.io

URL = "https://koronawirusunas.pl/"
DATA_SOURCE_KEYWORD = "dataSource"

VAR_NAME_MAPPING = {
    'country': 'date',
    'chor': 'active_cases',
    'wyl': 'cured',
    'zgo': 'deaths',
    'zar': 'cases',
    'arg': 'date',
    'p_chorzy': 'active_cases',
    'p_wyleczeni': 'cured',
    'p_zgony': 'deaths',
    'liczba': 'number', 
    'wojewodztwo': 'voivodeship',
    'kwar': 'quarantained',
    'nadzor': 'under_probation',
    'dzien': 'date',
    'kwar_z': 'quarantained_and_infected',
    'respiratory': 'life_saving_kit',
    'l_respiratory': 'used_life_saving_kit'
}


def set_value_type(val: str): 
    try:
        return datetime.strptime(val.replace('"', ''), '%d.%m.%Y')
    except ValueError:
        pass

    try:
        return float(val)
    except ValueError:
        pass

    return val.replace('"', '') if val != "null" else None


def map_variable_name(name):
    return VAR_NAME_MAPPING.get(name, name)


def parse_script_body(script):
    variables = script.split('var')
    variable_dict = {}

    for var in variables:
        if '=' in var and '[' in var:
            name, data = var.split('=')
            name = ''.join([char for char in list(name) if char not in ' \n\t\r;'])
            data = ''.join([char for char in list(data) if char not in ' \n\t\r;'])
            variable_dict[name] = data
    return variable_dict


def parse_source(source, keyword):
    xml = html.fromstring(source)
    scripts = [
        script for script in xml.xpath('//script/text()')
        if DATA_SOURCE_KEYWORD in script
    ]

    assert len(scripts) == 1, "Variables containing essential data have been either renamed or removed. Check page HTML source."

    variable_dict = parse_script_body(scripts[0])
    return variable_dict


def handle_variable(name, variable_dict):
    var = variable_dict[name]
    var = ''.join([char for char in list(var) if char not in '[]{; '])
    var = [s for s in var.split("},") if len(s) > 0]
    entity_dict = defaultdict(list)
    for entity in var:
        for kv_pair in [kv.split(':') for kv in entity.split(',')]:
            if len(kv_pair) > 1:
                key, value = map_variable_name(kv_pair[0]), set_value_type(kv_pair[1])
                entity_dict[key].append(value)
    db.covid.update_one({ 'name': name }, { '$set' : { 'name': name, 'data': entity_dict } }, upsert=True)


if __name__ == '__main__':

    source = requests.get(URL).content
    variable_dict = parse_source(source, DATA_SOURCE_KEYWORD)
        
    for key in variable_dict:
        handle_variable(key, variable_dict)