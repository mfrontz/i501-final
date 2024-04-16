# Python libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# custom module and class
from vaccine import Vaccine

import os
from dotenv import load_dotenv
#from utils.b2 import B2

# ------------------------------------------------------
#                      APP CONSTANTS
# ------------------------------------------------------
#REMOTE_DATA = 'child_vaccination_data_cleaned.csv'

# ------------------------------------------------------
#                        CONFIG
# ------------------------------------------------------
load_dotenv()

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

#df_vacc = get_data() # function in B2 to get data from remote server

st.set_page_config(page_title = 'Child Vaccinations', page_icon = None)

# create object using custom class Vaccine
vax = Vaccine()

# SIDEBAR WITH FILTERS
with st.sidebar:

    st.caption(':green[**⬇ Choose which vaccine data are shown**]')

    vax.vacc_option = st.selectbox(':green[Select Vaccine]', vax.vacc_options, index = 1, help = 'Vaccines recommended for children by the time they reach 2 years of age')

    vax.dose_option = st.selectbox(':green[Select Dose]', vax.get_dose_options(), help = 'Options for dose depend on selected vaccine')

    vax.age_option = st.selectbox(':green[Select Age Checkpoint]', vax.get_age_options(), help = 'Options for age checkpoint depend on selected vaccine and dose')

    st.caption(':blue[**⬇ For line graph and bar chart only**]')

    vax.geo_option = st.selectbox(':blue[Select Geographic Area]', vax.geo_options, index = 1, help = 'Options include: United States, specific State, or certain City/County breakouts')
    
    st.caption(':violet[**⬇ For bar chart only**]')

    vax.soc_dem_option = st.selectbox(':violet[Select Sociodemographic Factor]', ('Race and Ethnicity', 'Poverty Level', 'Health Insurance Coverage', 'Urbanicity'))

    soc_dem_dose_options, dose_index = vax.get_soc_dem_dose_options()

    vax.soc_dem_dose = st.selectbox(':violet[Select Dose *(if dose above not available)*]', soc_dem_dose_options, index = dose_index, help = 'Sociodemographic data only available for certain doses of vaccines')

# TABS
st.subheader(':children_crossing: :rainbow[Protecting Children\'s Health]')
tab1, tab2, tab3, tab4, tab5 = st.tabs([':syringe: Introduction', ':flag-us: Compare States', ':chart_with_upwards_trend: Compare Birth Years', ':bar_chart: Compare Sociodemographics', ':mag_right: Learn More'])

# INTRODUCTION
with tab1:
    st.write('##### What vaccinations should young children receive?')
    st.markdown('''To protect young children from serious (and potential life-threatening) diseases, the Centers for Disease Control and Prevention (CDC) \
                recommend that children in the United States receive all necessary doses of these 10 vaccines by the time they reach 2 years of age:  
- **DTaP vaccine** to protect against diphtheria, tetanus, and whooping cough (pertussis) 
- **Hep A vaccine** to protect against hepatitis A
- **Hep B vaccine** to protect against hepatitis B
- **Hib vaccine** to protect against *Haemophilus influenzae* type b
- **Influenza vaccine** to protect against seasonal flu
- **MMR vaccine** to protect against measles, mumps, and German measles (rubella)
- **PCV** to protect against pneumococcal disease
- **Polio vaccine** to protect against polio
- **Rotavirus vaccine** to protect against rotavirus
- **Varicella zoster vaccine** to protect against chicken pox''')
    st.caption('''Note: **Combined 7-Vaccine Series** includes all doses for: DTaP, Hep B, Hib, MMR, PCV, Polio, and Varicella''')
    st.write(''':red[**⬆ Choose a tab above to compare child vaccination rates by states, birth years, or sociodemographics**]''')

# CHOROPLETH MAP
with tab2:
    st.write('##### :green[How do child vaccination rates compare across states?]')
    st.caption('⬅ Use filters in sidebar to choose which data are shown')
    vax.show_choropleth_map()

# LINE GRAPH
with tab3:
    st.write('##### :blue[How do child vaccination rates compare by year of birth?]')
    st.caption('⬅ Use filters in sidebar to choose which data are shown')
    vax.show_line_graph()

# BAR CHART
with tab4:
    st.write('''##### :violet[How do child vaccination rates compare by sociodemographic factors?]''')
    st.caption('⬅ Use filters in sidebar to choose which data are shown')
    vax.show_bar_chart()
    st.caption('*Sociodemographic data is only available for age 24 months and certain doses of vaccines')
    st.caption('''**FPL** = Federal Poverty Level (lower % FPL = lower family income, higher % FPL = higher family income)  
               **MSA** = Metropolitan Statistical Area (Urban = MSA Principal City, Suburban = MSA Non-Principal City, Rural = Non-MSA)''')

# MORE INFO
with tab5:
    st.write('##### Where can I learn more about vaccinations for children?')
    st.image('./data/toddler-vaccination.jpg', width = 400)
    st.markdown('''The CDC has a [website to help parents learn more about vaccines for their children](https://www.cdc.gov/vaccines/parents/), including:  
- Why vaccines are important for protecting children's health
- Recommended vaccine schedules by child age
- Advice for preparing for your child's vaccine visit
- Answers to common questions about childhood vaccines
- Other resources to help parents make healthy choices for their children''')
    st.caption('''Photo Credit: [SELF x American Academy of Pediatrics Vaccine Photo Project](https://www.flickr.com/photos/selfmagazine/albums/72157710332198661/)''')

# FOOTER
st.divider()
st.caption('Original Dataset: [Vaccination Coverage Among Young Children (0-35 Months)](https://data.cdc.gov/Child-Vaccinations/Vaccination-Coverage-among-Young-Children-0-35-Mon/fhky-rtsk/about_data) (data last updated November 3, 2023)')
st.caption('Copyright © 2024 Michael Frontz')
st.caption('''This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).  
           You are free to use, share, or adapt this material for non-commercial purposes as long as you provide proper attribution and distribute any copies or adaptations under this same license.''')