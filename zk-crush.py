import streamlit as st
from hashlib import sha256

st.set_page_config(page_title="ZK Crush", page_icon="❤️")

st.markdown("<style> table { margin: 0 auto; } </style>", unsafe_allow_html=True)
st.markdown('<style> [data-testid="stImage"], table { margin: 0 auto; } </style>', unsafe_allow_html=True)
st.markdown("<style> .reportview-container .main footer {visibility: hidden;}    #MainMenu {visibility: hidden;}</style>", unsafe_allow_html=True)

st.write('<h1 style="font-weight:900; color:#d08770; font-size: 60px">ZK Crush</h1>', unsafe_allow_html=True)
st.write('<div style="font-size: 20px; font-weight: 400;"> How this works </div>', unsafe_allow_html=True)
st.markdown('''
You enter your name and the name of your crush, both of which are hashed.
A unique link is then generated that can be shared publicly, or anonymously. 
People can enter their names into this unique link to generate the hash of their name, as well as the hash of their crush (hopefully you!)
If not, they will be told no match was made and no other info is revealed. 
''')

url = st.experimental_get_query_params()
print(url)
yn = st.text_input("Your name (first and last)").lower()
cn = st.text_input("Your crush's name (first and last)").lower()


if 'selected' in url and len(url['selected']) == 2:
    st.write("Let's see if your crush matches")
    check = st.button("Check crushes")
    if check:
        yn = sha256(yn.encode('utf-8')).hexdigest()
        cn = sha256(cn.encode('utf-8')).hexdigest()
        if cn == url['selected'][0] and yn == url['selected'][1]:
            st.success("You and your crush are a match!")
        else:
            st.error("Sorry, no match.")
else:
    button = st.button("Generate link")
    if button:
        yn = sha256(yn.encode('utf-8')).hexdigest()
        cn = sha256(cn.encode('utf-8')).hexdigest()
        st.success(f"Your link is http://localhost:8501/?selected={yn}&selected={cn}")