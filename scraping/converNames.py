import json 
import re 

def openJSON():
    file = open('src/data.json')
    data = json.load(file)
    return data


def returnNames():
    name_obj = []

    data = openJSON()
    counter = 0
    for sen in data:
        rename = sen.replace('_', " ")
        value_obj= {
            'id': counter,
            'key_name': sen,
            'rename': rename
        }
        name_obj.append(value_obj)
        counter += 1
    return name_obj

    

result = returnNames()

with open('nameSearchData.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
