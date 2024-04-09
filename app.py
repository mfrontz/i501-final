# Python libraries
import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
#from dotenv import load_dotenv

#from utils.b2 import B2

# ------------------------------------------------------
#                      FUNCTIONS (Move to module)
# ------------------------------------------------------

def read_data():
    '''
    Read data from CSV and perform additional cleaning for data types as result of reading in data
    '''
    df_csv = pd.read_csv('./data/child_vaccination_data_cleaned.csv')

    # convert Birth Year into string (so not displayed as float in charts)
    # first convert into nullable Integer and then into String (otherwise Streamlit changes Int64 back into float in charts)
    df_csv['Birth Year'] = np.where(pd.isnull(df_csv['Birth Year']), df_csv['Birth Year'], df_csv['Birth Year'].astype('Int64').astype(str))

    # convert Sample Size column from float to integer
    df_csv['Sample Size'] = df_csv['Sample Size'].astype('Int64')

    return df_csv

def get_geo_options():
    '''
    Get and return geographic area options for chart filter
    Order contained in separate csv file created from dataset because preferred order is unique (not strictly alphabetical)
    Order = US first, then HHS Regions by number, then States alphabetically with City/County breakouts ordered after their state
    '''
    df_geo_areas = pd.read_csv('./data/geo_areas_order.csv')
    geo_options_ordered = tuple(df_geo_areas['geo_area'].unique())

    return geo_options_ordered

# ------------------------------------------------------
#                      APP CONSTANTS
# ------------------------------------------------------
#REMOTE_DATA = 'child_vaccination_data_cleaned.csv'

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

#df_vacc = get_data() # function in B2 to get data from remote server

df_vacc = read_data()

# INTRODUCTION

st.title(':rainbow[Protecting Children\'s Health]')
st.subheader('Vaccination Rates for Young Children in the United States')
st.image('./data/toddler-vaccination.jpg')
st.caption('''Photo Credit: [SELF x American Academy of Pediatrics Vaccine Photo Project](https://www.flickr.com/photos/selfmagazine/albums/72157710332198661/)''')

st.markdown('''[To protect young children from serious (and potential life-threatening) diseases](https://www.cdc.gov/vaccines/parents/diseases/index.html), \
the Centers for Disease Control and Prevention (CDC) recommends that children receive all necessary doses for these 10 vaccines by the time they reach 2 years of age:
- **DTaP vaccine** to protect against diphtheria, tetanus, and whooping cough (pertussis) 
- **Hep A vaccine (HAV)** to protect against hepatitis A
- **Hep B vaccine (HBV)** to protect against hepatitis B
- **Hib vaccine** to protect against *Haemophilus influenzae* type b
- **Influenza vaccine** to protect against seasonal flu
- **MMR vaccine** to protect against measles, mumps, and German measles (rubella)
- **PCV** to protect against pneumococcal disease
- **Polio vaccine** to protect against polio
- **Rotavirus vaccine** to protect against rotavirus
- **Varicella zoster vaccine** to protect against chicken pox''')

st.caption('''Note: The **Combined 7-vaccine series** includes all necessary doses for:  DTaP, Hep B, Hib, MMR, PCV, Polio, and Varicella.''')

st.markdown(''':rainbow[**How many young children in the United States receive these recommended vaccinations?**]''')
st.markdown('''- Use the interactive charts in this web app to explore CDC data on child vaccination rates''')

st.divider()

# CHOROPLETH MAP
# choropleth map displays estimated vaccination rate (%) for each state for Birth Year 2020
# user can select filters for vaccine, vaccine dose, and age checkpoint

st.subheader('How do child vaccination rates compare across states?')

# select filter for vaccine type
vacc_options = tuple(df_vacc['Vaccine'].unique())
vacc_option = st.selectbox('Select Vaccine', vacc_options, help = 'Vaccines recommended for children by the time they reach 2 years of age')
filter_vacc = (df_vacc['Vaccine'] == vacc_option)

# select filter for vaccine dose (based on selected vaccine)
dose_options = tuple(df_vacc[filter_vacc]['Dose'].unique())
dose_option = st.selectbox('Select Dose', dose_options, help = 'Options for dose depend on selected vaccine')

