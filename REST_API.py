import requests
import json
from flask import Flask, request, render_template
from flask_restful import  Api
from flask.views import MethodView
from peewee import SqliteDatabase, Model, TextField, IntegerField
import os

#Resetting ORM database
if os.path.exists('posts.db'):
    os.remove('posts.db')

app = Flask(__name__)
api = Api(app)

base_url = 'http://localhost:3000/'

posts_endpoint = 'posts'

#Creating ORM database
db = SqliteDatabase('posts.db')

class BaseTable(Model):
    class Meta:
        database = db

#Model for post
class Post(BaseTable):
    id = IntegerField(primary_key=True, index=True)
    userId = IntegerField()
    title= TextField()
    body= TextField()

#Connecting to database
db.connect()
db.create_tables([Post])

#Error messages
Error_Wrong_ID_Int = "Wrong ID input. ID has to be integer."
Error_Wrong_Data_Str = "Wrong data input. Data have to be string."
Error_Data_Missing = "Some data you want to input are missing. Please check again."
Error_Post_Not_Found = "Post with this ID could not be found."
Error_ID_Not_Input = "ID or UserID is missing."

#Function for getting all posts from fakeAPI
def get_posts():
    r = requests.get(base_url+posts_endpoint)
    posts = json.loads(r.content)
    return posts

#Posts from fakeAPI
posts = get_posts()

#Importing posts from fakeAPI to ORM database
for post in posts:
    new_post = Post.create(
        id= post['id'],
        userId = post['userId'],
        title = post['title'],
        body = post['body']
    )
    new_post.save()

#Home Page
@app.route('/')
def home():
    return render_template("home.html")


