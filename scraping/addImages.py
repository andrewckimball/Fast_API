import requests
import json


WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

def openJSON():
    file = open('src/data.json')
    data = json.load(file)
    return data


def get_wiki_image(senator):
    try:
        response  = requests.get(WIKI_REQUEST+senator)
        json_data = json.loads(response.text)
        img_link = list(json_data['query']['pages'].values())[0]['original']['source']
        return img_link        
    except:
        return 0

def addImageJSON():
    data = openJSON()
    counter = 0
    for sen in data:
        if counter % 10 == 0:
            print(f"Ran through {counter} so far ...")
        img = get_wiki_image(sen)
        data[sen]['img'] = img
        counter += 1
    return data

result = addImageJSON()

with open('addImages.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)