# select filter for age checkpoint (based on selected vaccine and dose
# note: age checkpoint data are only available in dataset for Birth Year (not Birth Cohort)
filter_age = (df_vacc['Vaccine'] == vacc_option) & (df_vacc['Dose'] == dose_option) & (df_vacc['Birth Year'].notna())
age_options = tuple(df_vacc[filter_age]['Age'].unique())
age_option = st.selectbox('Select Age Checkpoint', age_options, help = 'Options for age checkpoint depend on selected vaccine and dose')

# apply selected filters to generate data subset for choropleth map
filter_map = (df_vacc['Vaccine'] == vacc_option) & (df_vacc['Dose'] == dose_option) & (df_vacc['Age'] == age_option) & (df_vacc['Birth Year'] == '2020') & (df_vacc['State'].notna())
map_data = df_vacc[filter_map]

# display choropleth map
st.markdown('#### :blue[' + vacc_option + '] Vaccination Rates by State')
st.markdown('##### :blue[' + dose_option + '] by Age :blue[' + age_option + '] for Children Born in 2020')

fig_map = px.choropleth(map_data, locations = 'State', color = 'Estimate (%)', color_continuous_scale = 'temps_r', locationmode = 'USA-states', scope = 'usa')

st.plotly_chart(fig_map, use_container_width=True)

st.divider()

# LINE GRAPH
# line graph displays estimated vaccination rate (%) for each birth year (2011-2020)
# vaccine, dose, and age checkpoint based on filters selected for choropleth map
# user can select filter for geographic area
# estimated vaccination rate for entire United States will also be plotted for comparison

st.subheader('How do child vaccination rates compare by year of birth?')

# select filter for geographic area (can set default to specific value, such as: index = 28)
geo_options = get_geo_options()
geo_option = st.selectbox('Select Geographic Area *(such as HHS Region, State, etc.)*', \
                          geo_options, help = 'Options include: United States, HHS Region, State, Territory, and certain City/County breakouts')

# provide way to view map of HHS Regions
# note: US Dept HHS divides states into 10 regions for data analysis purposes
with st.popover('View Map of HHS Regions'):
    st.image('./data/hhs-regions.png', caption='United States Department of Health and Human Services (HHS) Regions')

# apply selected filters to generate data subset for line graph (include United States for comparison to selected Geographic Area)
filter_line = (df_vacc['Vaccine'] == vacc_option) & (df_vacc['Dose'] == dose_option) & (df_vacc['Age'] == age_option) & \
    ((df_vacc['Geographic Area'] == 'United States') | (df_vacc['Geographic Area'] == geo_option)) & (df_vacc['Birth Year'].notna())

line_data = df_vacc[filter_line]

# display line graph
st.markdown('#### :blue[' + vacc_option + '] Vaccination Rates by Birth Year')
st.markdown('##### :blue[' + dose_option + '] by Age :blue[' + age_option + '] in :blue[' + geo_option +']')

fig_line = px.line(line_data, x = 'Birth Year', y = 'Estimate (%)', color = 'Geographic Area')
fig_line.update_layout(yaxis_range=[0,100]) # use 0-100 for y-axis scale
fig_line.update_xaxes(type='category') # display all values for x-axis by designating as categories

st.plotly_chart(fig_line, use_container_width=True)

st.divider()

# BAR CHART
# bar chart displays estimated vaccination rate (%) for 2 four-year birth cohorts (2014-2017 & 2016-2019)
# vaccine and dose based on filters selected for choropleth map
# user can select filter for socio-demographic variable
# note: socio-demographic data are only available in dataset for the 2 four-year birth cohorts
# note: estimated vaccination rates (%) for four-year birth cohorts are only available for 2 year (24 months) age checkpoint

st.subheader('How do child vaccination rates compare based on sociodemographic factors?')

# apply previous filters (vaccine, dose, geographic area - but not age) to generate data subset that only includes 2 four-year birth cohorts 
filter_soc_dem_data = (df_vacc['Vaccine'] == vacc_option) & (df_vacc['Dose'] == dose_option) & (df_vacc['Geographic Area'] == geo_option) & \
    ((df_vacc['Birth Cohort'] == '2014-2017') | (df_vacc['Birth Cohort'] == '2016-2019'))

