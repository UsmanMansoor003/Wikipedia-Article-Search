# Wikipedia articles Search App
This project ties together Flask, Mongodb and Docker in a simple application. It load the wikipedia articles on the mongodb database and allow you to search word occurences in those articles while managing it all with docker-compose.

## How to Run
* make sure your system have Docker installed otherwise follow the instruction of setup and installation of docker from https://docs.docker.com/docker-for-windows/install/
* Also, make sure that you have docker-compose installed as well. 
* Open the command terminal 'cmd'.
* Move into the directory folder of the project where docker file, app.py is present.
* Run docker-compose up command to build mongodb and flask application images and run there respective container.
* Onces the containers are up and running. Go to the browser and go to http://127.0.0.1:5000/. You will see "Hello World" printed on the screen.
* In order to load data into database go to http://127.0.0.1:5000/load. This will load the 10 wikipedia articles into mongodb database.
* After loading the data into the databases. Search the word occurences using this link http://127.0.0.1:5000/search/{Word to Search}.


