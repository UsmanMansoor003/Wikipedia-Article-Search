from flask import Flask
import json
import requests
import re
import pymongo
import sys

app = Flask(__name__)
#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# article keyword to crawl from wikipedia
# Todo: article can be randomized or can be passed as users input through api endpoint.
article_keywords = ['Uber', 'Careem', 'Free_Now_(service)', 'omio','BlaBlaCar', 'FlixBus','RegioJet',
                    'Deutsche_Bahn', 'Ryanair', 'Eurowings']


# Wikipedia API endpoint
# Todo: can be made dynamic.
API_ENDPOINT = 'https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&rvsection=0&titles=%s&format=json'


# mongoDB configuration
#Todo : Host name can be passed as a environment variable. and can be defined in docker compose file.
myclient = pymongo.MongoClient(host='wikipedia-article-search-mongodb-1', port=27017)
mydb = myclient["wikipedia"]
mycol = mydb["articles"]

@app.route('/')
def hello():
    return "Hello World"

# Todo: can pass article name as api argument.
@app.route('/load')
def load():
    try:
        for article in article_keywords:
            # get content of each article as response from wikipedia API
            response = requests.get(API_ENDPOINT  %article)
            # prepare data JSON to insert in mongoDB
            # Todo: Response handling can be improved.
            # Todo: Json repsonse can be cleaned.  
            data = {"name" : article, "content" : response.text}
            # dump response in mongodb
            x = mycol.insert_one(data)
    except:
        app.logger.error("Oops! ", sys.exc_info()[0], " occurred.")
        return {"msg" : "Data is not loaded because " + str(sys.exc_info()[0]) + " occurred."}

    return {"msg" :"Wikipedia articles are loaded successfully in mongoDB"}

#Todo: we can create a get endpoint to get current list of stored article list.

#Todo: instead of fetching all the content from mongodb we can use mongodb text search query and fetch direct result from that.
        #which might be faster than this.
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

# todo: Test Cases
# Db connection test case
# db insert and fetch test
# wikipedia api endpoint test case (check response) (structure) (network error) (empty response) (article not found)
# search query test case


# todo 
# can create a user interface
# can add multiple try to connect to do in docker compose file.
# can create a more generic code so that we don't need to do change in the app. 

