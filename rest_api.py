import requests
base_url = 'http://localhost:3000/'

users_endpoint = 'users'
posts_endpoint = 'posts'

def main_request(base_url, edpoint):
    r= requests.get(base_url+edpoint)
    return r.json()

posts_data = main_request(base_url, posts_endpoint)
users_data = main_request(base_url, users_endpoint)

def get_post_by_id(user_or_post,id):
    for i in posts_data:
        if i['id'] == id:
            return i

def get_post_by_userid(userid):
    for i in posts_data:
        if i['userId'] == id:
            return i


