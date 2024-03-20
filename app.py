#import os

import pandas as pd
import numpy as np

import streamlit as st
#from dotenv import load_dotenv

# ------------------------------------------------------
#                      APP CONSTANTS
# ------------------------------------------------------
DATA_FILE = 'vaccination_data_lab9.csv'

# ------------------------------------------------------
#                         APP
# ------------------------------------------------------

st.title('Vaccinations Among Young Children')

df_vacc = pd.read_csv(DATA_FILE)

st.dataframe(df_vacc)