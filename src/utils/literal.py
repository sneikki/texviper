import json

with open('src/utils/literals.json', 'r') as literals_file:
    literals = json.load(literals_file)

def get_literal(name):
    return literals[name]
