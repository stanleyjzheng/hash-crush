import datetime
import os

from dotenv import load_dotenv

from utils import *

load_dotenv()

streamlit_page_config()

st.title("Hash Crush")
st.write('<div style="font-size: 20px; font-weight: 400;"> How this works </div>', unsafe_allow_html=True)
st.markdown(f'''
You enter your name and the name of your crush(es), both of which are hashed.
These hashes are stored according to your Group ID.

After everyone has entered their names and their crush's name, move onto the [results page]({os.environ['site_url']}/Group_Results). 

Note that (anonymous), cryptographically secure hashes are saved to eliminate the need for link sharing. Please see [
individual](os.environ['site_url']) for a link-based implementation that does not save any data. Names are 
temporarily stored in your browser's local cookies. ''')

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
    crush_names.append(st.text_input(label="Your crush's name (first and last)", key=i))  # Pass index as key

if group_id not in [i[0] for i in get_event_ids()] and len(group_id) > 0:
    st.warning(
        "Group ID has not been used before. If you would like to proceed, you will be the first one to add your "
        "crushes. Otherwise, please amend your group ID.")

cookie_manager = get_manager()

with st.form(key="Cookie"):
    submitted = st.form_submit_button("/click_for_significant_other")
    hide_streamlit_style = """
    <style>
    [data-testid="stForm"] {border: none; padding: 0;}
    </style>
    """
    # incredibly hacky way to prevent st.success from disappearing instantly
    # details here https://discuss.streamlit.io/t/cookies-support-in-streamlit/16144/35?u=stanleyjzheng
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    if submitted:
        cookie_manager.set(cookie='crush_names', val=crush_names, expires_at=datetime.date(2022, 12, 31))
        your_name = hash_text(your_name)
        crush_names = [hash_text(cn) for cn in crush_names]
        crush_names = '|'.join(crush_names)
        add_entry(your_name, crush_names, group_id)
        st.success(
            "Your crush(es) have been added to the database. Proceed to the results page when everyone has submitted "
            "their crushes.")

footer()
