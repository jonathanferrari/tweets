# ## Imports & `.env` Setup


import pandas as pd, numpy as np, tweepy as tw, streamlit as st, requests, os, dotenv, json
dotenv.load_dotenv();
st.title('Politics and Twitter')


# ## Load Secret Variables

# ### Twitter




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


# # Work



def getUser(username):
    return api.search_users(username, count = 1)
def getTimeline(username):
    tweets = api.search_tweets(username, count = 10000)
    cleanTweets = [tweet for tweet in tweets if tweet.user._json["screen_name"] == username]
    return cleanTweets


if st.button("Show data"):
    st.write(get())