import requests
base_url = 'http://localhost:3000/'

users_endpoint = 'users'
posts_endpoint = 'posts'

posts = requests.get(base_url + posts_endpoint)
users = requests.get(base_url + users_endpoint)

posts_jsoned = posts.json()
posts_jsoned
print(posts_jsoned[])

