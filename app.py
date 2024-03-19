import os

import streamlit as st
from dotenv import load_dotenv

from utils.b2 import B2

# ------------------------------------------------------
#                      APP CONSTANTS
# ------------------------------------------------------
#REMOTE_DATA = 'data_file.csv'

# ------------------------------------------------------
#                        CONFIG
# ------------------------------------------------------
load_dotenv()

# load Backblaze connection
#b2 = B2(endpoint=os.environ['B2_ENDPOINT'],
#        key_id=os.environ['B2_KEYID'],
#       secret_key=os.environ['B2_APPKEY'])

# ------------------------------------------------------
#                        CACHING
# ------------------------------------------------------
#@st.cache_data
#def get_data():
#    b2.set_bucket(os.environ['B2_BUCKETNAME'])
#    df_data = b2.get_df(REMOTE_DATA)
#    return df_data

# ------------------------------------------------------
#                         APP
# ------------------------------------------------------

st.title('Vaccinations Among Young Children')
