import streamlit as st
from passlib.hash import pbkdf2_sha256
import random
import string

def hash_text(text):
    hs = pbkdf2_sha256.using(rounds=6400).hash(text)
    return hs[20:].replace('$', '')

def verify_text(hs, txt):
    hs = f"$pbkdf2-sha256$6400${hs[:-43]}${hs[-43:]}"
    return pbkdf2_sha256.verify(txt, hs)


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
You enter your name and the name of your crush, both of which are hashed.
A unique link is then generated that can be shared publicly, or anonymously (a school confessions page is a great place). 
People can enter their names into this unique link to generate the hash of their name, as well as the hash of their crush (hopefully you!)
If not, they will be told no match was made and no other info is revealed. 
''')

url = st.experimental_get_query_params()
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

if 'selected' in url and len(url['selected']) > 1:
    url_your_name = url['selected'][0]
    url_crush_names = url['selected'][1:]
    st.write("Let's see if your crush matches")
    check = st.button("Check crushes")
    if check:
        your_name_result = [verify_text(url_crush_name, your_name) for url_crush_name in url_crush_names]
        crush_names_result = [verify_text(url_your_name, crush_name) for crush_name in crush_names]
        if any(your_name_result) and any(crush_names_result):
            nm = crush_names[crush_names_result.index(True)]
            st.success(f"You and {nm} are a match!")
        else:
            st.error("Sorry, no match.")
else:
    button = st.button("Generate link")
    if button:
        your_name = hash_text(your_name)
        crush_names = [hash_text(cn) for cn in crush_names]
        crush_names = '&selected=' + '&selected='.join(crush_names)
        st.success(f"Your link is http://localhost:8501/?selected={your_name}{crush_names}")