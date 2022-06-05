import streamlit as st
from passlib.hash import pbkdf2_sha256
import random
import string
import sqlite3 as sql
import extra_streamlit_components as stx
import time
import os
from dotenv import load_dotenv
load_dotenv()


@st.cache(allow_output_mutation=True)
def get_manager():
    return stx.CookieManager()


def hash_text(text):
    text = text.lower().strip()
    hs = pbkdf2_sha256.using(rounds=6400).hash(text)
    return hs[20:].replace('$', '')


def verify_text(hs, text):
    text = text.lower().strip()
    hs = f"$pbkdf2-sha256$6400${hs[:-43]}${hs[-43:]}"
    return pbkdf2_sha256.verify(text, hs)


def add_entry(your_name_hash, crush_names_hash, event_id):
    conn = sql.connect('crush.db')
    c = conn.cursor()
    c.execute("INSERT INTO crush VALUES (?, ?, ?, ?)", (None, your_name_hash, crush_names_hash, event_id))
    conn.commit()
    conn.close()


def get_event_ids():
    conn = sql.connect('crush.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT event_id FROM crush")
    event_ids = c.fetchall()
    conn.close()
    return event_ids


st.set_page_config(page_title="Hash Crush", page_icon="❤️")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.write('<h1 style="font-weight:900; color:#d08770; font-size: 60px">Hash Crush</h1>', unsafe_allow_html=True)
st.write('<div style="font-size: 20px; font-weight: 400;"> How this works </div>', unsafe_allow_html=True)
st.markdown(f'''
You enter your name and the name of your crush(es), both of which are hashed.
These hashes are stored according to your Group ID.

After everyone has entered their names and their crush's name, move onto the [results page]({os.environ['site_url']}/Group_Results).

Note that (anonymous), cryptographically secure hashes are saved to eliminate the need for link sharing. Please see [individual](os.environ['site_url']) for a link-based implementation that does not save any data.
Names are temporarily stored in your browser's local cookies.
''')

group_id = st.text_input("Group ID")
your_name = st.text_input("Your name (first and last)").lower()
crush_names = []

if 'n_rows' not in st.session_state:
    st.session_state.n_rows = 1

add = st.button(label="Add more crushes")

if add:
    st.session_state.n_rows += 1
    st.experimental_rerun()

for i in range(st.session_state.n_rows):
    crush_names.append(st.text_input(label="Your crush's name (first and last)", key=i)) #Pass index as key

if group_id not in [i[0] for i in get_event_ids()] and len(group_id)> 0:
    st.warning("Group ID has not been used before. If you would like to proceed, you will be the first one to add your crushes. Otherwise, please ammend your group ID.")

cookie_manager = get_manager()

with st.form(key="Cookie"):
    submitted = st.form_submit_button("Submit")
    hide_streamlit_style = """
    <style>
    [data-testid="stForm"] {border: none; padding: 0;}
    </style>
    """
    # incredibly hacky way to prevent st.success from disappearing instantly
    # details here https://discuss.streamlit.io/t/cookies-support-in-streamlit/16144/35?u=stanleyjzheng
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    if submitted:
        cookie_manager.set(cookie='crush_names', val=crush_names)
        your_name = hash_text(your_name)
        crush_names = [hash_text(cn) for cn in crush_names]
        crush_names = '|'.join(crush_names)
        add_entry(your_name, crush_names, group_id)
        st.success("Your crush(es) have been added to the database. Proceed to the results page when everyone has submitted their crushes.")
