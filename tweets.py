###############
### Imports ###
###############



import streamlit as st
from utils import *



###########################
### App Metadata/Design ###
###########################



st.title('Politics and Twitter')



####################################
### App Layout and Functionality ###
####################################



tweets, user = showRandomTweets()

if st.checkbox("Show data"):
    st.write(get())
    
st.write()
    
nme = st.text_input(label = "Your Name", placeholder = "John Appleseed")
rater = hash(nme)

st.write(tweets)

rating = st.radio(label = "Rate the user above", options = ["Republican", "Democrat", "I don't know"], index = 2)

