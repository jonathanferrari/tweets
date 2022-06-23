# ## Imports & `.env` Setup


import pandas as pd, numpy as np, streamlit as st
import requests, os, dotenv, json, IPython.display
from hashlib import *
from IPython.display import *
dotenv.load_dotenv();
st.title('Politics and Twitter')


# ## Load Secret Variables

# ### Twitter



def do_tweepy_auth():
    key, secret_key = (os.getenv(i) for i in ["TWEET_KEY", "TWEET_SECRET_KEY"])
    auth = tw.OAuthHandler(key, secret_key)
    api = tw.API(auth, wait_on_rate_limit=True)


# ### Airtable




token, base, url = (os.getenv(i) for i in ["AIRTABLE_TOKEN",
                                           "AIRTABLE_BASE_ID",
                                           "AIRTABLE_URL"])


# ## Functions

# ### Twitter




def getTweets(search, method = "search_tweets", n = 50):
    tweets = tw.Cursor(eval(f"api.{method}"),
              q=search,
              lang="en").items(n)
    tweets = list(tweets)
    print("Total Tweets fetched:", len(tweets))
    return tweets
    # frm = pd.DataFrame([tweet._json | {"user" 
    #                                    : tweet.user._json["name"]} 
    #                     for tweet in tweets])
    # return frm[["text", "user"]]


def getUser(username):
    return api.search_users(username, count = 1)
def getTimeline(username, n = 100000):
    tweets = api.search_tweets(username, count = n)
    cleanTweets = [tweet._json["text"] for tweet in tweets if tweet.user._json["screen_name"] == username]
    return cleanTweets


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

# ### App

def showRandomTweets():
    tweets = get()
    selected = tweets.sample(1).iloc[0, :]
    selectedTweets, selectedUser = selected[[f"tweet{i+1}" for i in range(10)]], selected["user"]
    selectedTweets = "\n".join(["### •" + t for t in selectedTweets])
    return selectedTweets, selectedUser

def hash(obj):
    return sha1(obj.encode("utf-8")).hexdigest()

# # Work


tweets, user = showRandomTweets()

if st.button("Show data"):
    st.write(get())
    
st.write()
    
nme = st.text_input(label = "Your Name", placeholder = "John Appleseed")
rater = hash(nme)

st.write(tweets)

rating = st.radio(label = "Rate the user above", options = ["Republican", "Democrat", "I don't know"], index = 2)

