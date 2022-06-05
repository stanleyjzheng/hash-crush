import streamlit as st
from passlib.hash import pbkdf2_sha256
import sqlite3 as sql
import extra_streamlit_components as stx
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb


def streamlit_page_config():
    st.set_page_config(page_title="Hash Crush", page_icon="❤️")

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)



def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 81px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="white",
        text_align="center",
        height="auto",
        opacity=1
    )

    style_hr = styles(
        display="block",
        # margin=px(3, 3, "auto", "auto"),
        margin=px(0, 0, 10, 0),
        border_style="inset",
        border_width=px(2)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def footer():
    myargs = [
        "<>",
        " with ❤️ by ",
        link("https://twitter.com/0xlmeow", "@0xlmeow"),
        br(),
        "contribute on ",
        link("https://github.com/stanleyjzheng/hash-crush", "github")
    ]
    layout(*myargs)


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


def get_event(event_id):
    conn = sql.connect('crush.db')
    c = conn.cursor()
    c.execute("SELECT * FROM crush WHERE event_id = ?", (event_id,))
    entry = c.fetchall()
    conn.close()
    return entry


def generate_db():
    conn = sql.connect('crush.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS crush (id INTEGER PRIMARY KEY AUTOINCREMENT, your_name_hash TEXT, crush_names_hash TEXT, event_id TEXT)")
    conn.commit()
    conn.close()