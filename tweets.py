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

postTest = poster(["rater", "rated", "rating"], "ratings")

tweets, user = showTweets()

if st.checkbox("Show data"):
    st.write(get())
    
st.write()
    
nme = st.text_input(label = "Your Name", placeholder = "John Appleseed")
rater = hash(nme)

st.write(tweets)

rating = st.radio(label = "Rate the user above", options = ["Republican", "Democrat", "I don't know"], index = 2)

# def update(username, table = "tweets", step = 1):
#     """Update specific field values for a record."""
#     sheet = f"{url}/{table}"
#     headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
#     record = dict(get().query(f"user == '{username}'").iloc[0, :])
#     new_record = {"records": [ {"id": record["id"], "fields": {"Rated": int(record["Rated"]) + step}}]}
#     response = requests.request("PATCH", sheet, headers=headers, data=json.dumps(new_record))
#     return response


if st.button("Submit"):
    postTest(rater, user, rating)
    st.write("SUBMITTED")