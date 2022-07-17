import requests
import numbers
import json
from flask import Flask, request, render_template, jsonify
from flask_restful import Resource, Api
from requests import put, get
from flask.views import MethodView, View
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.database'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
base_url = 'http://localhost:3000/'

users_endpoint = 'users'
posts_endpoint = 'posts'

db=SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    title= db.Column(db.String)
    body= db.Column(db.String)

db.create_all()



Error_Wrong_ID_Int = "Wrong ID input. ID has to be integer."
Error_Wrong_Data_Str = "Wrong data input. Data have to be string."
Error_Data_Missing = "Some data you want to input are missing. Please check again."
Error_Post_Not_Found = "Post with this ID could not be found."
Error_ID_Not_Input = "ID or UserID is missing."

def get_post_by_id(id, posts):
    for i in posts:
        if i['id'] == id:
            return i

def get_post_by_userid(userid, posts):
    for i in posts:
        if i['userId'] == userid:
            return i

def get_posts():
    r = requests.get(base_url+posts_endpoint)
    posts = json.loads(r.content)
    return posts



@app.route('/')
def home():
    return render_template("home.html")


#class Users(View)
class Posts(MethodView):
    def get(self, id : str, userId : str):

        posts = get_posts()
        #If there is ID
        if id is not None:

            if id.isnumeric():
                id=int(id)
                for i in posts:
                    if i['id'] == id:
                        user_posts = []
                        user_posts.append(i)
                        return render_template('posts.html', posts=user_posts)
                return render_template('errors.html', error= Error_Post_Not_Found)
            return render_template('errors.html', error=Error_Wrong_ID_Int)
        #If there is UserID
        elif userId is not None:
            if userId.isnumeric():
                userId=int(userId)
                user_posts = []
                any_posts = False
                for i in posts:
                    if i['userId'] == userId:
                        user_posts.append(i)
                        any_posts= True
                if any_posts:
                    return render_template('posts.html', posts=user_posts)
                return render_template('errors.html', error=Error_Post_Not_Found)
            return render_template('errors.html', error=Error_Wrong_ID_Int)
        #Showing all the posts
        return render_template('posts.html', posts=posts)

    def post(self):
        new_post_id = request.json['id']
        new_post_userId = request.json['userId']
        new_post_title = request.json['title']
        new_post_body = request.json['body']
        if new_post_body is None or new_post_id is None or new_post_userId is None or new_post_body is None:
            return render_template('errors.html', error=Error_Data_Missing)

        post= Post(new_post_id, new_post_userId, new_post_title, new_post_body)
        db.session.add(post)
        db.commit()

        new_post = {'id': new_post_id, 'userId': new_post_userId, 'title': new_post_title, 'body': new_post_body}

        with open('db.json', 'r') as f:
            feeds = json.load(f)
            print(feeds)
        with open('db.json', 'w') as f:
            feeds["posts"].append(new_post)
            json.dump(feeds, f, indent = 4)
        return new_post

    def put(self, id : str, userId : str):
        new_title = request.json['title']
        new_body = request.json['body']
        if isinstance(new_title, str) == False or isinstance(new_body,str) == False:
            return render_template('errors.html', error=Error_Wrong_Data_Str)

        with open('db.json', 'r') as f:
            feeds = json.load(f)

        if id is not None:
            if id.isnumeric():
                id= int(id)
                posts = feeds['posts']
                for i in posts:
                    if i['id'] == id:
                        if new_title is not None:
                            i['title'] = new_title
                        if new_body is not None:
                            i['body'] = new_body
                        with open('db.json', 'w') as f:
                            json.dump(feeds, f, indent=4)
                        return i
                return render_template('errors.html', error=Error_Post_Not_Found)
            return render_template('errors.html', error=Error_Wrong_ID_Int)

        elif userId is not None:
            if userId.isnumeric():
                userId=int(userId)
                posts = feeds['posts']
                for i in posts:
                    if i['userId'] == userId:
                        if new_title is not None:
                            i['title'] = new_title
                        elif new_body is not None:
                            i['body'] = new_body
                        with open('db.json', 'w') as f:
                            json.dump(feeds, f, indent=4)
                        return i
                return render_template('errors.html', error=Error_Post_Not_Found)
            return render_template('errors.html', error=Error_Wrong_ID_Int)
        return render_template('errors.html', error=Error_ID_Not_Input)
    def delete(self, id, userId):
        if id is not None:
            with open('db.json', 'r') as f:
                feeds = json.load(f)
            posts = feeds['posts']
            for i in posts:
                if i['id'] == id:
                    posts.remove(i)
                    with open('db.json', 'w') as f:
                        json.dump(feeds,f, indent=4)
                    return "Post was succesfulyy deleted"
            return render_template('errors.html', error=Error_Post_Not_Found)
        elif userId is not None:
            with open('db.json', 'r') as f:
                feeds = json.load(f)
            posts = feeds['posts']
            for i in posts:
                if i['userId'] == userId:
                    posts.remove(i)
                    with open('db.json', 'w') as f:
                        json.dump(feeds, f, indent=4)
                    return "Post was succesfulyy deleted"
            return render_template('errors.html', error=Error_Post_Not_Found)

posts = Posts.as_view('posts')
app.add_url_rule('/posts/', view_func=posts, methods = ['POST'])
app.add_url_rule('/posts/', defaults={'userId' : None, 'id' : None},view_func=posts)
app.add_url_rule('/posts/id=<id>', defaults={'userId' : None},view_func=posts, methods = ['GET', 'PUT','DELETE'])
app.add_url_rule('/posts/userId=<userId>',defaults={'id' : None},  view_func=posts, methods = ['GET', 'PUT', 'DELETE'])



'''class ShowPostByID(MethodView):
    def get(self, id):
        posts = get_posts()
        if id is None:
            pass
        else:
            pass
        for i in posts:
            if i['id'] == id:
                posts = i
        return render_template('posts.html', posts=posts)
app.add_url_rule('/posts/blablablalba')'''
'''
class Users(View):
    def render_template(self):
        return render_template('layout.html')

app.add_url_rule('/users', view_func=Users.as_view('users'))
'''

@app.route('/users')
def Users():
    return "ahoj"


#api.add
if __name__ == '__main__':
    app.run(debug=True)