#class Posts and its request methods
class Posts(MethodView):
    #Takes ID or UserID and returns the post or posts with the ID, if no ID or UserID is given, returns all posts
    def get(self, id : str, userId : str):
        posts = get_posts()
        #If there is ID
        if id is not None:
            #If ID is int
            if id.isnumeric():
                id=int(id)
                user_posts = []
                #Looking for post in ORM database
                for i in Post.select():
                    if i.id == id:
                        user_posts.append(i)
                        #Returning post with given ID from ORM database
                        return render_template('posts.html', posts=user_posts)
                #If no posts with given ID are found, looks for posts in fakeAPI /posts endpoint
                if user_posts == '':
                    for i in posts:
                        if i['id'] == id:
                            user_posts.append(i)
                            #Returning posts with given ID from endpoint
                            return render_template('posts.html', posts=user_posts)
                #Error when post with given ID is not found in ORM database or fakeAPI endpoint
                return render_template('errors.html', error= Error_Post_Not_Found)
            #Error when given ID is not integer
            return render_template('errors.html', error=Error_Wrong_ID_Int)
        #If there is UserID
        elif userId is not None:
            #If UserID is integer
            if userId.isnumeric():
                userId=int(userId)
                user_posts = []
                #Looking for post with given UserID in ORM database
                for i in Post.select():
                    #Found post with given UserID
                    if i.userId == userId:
                        user_posts.append(i)
                if user_posts:
                    #Returning if we found any posts with given UserID
                    return render_template('posts.html', posts=user_posts)
                else:
                    #If no posts were found, look for them in fakeAPI
                    for i in posts:
                        #Found post in fakeAPI
                        if i['userId'] ==userId:
                            user_posts.append(i)
                    if user_posts:
                        #Returning if we found any posts with given UserID in fakeAPI
                        return render_template('posts.html', posts=user_posts)
                #Error if no posts were found with given UserID
                return render_template('errors.html', error=Error_Post_Not_Found)
            #Error if UserID given is not integer
            return render_template('errors.html', error=Error_Wrong_ID_Int)
        #Showing all the posts
        return render_template('posts.html', posts=posts)

    #Used to create new post
    def post(self):
        #Receiving data for new post
        new_post_id= request.json['id']
        new_post_userId = request.json['userId']
        new_post_title = request.json['title']
        new_post_body= request.json['body']
        #Checking if all data were given
        if new_post_body is None or new_post_id is None or new_post_userId is None or new_post_body is None:
            #Error if some data are missing
            return render_template('errors.html', error=Error_Data_Missing)
        #Checking if all data are of correct type
        if isinstance(new_post_id, int) ==False or isinstance(new_post_userId, int) == False or isinstance(new_post_body, str) == False or isinstance(new_post_title, str) == False:
            return render_template('errors.html',error="Type of some data is wrong. ID and UserID have to be integer, Body and Title have to be string.")
        #Looking through database if there are any posts with same ID
        for i in Post.select():
            if i.id == new_post_id:
                #Error when the post with same ID is found in database
                return render_template('errors.html', error= "There is already post with this ID")
        #Creating new post
        new_post = Post.create(
            id =new_post_id,
            userId = new_post_userId,
            title = new_post_title,
            body= new_post_body
        )
        #Adding post to ORM database
        new_post.save()
        #Putting new post into JSON format
        new_post = {'id': new_post.id, 'userId': new_post.userId, 'title': new_post.title, 'body': new_post.body}
        #Reading data from JSON database
        with open('db.json', 'r') as f:
            #Loading data from JSON database
            feeds = json.load(f)
        #Adding new post into JSON database
        with open('db.json', 'w') as f:
            feeds["posts"].append(new_post)
            json.dump(feeds, f, indent = 4)
        #Returning created post
        return new_post

    #Used to edit already existing post
    def put(self, id : str):
        #Requesting data
        print(id)
        new_title = request.json['title']
        new_body = request.json['body']
        #Checking if all data were given
        if new_title is None or new_body is None:
            #Error if there are missing data
            return render_template('errors.html', error=Error_Data_Missing)
        #Checking if data are string
        if isinstance(new_title, str) == False or isinstance(new_body,str) == False:
            return render_template('errors.html', error=Error_Wrong_Data_Str)
        #Reading data from JSON database
        with open('db.json', 'r') as f:
            feeds = json.load(f)
        if id is not None:
            #Checking if ID is integer
            if id.isnumeric():
                id= int(id)
                #Looking for post with given ID in ORM database
                for i in Post.select():
                    if i.id == id:
                        #Editing found post in ORM database
                        i.title = new_title
                        i.body = new_body
                        #Posts in JSON database
                        posts=feeds['posts']
                        for j in posts:
                            if j['id'] == i.id:
                                #Editing post JSON database
                                j['title'] = i.title
                                j['body'] = i.body
                                #Writing edited data back into JSON database
                                with open('db.json', 'w') as f:
                                    json.dump(feeds, f, indent=4)
                                #Returning edited post
                                return j
                #Eror if no post with given IDD was found
                return render_template('errors.html', error=Error_Post_Not_Found)
            #Error if give ID is not integer
            return render_template('errors.html', error=Error_Wrong_ID_Int)
        #Return if ID was not given
        return render_template('errors.html', error=Error_ID_Not_Input)

    #Used to delete post
    def delete(self, id: str):
        if id is not None:
            #Checking if given ID is integer
            if id.isnumeric():
                id = int(id)
                #Looking for post in ORM database
                for j in Post.select():
                    if j.id == id:
                        #Deleting post in ORM database
                        post_to_delete = Post.get(id=id)
                        post_to_delete.delete_instance()
                        #Reading data from JSON database
                        with open('db.json', 'r') as f:
                            feeds = json.load(f)
                        #Posts from JSON database
                        posts = feeds['posts']
                        #Looking for post in posts from JSON database
                        for i in posts:
                            if i['id'] == id:
                                #Deleting post
                                posts.remove(i)
                                #Writing edited data back to JSON database
                                with open('db.json', 'w') as f:
                                    json.dump(feeds,f, indent=4)
                                #Returning if post was successfuly deleted
                                return "Post was succesfuly deleted"
                #Returning if post with given ID was not found
                return render_template('errors.html', error=Error_Post_Not_Found)
            #Error if given ID is not integer
            return render_template('erros.html', error = Error_Wrong_ID_Int)
        #Returning if no ID was given
        return render_template('erros.html', error = Error_ID_Not_Input)

posts = Posts.as_view('posts')
#Creating endpoints for REST API
app.add_url_rule('/posts/', view_func=posts, methods = ['POST'])
app.add_url_rule('/posts/', defaults={'userId' : None, 'id' : None},view_func=posts)
app.add_url_rule('/posts/id=<id>',view_func=posts, methods = ['GET', 'PUT','DELETE'])
app.add_url_rule('/posts/userId=<userId>',defaults={'id' : None},  view_func=posts, methods = ['GET'])

if __name__ == '__main__':
    app.run(debug=False)