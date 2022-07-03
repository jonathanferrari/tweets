 
import pandas as pd, numpy as np, streamlit as st
import streamlit.components.v1 as comp, urllib.request as urlreq
import requests, json, os, re

def showTweet(tweet_url):
    short_url, pat = urlreq.urlopen(tweet_url).url, r"(https.*/status/\d*)/"
    url = re.findall(pat, short_url)[0]
    api=f"https://publish.twitter.com/oembed?url={url}"
    text = requests.get(api).json()["html"]
    text = text.replace('<blockquote class="twitter-tweet">', 
                 '<blockquote class="twitter-tweet">')
    return comp.html(text, width = 400, height = 610)

showTweet("https://t.co/sIsOS8sjwV")