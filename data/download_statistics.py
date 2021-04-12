from lxml import html

import json
import requests

URL = "https://koronawirusunas.pl/"
DATA_SOURCE_KEYWORD = "dataSource"

def recur_tree(node, buffer, tag):
    for child in node:
        if(child.tag == tag):
            buffer.append(child)
        recur_tree(child, buffer, tag)

def parse_script_body(script):
    var_list = script.split('var')
    var_dict = {}

    for var in var_list:
        if '=' in var and '[' in var:
            name, data = var.split('=')
            name = ''.join([char for char in list(name) if char not in ' \n\t\r;'])
            data = ''.join([char for char in list(data) if char not in ' \n\t\r;'])
            var_dict[name] = data
    return var_dict

def parse_source(source, keyword):
    parsed = html.fromstring(source)
    script_buffer = []
    recur_tree(parsed, script_buffer, 'script')
    script_buffer = [script.text_content() for script in script_buffer if keyword in script.text_content()]

    assert len(script_buffer) == 1, "Variables containing essential data have been either renamed or removed. Check page HTML source"

    var_dict = parse_script_body(script_buffer[0])
    return var_dict

def handle_variable(name, var_dict):
    var = var_dict[name]
    var = ''.join([char for char in list(var) if char not in '[]{; '])
    var = [s for s in var.split("},") if len(s) > 0]

    with open(name + '.json', 'w+') as j:
        data = []
        for tup in var:
            d = {}
            for pair in tup.split(','):
                pair = pair.split(':')
                if len(pair) > 1:
                    d[pair[0]] = pair[1].replace('"', '')
            data.append(d)
        json.dump(data, j)

if __name__ == '__main__':

    source = requests.get(URL).content
    var_dict = parse_source(source, DATA_SOURCE_KEYWORD)
        
    for key in var_dict:
        handle_variable(key, var_dict)