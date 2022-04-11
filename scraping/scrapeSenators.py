from xxlimited import new
import requests
from bs4 import BeautifulSoup
import joblib
import json
import csv

def getSenatorObject():
    response = requests.get(url="https://en.wikipedia.org/wiki/List_of_current_United_States_senators")
    soup = BeautifulSoup(response.content, 'html.parser')

    senator_list = []
    span_list = soup.find_all('span', {'class': 'fn'})
    for sen in span_list:
        link = sen.find('a').get('href')
        senator_list.append(link)

    senator_list = senator_list[-100:]
    
    wiki = 'https://en.wikipedia.org'
    senator_link_list = [wiki + sen for sen in senator_list]

    senator_obj = {}
    twitter_handles = processingHandles()

    for i in range(len(senator_link_list)):
        if i % 10 == 0:
            print(f'Scraped {i} senators so far ...\n')

        key = senator_link_list[i].split("wiki/", 1)[1]
        wiki_html = callWikiAPI(key)
        location_list = scrapeCapitolInfo()

        value_obj = {
            'handle': twitter_handles[i],
            'state': location_list[i][0],
            'capital_city': location_list[i][1],
            'latitude': location_list[i][2],
            'longitude': location_list[i][3],
            'wiki_html': str(wiki_html),
        }
        senator_obj[key] = value_obj
    
    return senator_obj
        

def processingHandles():
    updated_handles = [
        'SenShelby', 'SenTuberville', 'lisamurkowski', 'SenDanSullivan', 'SenatorSinema', 'SenMarkKelly', 'JohnBoozman', 'SenTomCotton','SenFeinstein', 
        'AlexPadilla4CA', 'SenBennetCO', 'SenCoryGardner', 'SenBlumenthal', 'ChrisMurphyCT', 'SenatorCarper', 'ChrisCoons', 'marcorubio', 'SenBillNelson', 
        'SenDavidPerdue', 'SenatorIsakson', 'brianschatz', 'maziehirono', 'MikeCrapo', 'SenatorRisch', 'SenatorDurbin', 'SenDuckworth', 'SenToddYoung', 
        'SenDonnelly', 'ChuckGrassley', 'joniernst', 'JerryMoran', 'SenPatRoberts', 'LeaderMcConnell', 'RandPaul', 'BillCassidy', 'SenJohnKennedy', 
        'SenatorCollins', 'SenAngusKing', 'SenatorCardin', 'ChrisVanHollen', 'SenWarren', 'senmarkey', 'SenStabenow','SenGaryPeters', 'amyklobuchar', 
        'SenTinaSmith', 'SenatorWicker', 'SenHydeSmith', 'RoyBlunt', 'clairecmc', 'SenatorTester', 'SteveDaines', 'SenatorFischer', 'BenSasse', 
        'SenCortezMasto', 'SenDeanHeller', 'SenatorShaheen', 'SenatorHassan', 'SenatorMenendez', 'CoryBooker', 'MartinHeinrich', 'SenatorTomUdall', 
        'SenSchumer', 'SenGillibrand', 'SenatorBurr', 'SenThomTillis', 'SenJohnHoeven', 'SenatorHeitkamp', 'SenSherrodBrown', 'SenRobPortman', 
        'jiminhofe', 'SenatorLankford', 'RonWyden', 'SenJeffMerkley', 'SenBobCasey', 'SenToomey', 'SenJackReed', 'SenWhitehouse', 'GrahamBlog', 
        'SenatorTimScott', 'SenJohnThune', 'SenatorRounds', 'SenAlexander', 'BobCorker', 'JohnCornyn', 'SenTedCruz', 'SenMikeLee', 'SenOrrinHatch', 
        'SenatorLeahy', 'SenatorSanders', 'MarkWarner', 'timkaine', 'PattyMurray', 'SenatorCantwell', 'Sen_JoeManchin', 'SenCapito', 'SenRonJohnson',
        'SenatorBaldwin', 'SenJohnBarrasso', 'SenatorEnzi'
    ]
    return updated_handles


def callWikiAPI(senator_wiki):
    url = f"http://en.wikipedia.org/w/api.php?action=parse&format=json&prop=text&section=0&page={senator_wiki}&origin=*"
    response = requests.get(url)
    json_data = json.loads(response.text)
    soup = BeautifulSoup(json_data['parse']['text']['*'], 'html.parser') # 'html.parser'

    for a in soup.findAll('a'):
        a.replaceWithChildren()

    return soup.findAll('p')


def scrapeCapitolInfo():
    location_list = []
    with open('src/us-state-capitals.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            sub_list = []
            if line_count == 0:
                line_count += 1
            else:
                sub_list.extend([row[0], row[1], row[2], row[3]])
                location_list.append(sub_list)
                location_list.append(sub_list)
                line_count += 1
    
    return location_list
                

result = getSenatorObject()

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)