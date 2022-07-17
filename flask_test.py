import requests
import json
from flask import Flask, request, render_template, jsonify
from flask_restful import Resource, Api
from flask.views import MethodView, View
from peewee import SqliteDatabase, Model, TextField, IntegerField
import os
from os.path import exists
if os.path.exists('posts.db'):
    os.remove('posts.db')

app = Flask(__name__)
api = Api(app)

base_url = 'http://localhost:3000/'

users_endpoint = 'users'
posts_endpoint = 'posts'

db = SqliteDatabase('posts.db')

class BaseTable(Model):
    class Meta:
        database = db

class Post(BaseTable):
    id = IntegerField(primary_key=True, index=True)
    userId = IntegerField()
    title= TextField()
    body= TextField()

db.connect()
db.create_tables([Post])

'''post1 = Posts.create(
    userId= 1,
    title = "Skusobny text na peewee",
    body="Testujem peewee"
)
post1.save()
for posts in Posts.select():
    print("id:",posts.id)
'''
Error_Wrong_ID_Int = "Wrong ID input. ID has to be integer."
Error_Wrong_Data_Str = "Wrong data input. Data have to be string."
Error_Data_Missing = "Some data you want to input are missing. Please check again."
Error_Post_Not_Found = "Post with this ID could not be found."
Error_ID_Not_Input = "ID or UserID is missing."


def get_posts():
    r = requests.get(base_url+posts_endpoint)
    posts = json.loads(r.content)
    return posts

posts = get_posts()

for post in posts:
    new_post = Post.create(
        id= post['id'],
        userId = post['userId'],
        title = post['title'],
        body = post['body']
    )
    print(new_post.id, new_post.userId, new_post.title, new_post.body)
    new_post.save()




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
                user_posts = []
                for i in Post.select():
                    if i.id == id:
                        user_posts.append(i)
                        return render_template('posts.html', posts=user_posts)
                if user_posts == None:
                    for i in posts:
                        if i['id'] == id:
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
                for i in Post.select():
                    if i.userId == userId:
                        user_posts.append(i)
                        any_posts= True
                if any_posts:
                    return render_template('posts.html', posts=user_posts)
                else:
                    for i in posts:
                        if i['userId'] ==userId:
                            user_posts.append(i)
                            any_posts=True
                    if any_posts == True:
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

        for i in Post.select():
            if i.id == new_post_id:
                return render_template('errors.html', error= "There is already post with this ID")

        new_post = Post.create(
            id =new_post_id,
            userId = new_post_userId,
            title = new_post_title,
            body= new_post_body
        )
        new_post.save()
        new_post = {'id': new_post.id, 'userId': new_post.userId, 'title': new_post.title, 'body': new_post.body}

        with open('db.json', 'r') as f:
            feeds = json.load(f)
        with open('db.json', 'w') as f:
            feeds["posts"].append(new_post)
            json.dump(feeds, f, indent = 4)
        return new_post

    def put(self, id : str, userId : str):
        new_title = request.json['title']
        new_body = request.json['body']

        if new_title is None or new_body is None:
            return render_template('errors.html', error=Error_Data_Missing)

        if isinstance(new_title, str) == False or isinstance(new_body,str) == False:
            return render_template('errors.html', error=Error_Wrong_Data_Str)

        with open('db.json', 'r') as f:
            feeds = json.load(f)

        if id is not None:
            if id.isnumeric():
                id= int(id)
                for i in Post.select():
                    if i.id == id:
                        i.title = new_title
                        i.body = new_body
                        posts = feeds['posts']
                        for j in posts:
                            if j['id'] == i.id:
                                if new_title is not None:
                                    i['title'] = i.title
                                if new_body is not None:
                                    i['body'] = i.body
                                with open('db.json', 'w') as f:
                                    json.dump(feeds, f, indent=4)
                                return i
                return render_template('errors.html', error=Error_Post_Not_Found)
            return render_template('errors.html', error=Error_Wrong_ID_Int)
        elif userId is not None:
            if userId.isnumeric():
                userId=int(userId)
                for j in Post.select():
                    if j.userId == userId:
                        j.title = new_title
                        j.body = new_body
                        posts = feeds['posts']
                        for i in posts:
                            if i['userId'] == j.userId:
                                if new_title is not None:
                                    i['title'] = j.new_title
                                elif new_body is not None:
                                    i['body'] = j.new_body
                                with open('db.json', 'w') as f:
                                    json.dump(feeds, f, indent=4)
                                return i
                return render_template('errors.html', error=Error_Post_Not_Found)
            return render_template('errors.html', error=Error_Wrong_ID_Int)
        return render_template('errors.html', error=Error_ID_Not_Input)
    def delete(self, id, userId):
        if id is not None:
            if id.isnumeric:
                id = int(id)
                for j in Post.select():
                    if j.id == id:
                        post_to_delete = Post.get(id=id)
                        post_to_delete.delete_instance()
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
            return render_template('erros.html', error = Error_Wrong_ID_Int)
        elif userId is not None:
            if userId.isnumeric:
                userId = int(userId)
                for j in Post.select():
                    if j.userId == userId:
                        post_to_delete = Post.get(userId=userId)
                        post_to_delete.delete_instance()
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
            return render_template('erros.html', error= Error_Wrong_ID_Int)
        return render_template('erros.html', error = Error_ID_Not_Input)

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