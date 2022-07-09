from hashlib import *
import requests, os, dotenv, json, re
import streamlit.components.v1 as comp, urllib.request as urlreq
import pandas as pd, numpy as np, streamlit as st



######################################
### Load Secret Variables and .env ###
######################################



dotenv.load_dotenv()
token, base, url = (os.getenv(i) for i in ["AIRTABLE_TOKEN",
                                           "AIRTABLE_BASE_ID",
                                           "AIRTABLE_URL"])



##########################
### Airtable Functions ###
##########################



def post(data, table = "ratings"):
    """Add data to the Airtable."""
    sheet = f"{url}/{table}"
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    response = requests.request("POST", sheet, headers=headers, data=json.dumps(data))
    return response


def get(query = None, table = "tweets"):
    """Retrieve Tweet Data"""
    sheet = f"{url}/{table}"
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    response = requests.request("GET", sheet, headers=headers)
    data = [{"id" : record["id"]} | record["fields"] for record in eval(response.text)["records"]]
    frame = pd.DataFrame(data)
    return frame


def update(username, table = "tweets", step = 1):
    """Update specific field values for a record."""
    sheet = f"{url}/{table}"
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    record = dict(get().query(f"user == '{username}'").iloc[0, :])
    new_record = {"records": [ {"id": record["id"], "fields": {"Rated": int(record["Rated"]) + step}}]}
    response = requests.request("PATCH", sheet, headers=headers, data=json.dumps(new_record))
    return response



#####################
### App Functions ###
#####################



def showRandomTweets():
    tweets = get()
    selected = tweets.sample(1).iloc[0, :]
    selectedTweets, selectedUser = selected[[f"tweet{i+1}" for i in range(10)]], selected["user"]
    selectedTweets = "\n".join(["### •" + t for t in selectedTweets])
    return selectedTweets, selectedUser


def hash(obj):
    """Hash `obj` using Secure Hasing Algorithm 1 Protocol"""
    return sha1(obj.encode("utf-8")).hexdigest()


def showTweet(tweet_url):
    """Show a tweet via the `twitter blockquote` HTML tag"""
    short_url, pat = urlreq.urlopen(tweet_url).url, r"(https.*/status/\d*)/"
    url = re.findall(pat, short_url)[0]
    api=f"https://publish.twitter.com/oembed?url={url}"
    text = requests.get(api).json()["html"]
    text = text.replace('<blockquote class="twitter-tweet">', 
                 '<blockquote class="twitter-tweet">')
    return comp.html(text, width = 400, height = 610)
