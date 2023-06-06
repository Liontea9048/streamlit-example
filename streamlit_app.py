from modules.Utils import readYT, readTK, makeKwrdsAndVideoBundles
import streamlit as st
from collections import namedtuple
import math
import pandas as pd
from pyparsing import empty
import streamlit.components.v1 as components
from collections import defaultdict
from st_pages import Page, add_page_title, show_pages, hide_pages
from streamlit_extras.switch_page_button import switch_page
# import warnings
# warnings.filterwarnings('ignore')


# connection_info = "host=147.47.200.145 dbname=teamdb9 user=team9 password=99990000 port=34543"
# df = readSQL(connection_info, """
# SELECT * FROM youtube_trending_video
# where collect_datetime = (select max(collect_datetime) from youtube_trending_video)
# """)

def main():
    st.set_page_config(layout="wide")
    
    add_page_title()
    show_pages(
    [
        Page("streamlit_app.py", "Home"),
        Page("pages/page1.py", "Topic1"),
        Page("pages/page2.py", "Topic2"),
        Page("pages/page3.py", "Topic3"),
        Page("pages/page4.py", "Topic4"),
        Page("pages/page5.py", "Topic5"),
        Page("pages/page6.py", "Topic6"),
        Page("pages/page7.py", "Topic7"),
        Page("pages/page8.py", "Topic8"),
        Page("pages/page9.py", "Topic9"),
        Page("pages/page10.py", "Topic10"),
    ]
)

    # connection info
    connection_info = "host=147.47.200.145 dbname=teamdb9 user=team9 password=99990000 port=34543"

    # collect from tredning video tables
    df = readYT(connection_info)[['video_title', 'thumbnail_url', 'video_url', 'id']]
    titles = df['video_title']; urls = df['video_url']; 
    video_ids  = df['id']; thumnail_urls=df['thumbnail_url']
    
    # id, video_id, keyword, rank, timestamp    
    keywordsSet = readTK(connInfo=connection_info)
    keywordBundles, videoidBundles = makeKwrdsAndVideoBundles(keywordsSet)
    
    numBundle = int(max(keywordsSet['rank']))
    verticalSpace = 7

    emt1,   col1,        emt2 = st.columns([5, 90, 5])
    emt1,   col2,  col3, emt2 = st.columns([5, 45, 45, 5])
    emt1,   col4,  col5, emt2 = st.columns([5, 45, 45, 5])
    emt1,   col6,  col7, emt2 = st.columns([5, 45, 45, 5])
    emt1,   col8,  col9, emt2 = st.columns([5, 45, 45, 5])
    emt1,  col10, col11, emt2 = st.columns([5, 45, 45, 5])

    cols = [col2, col3, col4, col5, col6, col7, col8, col9, col10, col11]
    video_list = []
    with emt1:
        empty()

    with col1 :
        st.title("Trend-Seeker")
        st.subheader("We Present a Trend Videos and Reactions!")

    maxLengthofKwrd = len(keywordsSet) - 2
    # print(maxLengthofKwrd)
    tmpLengthofKwrd = 0

    if tmpLengthofKwrd < maxLengthofKwrd:
        tmpLengthofKwrd += 1
        with col2:
            # try:
            video_id = videoidBundles[0]
        
            title = df[df['id'] == video_id]['video_title']
            title = str(title.values[0])

            if st.button(title):
                switch_page("topic1")

    if tmpLengthofKwrd < maxLengthofKwrd:
        tmpLengthofKwrd += 1
        with col3:
            video_id = videoidBundles[1]
            title = df[df['id'] == video_id]['video_title']
            title = str(title.values[0])
            if st.button(title):
                switch_page("topic2")

    if tmpLengthofKwrd < maxLengthofKwrd:
        tmpLengthofKwrd += 1
        with col4:
            video_id = videoidBundles[2]
            title = df[df['id'] == video_id]['video_title']
            title = str(title.values[0])
            if st.button(title):
                switch_page("topic3")

    if tmpLengthofKwrd < maxLengthofKwrd:
        tmpLengthofKwrd += 1
        with col5:
            video_id = videoidBundles[3]
            title = df[df['id'] == video_id]['video_title']
            title = str(title.values[0])
            if st.button(title):
                switch_page("topic4")

    if tmpLengthofKwrd < maxLengthofKwrd:
        tmpLengthofKwrd += 1
        with col6:
            video_id = videoidBundles[4]
            title = df[df['id'] == video_id]['video_title']
            title = str(title.values[0])
            if st.button(title):
                switch_page("topic5")

    if tmpLengthofKwrd < maxLengthofKwrd:
        tmpLengthofKwrd += 1
        with col7:
            # try:
            video_id = videoidBundles[5]
        
            title = df[df['id'] == video_id]['video_title']
            title = str(title.values[0])

            if st.button(title):
                switch_page("topic6")

    if tmpLengthofKwrd < maxLengthofKwrd:
        tmpLengthofKwrd += 1
        with col8:
            video_id = videoidBundles[6]
            title = df[df['id'] == video_id]['video_title']
            title = str(title.values[0])
            if st.button(title):
                switch_page("topic7")

    if tmpLengthofKwrd < maxLengthofKwrd:
        tmpLengthofKwrd += 1
        with col9:
            video_id = videoidBundles[7]
            title = df[df['id'] == video_id]['video_title']
            title = str(title.values[0])
            if st.button(title):
                switch_page("topic8")

    if tmpLengthofKwrd < maxLengthofKwrd:
        tmpLengthofKwrd += 1
        with col10:
            video_id = videoidBundles[8]
            title = df[df['id'] == video_id]['video_title']
            title = str(title.values[0])
            if st.button(title):
                switch_page("topic9")

    if tmpLengthofKwrd < maxLengthofKwrd:
        tmpLengthofKwrd += 1
        with col11:
            video_id = videoidBundles[9]
            title = df[df['id'] == video_id]['video_title']
            title = str(title.values[0])
            if st.button(title):
                switch_page("topic10")


    for col in cols:
        idx = cols.index(col) # 0 1 2 ... 9
        if idx >= maxLengthofKwrd-1-1:
            continue
        with col:
            # print(videoidBundles)
            video_id = videoidBundles[idx]
            video_list.append(video_id)
            
            title = df[df['id'] == video_id]['video_title']
            title = str(title.values[0])
            # if st.button(title):
            #     switch_page(f"topic{idx+1}")
            imageURL = df[df['id'] == video_id]['thumbnail_url'].values[0]
            st.image(imageURL, width = 600)
            

    with emt2:
        empty()

if __name__ == '__main__':
    main()

# st.title('Hello Streamlit')


# with st.echo(code_location='below'):
#     total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
#     num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

#     Point = namedtuple('Point', 'x y')
#     data = []

#     points_per_turn = total_points / num_turns

#     for curr_point_num in range(total_points):
#         curr_turn, i = divmod(curr_point_num, points_per_turn)
#         angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
#         radius = curr_point_num / total_points
#         x = radius * math.cos(angle)
#         y = radius * math.sin(angle)
#         data.append(Point(x, y))

#     st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
#         .mark_circle(color='#0068c9', opacity=0.5)
#         .encode(x='x:Q', y='y:Q'))