soc_dem_data = df_vacc[filter_soc_dem_data]

# select filter for socio-demographic variable
soc_dem_option = st.selectbox('Select Sociodemographic Factor', ('Race and Ethnicity', 'Poverty Level', 'Health Insurance Coverage', 'Urbanicity'))

# get filter that matches selection (and get array for preferred order of categories in bar chart)
match soc_dem_option:
    case 'Race and Ethnicity':
        filter_soc_dem_var = soc_dem_data['Race and Ethnicity'].notna()
        soc_dem_array = ['Black, Non-Hispanic', 'Hispanic', 'White, Non-Hispanic', 'Other or Multiple Races, Non-Hispanic']
    case 'Poverty Level':
        filter_soc_dem_var = soc_dem_data['Poverty Level'].notna()
        soc_dem_array = ['<133% FPL', '133% to <400% FPL', '>400% FPL']
    case 'Health Insurance Coverage':
        filter_soc_dem_var = soc_dem_data['Health Insurance Coverage'].notna()
        soc_dem_array = ['Uninsured', 'Any Medicaid', 'Private Insurance Only', 'Other']
    case 'Urbanicity':
        filter_soc_dem_var = soc_dem_data['Urbanicity'].notna()
        soc_dem_array = ['Living In a MSA Principal City', 'Living In a MSA Non-Principal City', 'Living In a Non-MSA']

# apply selected filter to generate data subset for bar chart
soc_dem_bar_data = soc_dem_data[filter_soc_dem_var]

# display bar chart
st.markdown('#### :blue[' + vacc_option + '] Vaccination Rates by :blue[' + soc_dem_option + ']')
st.markdown('##### :blue[' + dose_option + '] by Age 24 Months for Two Birth Cohorts in :blue[' + geo_option +']')

fig_bar = px.bar(soc_dem_bar_data, x = soc_dem_option, y = 'Estimate (%)', color = 'Birth Cohort', barmode = 'group')
fig_bar.update_layout(yaxis_range=[0,100]) # use 0-100 for y-axis scale
fig_bar.update_xaxes(categoryorder = 'array', categoryarray = soc_dem_array) # set preferred order for x-axis categories

st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

st.subheader('How can I learn more about vaccinations for children?')

st.markdown('''The CDC has a [website to help parents learn more about vaccines for their children]\
(https://www.cdc.gov/vaccines/parents/), including:
- Why vaccines are important for protecting children's health
- Recommended vaccine schedules by child age
- Advice for preparing for your child's vaccine visit
- Answers to common questions about childhood vaccines
- Other resources to help parents make healthy choices for their children''')

st.divider()

# MVP - ISSUES AND NEXT STEPS
# temp - remove for final app

st.subheader(':red[Issues with MVP]')
st.markdown('''- Need to solve issue connecting to remote cloud storage service to access data file
    - Can connect to remote server on local machine but not on Streamlit Cloud
    - Currently storing and accessing data file stored on GitHub''')

st.subheader(':green[Next Steps for MVP]')
st.markdown('''- Connect to remote cloud storage: will try using requirements.txt instead of environment.yml
- Add or modify content as necessary to ensure users understand context and intent of app, can interact with app easily, and can interpret visualizations easily and accurately
- Experiment with different content layout (such as using sidebar to house data filters, etc.)
- Need to refactor code to include error handling, at least one class, and a module with several functions
- Create `README.md` file for GitHub repository describing project''')

st.divider()

# FOOTER
st.caption('Original Dataset: [Vaccination Coverage Among Young Children (0-35 Months)](https://data.cdc.gov/Child-Vaccinations/Vaccination-Coverage-among-Young-Children-0-35-Mon/fhky-rtsk/about_data) (data last updated November 3, 2023)')
st.caption('Copyright © 2024 Michael Frontz')
st.caption('''This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).  
           You are free to use, share, or adapt this material for non-commercial purposes as long as you provide proper attribution and distribute any copies or adaptations under this same license.''')