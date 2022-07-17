# AMCEF_Test

**Description:**    
This REST API is made to manage posts and work with fakeAPI Json Server

**Documentation for REST-API:**
>https://documenter.getpostman.com/view/22005674/UzQvsjcX

**Dependancies you will need to install:** <br>

Peewee:  
>$pip install peewee

Flask
>$pip install flask

Requests
>$pip install requests

Json Server
>$npm install -g json-server

**First Start:**    
Start JSON Server   
>$npm run json:server    

Start REST API
>$python REST_API.py    

Your REST API is going to be located on this adress:
>http://127.0.0.1:5000

Your fakeAPI JSON Server is going to be located on this adress:
>http://localhost:3000/



JSON Server takes data from 'db.json' so if you want to input some data
manually, you can here. 

When you run REST API data will be takem from JSON Server to ORM database
and on every restart of REST API, the database is gonna be deleted, then created
with updated data.

You can find list of requests and instructions to use them in API documentation.


