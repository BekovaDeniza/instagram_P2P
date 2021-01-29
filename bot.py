import pprint
from time import sleep
from InstagramAPI import InstagramAPI

api  =  InstagramAPI ( "username", "password")

api.USER_AGENT = 'Instagram 10.34.0 Android (18/4.3; 320dpi; 720x1280; Xiaomi; HM 1SW; armani; qcom; en_US)'

users_list = []
following_users = []

def get_likes_list(username):
    """ Function: return all likers with user ID and username. """
    api.login()
    # Search for user
    api.searchUsername(username)
    result = api.LastJson
    username_id = result['user']['pk']
    # Get most recent post
    user_posts = api.getUserFeed(username_id)
    result = api.LastJson
    media_id = result['items'][0]['id']
    # Get Likers
    api.getMediaLikers(media_id)
    users = api.LastJson['users']
    for user in users:
        users_list.append({'pk':user['pk'], 'username':user['username']})
    follow_users(users_list)


def follow_users(users_list):
    """ Function: subscribe to users. """
    api.login()
    api.getSelfUsersFollowing()
    result = api.LastJson
    for user in result['users']:
        following_users.append(user['pk'])
    for user in users_list:
        if not user['pk'] in following_users:
            print('Following @' + user['username'])
            api.follow(user['pk'])
            sleep(10)
        else:
            print('Already following @' + user['username'])
            sleep(10)


def get_my_profile_details():
    """ Function: getting information from your account."""
    api.login()
    api.getSelfUsernameInfo()
    result = api.LastJson
    username = result['user']['username']
    full_name = result['user']['full_name']
    followers = result['user']['follower_count']
    print({'Username': username, 'Full name': full_name, 'Followers': followers})


def get_my_feed():
    """ Function: getting the URL of posts. """
    image_urls = []
    api.login()
    api.getSelfUserFeed()
    result = api.LastJson
    if 'items' in result.keys():
        for item in result['items'][:5]:
            if 'image_versions2' in item.keys():
                image_url = item['image_versions2']['candidates'][1]['url']
                image_urls.append(image_url)
    print(image_urls)


get_likes_list('profile_name')
