import requests
from requests_oauthlib import OAuth1
from multiprocessing import Pool, TimeoutError
from main_app.conf import DUCK_DUCK_GO_URL, GOOGLE_API_URL, \
    TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, \
    TWITTER_ACCESS_TOKEN, TWITTER_TOKEN_SECRET, TWITTER_API_URL
from pprint import pprint


def make_duck_duck_go_response(query):
    duckduckgo_data = requests.get(DUCK_DUCK_GO_URL, params = {
            'q': query
        })

    data = duckduckgo_data.json()
    main_data = data.get('RelatedTopics')
    if not main_data:
        return {
            'duckduckgo': {
                "url": "",
                "text": ""
            }
        }
    else:
        return {
            'duckduckgo': {
                "url": main_data[0]['FirstURL'],
                "text": main_data[0]['Text']
            }
        }


def make_google_response(query):
    google_data = requests.get(GOOGLE_API_URL, params = {
            'q': query
        })

    data = google_data.json()
    main_data = data.get('items')
    if not main_data:
        return {
            'google': {
                "url": "",
                "text": ""
            }
        }
    else:
        return {
            'google': {
                "url": main_data[0]['link'],
                "text": main_data[0]['snippet']
            }
        }


def make_twitter_response(query):
    auth = OAuth1(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET,
                  TWITTER_ACCESS_TOKEN, TWITTER_TOKEN_SECRET)

    twitter_data = requests.get(TWITTER_API_URL, auth=auth, params = {
            'q': query
        })

    data = twitter_data.json()
    main_data = data['statuses']
    if not main_data:
        return {
            'twitter': {
                "url": "",
                "text": ""
            }
        }
    else:
        data_url = 'https://twitter.com/' + \
                    main_data[0]['user']['screen_name'] + \
                    '/status/' + main_data[0]['id_str']

        return {
            'twitter': {
                "url": data_url,
                "text": main_data[0]['text']
            }
        }


def fetch_data(query):
    pool = Pool()
    duckduckgo_object = pool.apply_async(make_duck_duck_go_response, (query,))
    google_object = pool.apply_async(make_google_response, (query,))
    twitter_object = pool.apply_async(make_twitter_response, (query,))

    try:
        duckduckgo_data = duckduckgo_object.get(timeout=1)
    except TimeoutError:
        duckduckgo_data = {
            'duckduckgo': {
                'error': 'Request get timed out'
            }
        }
    try:
        google_data = google_object.get(timeout=1)
    except TimeoutError:
        google_data = {
            'google': {
                'error': 'Request get timed out'
            }
        }

    try:
        twitter_data = twitter_object.get(timeout=1)
    except TimeoutError:
        twitter_data = {
            'twitter': {
                'error': 'Request get timed out'
            }
        }

    res = {}
    res.update(duckduckgo_data)
    res.update(google_data)
    res.update(twitter_data)

    return res
