import os

import pandas as pd
import numpy as np

import streamlit as st
#from dotenv import load_dotenv

#from utils.b2 import B2

# ------------------------------------------------------
#                      APP CONSTANTS
# -----------------------------------------------------
REMOTE_DATA = 'vaccination_data_lab9.csv'

# ------------------------------------------------------
#                        CONFIG
# ------------------------------------------------------
#load_dotenv()

# load Backblaze connection
#b2 = B2(endpoint=os.environ['B2_ENDPOINT'],
#        key_id=os.environ['B2_KEYID'],
#        secret_key=os.environ['B2_APPKEY'])

# ------------------------------------------------------
#                        CACHING
# ------------------------------------------------------
#@st.cache_data
#def get_data():
#    b2.set_bucket(os.environ['B2_BUCKETNAME'])
#    df_remote = b2.get_df(REMOTE_DATA)
#    return df_remote

# ------------------------------------------------------
#                         APP
# ------------------------------------------------------

st.title('Vaccinations Among Young Children in the United States')

#df_vacc = get_data()
df_vacc = pd.read_csv('vaccination_data_lab9.csv')
df_vacc['Birth Year'] = df_vacc['Birth Year'].astype(str)

st.header('MMR Vaccination Rate')
st.markdown('''The CDC recommends that children receive their 1st dose of MMR vaccine (Measles, Mumps, and Rubella)  
            at 12-15 months of age, and their second dose at 4-6 years of age.''')
st.caption('For children born in 2020, how many had received their 1st dose of MMR vaccine by various age checkpoints?')

mask = ((df_vacc['Birth Year'] == '2020') &
        (df_vacc['Vaccine'] == 'MMR'))

chart_data = df_vacc[mask]

st.bar_chart(chart_data, x = 'Age', y = 'Estimate (%)')

st.markdown('''In 2024, [cases of measles](https://www.cdc.gov/measles/cases-outbreaks.html) have been reported among unvaccinated children in multiple states.''')

st.header('View of Data Subset')
st.dataframe(df_vacc)