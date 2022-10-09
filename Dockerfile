# base image  
FROM python:3.7.9    
ADD . /code
# where your code lives 
WORKDIR /code
# run this command to install all dependencies  
RUN pip install -r requirements.txt
# run this command to start the app 
CMD python app.py