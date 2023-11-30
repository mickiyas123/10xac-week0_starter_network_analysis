import streamlit as stl
import os, sys
import json
import glob
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from nltk.corpus import stopwords
from wordcloud import WordCloud

rpath = os.path.abspath('..')
if rpath not in sys.path:
    sys.path.insert(0, rpath)

from src.loader import SlackDataLoader
import src.utils as utils


# Please include the path to datafiles here for this code to work
read_file = SlackDataLoader("../anonymized")
message_with_user = read_file.slack_parser("../anonymized/Week8and9/")
stl.set_option('deprecation.showPyplotGlobalUse', False)
msg_sent_standard_time = utils.convert_2_timestamp("msg_sent_time", message_with_user)
message_with_user["msg_sent_standard_time"] = pd.to_datetime(msg_sent_standard_time)

json_files = glob.glob(os.path.join("../anonymized/all-week3/", '*.json'))
combined_df  = pd.DataFrame()

for json_file in json_files:
    with open(json_file, 'r') as f:
        json_data = json.load(f)
    df = pd.json_normalize(json_data)

replies_df = pd.json_normalize(df["replies"].explode())
replies_df['ts'] = pd.to_datetime(replies_df['ts'], unit='s')
replies_df['time_difference'] = replies_df.groupby('user')['ts'].diff()
replies_df = replies_df.dropna()
combined_df = df.append(replies_df, ignore_index=True)

def draw_avg_reply_count(data, channel='Random'):
    """who commands many replies?"""

    fig, ax = plt.subplots(figsize=(15, 7.5))
    data.groupby('sender_name')['reply_count'].mean().sort_values(ascending=False)[:20]\
        .plot(kind='bar', ax=ax)
    
    ax.set_title(f'Average Number of reply count per Sender in #{channel}', size=20, fontweight='bold')
    ax.set_xlabel("Sender Name", size=18)
    ax.set_ylabel("Frequency", size=18)
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14)

    # Return the Matplotlib figure
    return fig


stl.set_page_config(page_title="10 Academy week0", page_icon=":ninja:", layout="wide")
# Header section

# Body Section
with stl.container():
    stl.subheader("Hi, I am mike :wave:")
    stl.title("This is a presentation of my finding for task 1 and 2")
with stl.container():
    stl.write("---")
    left_column, right_column = stl.columns([0.3, 0.7])
    with left_column:
        stl.header("Task 1")
        stl.write("##")
        stl.write("""
        Average number of reply count per Sender in the channel random
        """)
    with right_column:
        stl.pyplot(draw_avg_reply_count(message_with_user))
with stl.container():
    stl.write("---")
    left_column, right_column = stl.columns([0.3, 0.7])
    with left_column:
        stl.header("Task 2")
        stl.write("##")
        stl.write("""
        Histogram of the time difference between Consecutive messages
        """)
    with right_column:
        message_with_user["time_difference"] = message_with_user.groupby("msg_type")["msg_sent_standard_time"].diff()

        # Plot the histogram
        fig, ax = plt.subplots()
        ax.hist( message_with_user[message_with_user["msg_type"] == 'message']["time_difference"].dt.total_seconds() / 60,
                bins=10,
                edgecolor='black')
        ax.set_title('Time Differences between Consecutive Messages')
        ax.set_xlabel('Time Difference (minutes)')
        ax.set_ylabel('Frequency')
        # Display the plot using Streamlit
        stl.pyplot(fig)
with stl.container():
    stl.write("---")
    left_column, right_column = stl.columns([0.3, 0.7])
    with left_column:
        stl.header("Task 2")
        stl.write("##")
        stl.write("""
        Histogram of the time difference between Consecutive replys of a message
        """)
    with right_column:
        fig, ax = plt.subplots()
        ax.hist(combined_df['time_difference'].dt.total_seconds() / 60, bins=15, edgecolor='black')
        ax.set_title('Time Differences between Consecutive Replies (Combined Data)')
        ax.set_xlabel('Time Difference (minutes)')
        ax.set_ylabel('Frequency')

        # Display the plot using Streamlit
        stl.pyplot(fig)
