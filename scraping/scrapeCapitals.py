import requests
from bs4 import BeautifulSoup
import json
import re


def getCapitalCityInfo():
    response = requests.get(url="https://en.wikipedia.org/wiki/List_of_capitals_in_the_United_States")
    soup = BeautifulSoup(response.content, 'html.parser')

    capital_list = []
    th_list = soup.find_all('th', {'scope': 'row'})
    for sen in th_list:
        try:
            link = sen.find('a').get('href')
            capital_list.append(link)
        except:
            pass

    capital_list = capital_list
    return capital_list


def callWikiAPI(capital):
    url = f"http://en.wikipedia.org/w/api.php?action=parse&format=json&prop=text&section=0&page={capital}&origin=*"
    response = requests.get(url)
    json_data = json.loads(response.text)
    soup = BeautifulSoup(json_data['parse']['text']['*'], 'html.parser') # 'html.parser'

    for a in soup.findAll('a'):
        a.replaceWithChildren()

    try:
        p_tags = soup.findAll('p')
        cleaned_p = p_tags[1].get_text(strip=False)
        return re.sub("[\(\[].*?[\)\]]", "", cleaned_p)
    except:
        return ""


def pullCapitalSummary():
    capital_list = getCapitalCityInfo()
    summary_list = []

    counter = 0
    for cap in capital_list:
        if counter % 5 == 0:
            print(f"Scraped {counter} capitals so far ...")
        cap = cap.split("wiki/", 1)[1]
        summary_list.append(callWikiAPI(cap))
        summary_list.append(callWikiAPI(cap))
        counter += 1
    
    return summary_list


def openJSON():
    file = open('src/data.json')
    data = json.load(file)
    return data


def updateJSON():
    data = openJSON()
    summaries = pullCapitalSummary()

    counter = 0
    for x in data:
        data[x]['capital_summary'] = summaries[counter]
        counter += 1

    return data
        

data_updated = updateJSON()
with open('data_updated.json', 'w', encoding='utf-8') as f:
    json.dump(data_updated, f, ensure_ascii=False, indent=4)



