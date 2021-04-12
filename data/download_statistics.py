from lxml import html

import json
import requests

URL = "https://koronawirusunas.pl/"
DATA_SOURCE_KEYWORD = "dataSource"

def set_value_type(val: str):
    try:
        return int(val)
    except ValueError:
        pass

    try:
        return float(val)
    except ValueError:
        pass

    return val.replace('"', '')

def recur_tree(node, buffer, tag):
    for child in node:
        if(child.tag == tag):
            buffer.append(child)
        recur_tree(child, buffer, tag)

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
    parsed = html.fromstring(source)
    buffer = []
    recur_tree(parsed, buffer, 'script')
    scripts = [script.text_content() for script in buffer if keyword in script.text_content()]

    assert len(scripts) == 1, "Variables containing essential data have been either renamed or removed. Check page HTML source."

    variable_dict = parse_script_body(scripts[0])
    return variable_dict

def handle_variable(name, variable_dict):
    var = variable_dict[name]
    var = ''.join([char for char in list(var) if char not in '[]{; '])
    var = [s for s in var.split("},") if len(s) > 0]

    with open(name + '.json', 'w+') as j:
        json_entity_list = []
        for entity in var:
            json_entity = {}
            for key_val_pair in entity.split(','):
                key_val_pair = key_val_pair.split(':')
                if len(key_val_pair) > 1:
                    key, val = key_val_pair
                    json_entity[key] = set_value_type(val)
            json_entity_list.append(json_entity)
        json.dump(json_entity_list, j)

if __name__ == '__main__':

    source = requests.get(URL).content
    variable_dict = parse_source(source, DATA_SOURCE_KEYWORD)
        
    for key in variable_dict:
        handle_variable(key, variable_dict)