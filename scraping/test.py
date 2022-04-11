import re 
import json


def openJSON():
    file = open('src/data.json')
    data = json.load(file)
    return data

def fixPTags():
    data = openJSON()
    for sen in data:
        replace = data[sen]['wiki_html']
        new = re.sub(r"(</p>,)", "</p>", replace)
        data[sen]['wiki_html'] = new
    return data
    


result = fixPTags()

with open('data_updated.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
# x = '</p>, <p><b>Richard Craig Shelby .... </p>, oooooo'
# new = re.sub(r"(</p>,)", "</p>", x)
# print(new)