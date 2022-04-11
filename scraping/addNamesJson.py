import json 
import re 

def openJSON():
    file = open('src/data.json')
    data = json.load(file)
    return data


def addNames():
    data = openJSON()
    for sen in data:
        rename = sen.replace('_', " ")
        data[sen]['full_name'] = rename
    return data

    

result = addNames()

with open('addedNames.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
