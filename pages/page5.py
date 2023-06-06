from modules.Utils import readSQL, executeSQL, readYT, readTK, makeKwrdsAndVideoBundles
import streamlit as st
from collections import namedtuple
import math
import pandas as pd
from pyparsing import empty
import streamlit.components.v1 as components
from collections import defaultdict
from st_pages import Page, add_page_title, show_pages
import requests
from streamlit_extras.switch_page_button import switch_page
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(layout="wide")
PAGENUM = 4

# connection info
connection_info = "host=147.47.200.145 dbname=teamdb9 user=team9 password=99990000 port=34543"

df = readYT(connection_info)[['video_title', 'description', 'video_url', 'id']]
titles = df['video_title']; descriptions = df['description']; urls = df['video_url']; ids  = df['id']
# print(titles.keys())

comments = readSQL(connection_info, "SELECT * FROM comments")

emt1,   col1, emt2 = st.columns([5, 90, 5])
emt1,   col2, emt2 = st.columns([20, 60, 20])
emt1,   col3, col4, emt2 = st.columns([5, 45, 45, 5])
emt1,   col5, col6, emt2 = st.columns([5, 45, 45, 5])
emt1,   col71, emt3, col72, emt2 = st.columns([2, 45, 1, 45, 2])
emt1,   col81, emt3, col82, emt2 = st.columns([2, 45, 1, 45, 2])
emt1,   col91, emt3, col92, emt2 = st.columns([2, 45, 1, 45, 2])


commentCols = [col3,col4,col5,col6]

with emt1:
    empty()
with emt2:
    empty()
with emt3:
    empty()

keywordsSet = readTK(connInfo=connection_info)
keywordBundles, videoBundles = makeKwrdsAndVideoBundles(keywordsSet)

video_id = videoBundles[PAGENUM] # {1 : [78]  2: 
with col1:
    if st.button('Home'):
        switch_page('streamlit_app')
    
    print('video-id is :', video_id)
    title = df[df['id'] == video_id]['video_title']
    st.title(title)

    comments = readSQL(connection_info, f"SELECT comment FROM comments where video_id = {video_id}").values.tolist() # {ids[i]}

    video = df[df['id'] == video_id]['video_url']
    video = str(video.values[0])
    st.video(video)

    st.subheader("Comments")    

for comment in comments[:4]:
    idx = comments.index(comment)

    with commentCols[idx]:
        st.write(f'*comment {comments.index(comment)}*')
        comment = comment[0]
        st.markdown(comment)
    
# keywords
keywords = keywordBundles[videoBundles[PAGENUM]]

# load tweet data
tweet_ids = []
for kwrd in keywords:
    query = f"select tweet_id from twitter_data where keyword = \'{kwrd}\'"
    tmp = readSQL(connInfo=connection_info, query=query)
    if not tmp.empty:
        tweet_ids.append(*(tmp.values.tolist()[0]))


def theTweet(tweet_url):
    api = "https://publish.twitter.com/oembed?url={}".format(tweet_url)
    response = requests.get(api)
    res = response.json()["html"]
    return res

twitter_base = "https://twitter.com/twitter/statuses/"

urls = []
for tweet_id in tweet_ids:
    tmp = twitter_base + str(tweet_id)
    urls.append(tmp)

with col71:
    st.subheader("Tweets")
    try:
        res = theTweet(urls[0])
        components.html(res, height=700, width=400)
    except: pass
    try:
        res = theTweet(urls[2])
        components.html(res, height=700, width=400)
    except: pass

with col72:
    try:
        res = theTweet(urls[1])
        components.html(res, height=700, width=300)
    except: pass
    try:
        res = theTweet(urls[3])
        components.html(res, height=700, width=300)
    except: pass

with col81:
    st.subheader("Instagram")

with col91:
    st.subheader("News")
