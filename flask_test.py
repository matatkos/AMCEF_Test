import requests
import json
from flask import Flask, request, render_template
from flask_restful import Resource, Api
from requests import put, get
from flask.views import MethodView, View

import rest_api

app = Flask(__name__)
api = Api(app)

base_url = 'http://localhost:3000/'

users_endpoint = 'users'
posts_endpoint = 'posts'


#class Users(View)
class Posts(MethodView):
    def get(self):
        r = requests.get(base_url+posts_endpoint)
        posts = json.loads(r.content)
        return render_template('users.html', posts= posts)
app.add_url_rule('/posts', view_func=Posts.as_view('posts'))

'''
class Users(View):
    def render_template(self):
        return render_template('layout.html')

app.add_url_rule('/users', view_func=Users.as_view('users'))
'''

@app.route('/users')
def Users():
    return render_template('users.html')


#api.add
if __name__ == '__main__':
    app.run(debug=False)