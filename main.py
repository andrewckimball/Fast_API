from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware    
import json
import bz2
import _pickle as cPickle


### uvicorn main:app --reload ###

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def decompress_pickle(file):
    data = bz2.BZ2File(file, 'rb')
    data = cPickle.load(data)
    return data

bayes_model = decompress_pickle('src/compressed.pbz2')

@app.get('/')
def root():
    return {'message': 'Hello World!'}


@app.get('/predict/{tweet}')
def runModel(tweet):
    # Run model on guess
    prediction = bayes_model.predict([tweet])[0]

    # Get json object matching predicted senator 
    key = returnSenator(prediction)
    return key


@app.get('/select/{senator}')
def selectSenator(senator):
    data = openJSON()
    if senator in data:
        return data[senator]
    else: 
        return {'Error, not found'}


def openJSON():
    file = open('src/data.json')
    data = json.load(file)
    return data
    

def returnSenator(senator):
    data = openJSON()
    key_list = list(data.keys())
    val_list = list(data.values())
    handle_tuple = [(k['handle']) for k in val_list]
    position = handle_tuple.index(senator)
    key = key_list[position]

    return data[key]


