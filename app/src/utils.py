import json

def get_error_code(name):
    error_codes=json.load(open('app/json/error_codes.json', 'r'))
    return error_codes.get(name)