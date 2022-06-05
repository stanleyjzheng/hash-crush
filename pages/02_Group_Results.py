import streamlit as st
from passlib.hash import pbkdf2_sha256
import random
import string
import sqlite3 as sql
import extra_streamlit_components as stx


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


def get_event_ids():
    conn = sql.connect('crush.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT event_id FROM crush")
    event_ids = c.fetchall()
    conn.close()
    return event_ids


def get_event(event_id):
    conn = sql.connect('crush.db')
    c = conn.cursor()
    c.execute("SELECT * FROM crush WHERE event_id = ?", (event_id,))
    entry = c.fetchall()
    conn.close()
    return entry


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
st.markdown('''
Enter your name here to get your results.
''')

group_id = st.text_input("Group ID")
your_name = st.text_input("Your name (first and last)").lower()

if group_id not in [i[0] for i in get_event_ids()] and len(group_id)> 0:
    st.error("Group ID has not been used before. If you would like to create a Group ID, please go back to the Group Submit page. Otherwise, please ammend your group ID.")

button = st.button("Submit")
cookie_manager = get_manager()
cookies = cookie_manager.get_all()

if button:
    event = get_event(group_id)
    user_name = [i for i in event if verify_text(i[1], your_name)]
    crush_names = cookies['crush_names']
    if len(user_name) == 0:
        st.error("Your name is not in the group. Please try again.")
    else:
        user_name = user_name[-1]
        print(user_name)
        matches = []
        for user in event:
            all_crushes = user[2].split('|')
            for hsh in all_crushes:
                if verify_text(hsh, your_name):
                    for crush_name in crush_names:
                        if verify_text(user[1], crush_name):
                            matches.append(crush_name)
        if len(matches) > 0:
            st.success(f"Amazing! You are a match for {', '.join(matches)}")
        else:
            st.error("Sorry, no matches.")
