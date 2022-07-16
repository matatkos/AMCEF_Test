import requests
import json
from flask import Flask, request, render_template, jsonify
from flask_restful import Resource, Api
from requests import put, get
from flask.views import MethodView, View
import rest_api

app = Flask(__name__)
api = Api(app)

base_url = 'http://localhost:3000/'

users_endpoint = 'users'
posts_endpoint = 'posts'

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

#class Users(View)
class Posts(MethodView):
    def get(self, id, userId):
        posts = get_posts()
        #If there is ID
        if type(id) != int:
            if id == '':
                return "Could not find any posts with this ID"
            for i in posts:
                if i['id'] == id:
                    user_posts = []
                    user_posts.append(i)
                    return render_template('posts.html', posts=user_posts)
            return "Could not find any posts with this ID"
        #If there is UserID
        elif userId is not None:
            user_posts = []
            any_posts = False
            for i in posts:
                if i['userId'] == userId:
                    user_posts.append(i)
                    any_posts= True
            if any_posts:
                return render_template('posts.html', posts=user_posts)
            return "Couldnt find any posts with this UserID"
        #Showing all the posts
        return render_template('posts.html', posts=posts)

    def post(self):
        new_post_id = request.json['id']
        new_post_userId = request.json['userId']
        new_post_title = request.json['title']
        new_post_body = request.json['body']
        new_post = {'id': new_post_id, 'userId': new_post_userId, 'title': new_post_title, 'body': new_post_body}
        with open('db.json', 'r') as f:
            feeds = json.load(f)
            print(feeds)
        with open('db.json', 'w') as f:
            feeds["posts"].append(new_post)
            json.dump(feeds, f, indent = 4)
        return new_post

    def put(self, id, userId):
        new_title = request.json['title']
        new_body = request.json['body']
        with open('db.json', 'r') as f:
            feeds = json.load(f)
        if id is not None:
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
            return "Post was not found"
        if userId is not None:
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
            return "Post was not found"
        return '', 200
    def delete(self, id, userid):
        if id is not None
        return

posts = Posts.as_view('posts')
app.add_url_rule('/posts/', view_func=posts, methods = ['POST'])
app.add_url_rule('/posts/', defaults={'userId' : None, 'id' : None},view_func=posts)
app.add_url_rule('/posts/id=<int:id>', defaults={'userId' : None},view_func=posts, methods = ['GET', 'PUT','DELETE'])
app.add_url_rule('/posts/userId=<int:userId>',defaults={'id' : None},  view_func=posts, methods = ['GET', 'PUT', 'DELETE'])



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