from lxml import html

import requests
from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:admin@cluster0.kvxff.mongodb.net/io?retryWrites=true&w=majority")
db = client.io

URL = "https://koronawirusunas.pl/"
DATA_SOURCE_KEYWORD = "dataSource"

def set_value_type(val: str):
    if val == "null":
        return None
    try:
        return int(val)
    except ValueError:
        pass

    try:
        return float(val)
    except ValueError:
        pass

    return val.replace('"', '')

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

    json_entity_dict = {}
    for entity in var:
        for key_val_pair in entity.split(','):
            key_val_pair = key_val_pair.split(':')
            if len(key_val_pair) > 1:
                key, val = key_val_pair
                if key not in json_entity_dict:
                    json_entity_dict[key] = []
                json_entity_dict[key].append(set_value_type(val))
    db.covid.update_one({ 'name': name }, { '$set' : { 'name': name, 'data': json_entity_dict } }, upsert=True)


if __name__ == '__main__':

    source = requests.get(URL).content
    variable_dict = parse_source(source, DATA_SOURCE_KEYWORD)
        
    for key in variable_dict:
        handle_variable(key, variable_dict)