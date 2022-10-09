from flask import Flask
import json
import requests
import re
import pymongo
import sys

app = Flask(__name__)
#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# article keyword to crawl from wikipedia
article_keywords = ['Uber', 'Careem', 'Free_Now_(service)', 'omio','BlaBlaCar', 'FlixBus','RegioJet',
                    'Deutsche_Bahn', 'Ryanair', 'Eurowings']


# Wikipedia API endpoint
API_ENDPOINT = 'https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&rvsection=0&titles=%s&format=json'


# mongoDB configuration
myclient = pymongo.MongoClient(host='wikipedia-article-search-mongodb-1', port=27017)
mydb = myclient["wikipedia"]
mycol = mydb["articles"]

@app.route('/')
def hello():
    return "Hello World"

@app.route('/load')
def load():
    try:
        for article in article_keywords:
            # get content of each article as response from wikipedia API
            response = requests.get(API_ENDPOINT  %article)
            # prepare data JSON to insert in mongoDB
            data = {"name" : article, "content" : response.text}
            # dump response in mongodb
            x = mycol.insert_one(data)
    except:
        app.logger.error("Oops! ", sys.exc_info()[0], " occurred.")
        return {"msg" : "Data is not loaded because " + str(sys.exc_info()[0]) + " occurred."}

    return {"msg" :"Wikipedia articles are loaded successfully in mongoDB"}

@app.route('/search/<name>')
def search(name):
    res = 0
    data = {}
    try:
        # get all documents from mongoDB
        x  = mycol.find()
        # iterate cursor of each mongoDB document
        for item in x:
            # the serach keyword 'name' can be found on each content of article using regular expression
            # and keep track of the count of each article in dictionary 'data'
            data[item['name']] = len(re.findall(name, item['content'], re.I | re.M))
        return data
    except:
        app.logger.error("Oops! ", sys.exc_info()[0], " occurred.")
        return {"msg" : "Not found because " + str(sys.exc_info()[0]) + " occurred."}

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)



