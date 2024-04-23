# custom module for vaccine app
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

class Vaccine():
    '''
    Class properties store data set, store filter options for vaccines and geographic areas, and store user-selected option for each filter
    Class methods read in data set, read in geographic area data, generate dynamic filter options dependent on other filters, and generate visualizations
    '''
    def __init__(self, df_csv):
        self.data = self.fix_data(df_csv)
        self.vacc_options = self.get_vacc_options()
        self.geo_options = self.get_geo_options()
        self.vacc_option = None
        self.dose_option = None
        self.age_option = None
        self.geo_option = None
        self.soc_dem_option = None
        self.soc_dem_dose = None

    @st.cache_data
    def fix_data(_self, df_csv):
        '''
        Perform data cleaning for one data type as result of reading in data and return cleaned CSV back to self
        '''
        try:
            # convert Birth Year into string (otherwise will display as float value in charts)
            # first convert into nullable Integer and then into String
            df_csv['Birth Year'] = np.where(pd.isnull(df_csv['Birth Year']), df_csv['Birth Year'], df_csv['Birth Year'].astype('Int64').astype(str))

            return df_csv
        
        except:
            st.write('Error processing vaccine data file')
            return None
    
    @st.cache_data
    def get_vacc_options(_self):
        '''
        Get and return vaccine options for filter
        '''
        try:
            vacc_options = tuple(_self.data['Vaccine'].unique())
            return vacc_options
        
        except:
            st.write('Error generating vaccine options')
            return None            

    @st.cache_data
    def get_geo_options(_self):
        '''
        Get and return geographic area options for chart filter
        Order contained in separate csv file created from dataset because preferred order is unique (not strictly alphabetical)
        Order = US first, then HHS Regions by number, then States alphabetically with City/County breakouts ordered after their state
        '''
        try:
            df_geo_areas = pd.read_csv('./data/geo_areas_order.csv')

            # filter out HHS Regions and Territories (Guam, Puerto Rico) because sociodemographic data is NOT available for those
            filter_regions_territories = (df_geo_areas['geo_area'].str.contains('HHS Region') == False) & \
                (df_geo_areas['geo_area'] != 'Guam') & (df_geo_areas['geo_area'] != 'Puerto Rico')
            
            geo_options_ordered = tuple(df_geo_areas[filter_regions_territories]['geo_area'].unique())

            return geo_options_ordered
        
        except:
            st.write('Error reading geographic data file')
            return None            

    def get_dose_options(self):
        '''
        Get and return dose options for dose selection filter based on selected vaccine
        '''
        filter_vacc = (self.data['Vaccine'] == self.vacc_option)
        dose_options = tuple(self.data[filter_vacc]['Dose'].unique())

        return dose_options

    def get_age_options(self):
        '''
        Get and return age options for age selection filter based on selected vaccine and dose
        '''   
        filter_age = (self.data['Vaccine'] == self.vacc_option) & (self.data['Dose'] == self.dose_option) & (self.data['Birth Year'].notna())

        age_options = tuple(self.data[filter_age]['Age'].unique())

        return age_options

    def get_soc_dem_dose_options(self):
        '''
        Get and return dose options and default option index for sociodemographic chart filter
        '''
        # apply selected vaccine filter to generate data subset that only includes the 2 four-year birth cohorts (which have sociodemographic data)
        filter_soc_dem_data = (self.data['Vaccine'] == self.vacc_option) & ((self.data['Birth Cohort'] == '2014-2017') | (self.data['Birth Cohort'] == '2016-2019'))

        soc_dem_data = self.data[filter_soc_dem_data]

        # get available doses for vaccine within sociodemographic data (might be subset of doses for selected vaccine)
        soc_dem_dose_options = tuple(soc_dem_data['Dose'].unique())

        # if available, select previous dose; otherwise default to first available dose option
        if self.dose_option in soc_dem_dose_options:
            dose_index = soc_dem_dose_options.index(self.dose_option)
        else:
            dose_index = 0
        
        return soc_dem_dose_options, dose_index

    def show_choropleth_map(self):
        '''
        Choropleth map displays estimated vaccination rate (%) for each state for Birth Year 2020
        Data filtered by selections for vaccine, dose, and age checkpoint
        '''
        # apply selected filters to generate data subset for choropleth map
        filter_map = (self.data['Vaccine'] == self.vacc_option) & (self.data['Dose'] == self.dose_option) & (self.data['Age'] == self.age_option) & \
            (self.data['Birth Year'] == '2020') & (self.data['State'].notna())
        map_data = self.data[filter_map]

        # title for choropleth map
        st.markdown('##### :green[' + self.vacc_option + '] Vaccination Rates by State')
        st.markdown('##### :green[' + self.dose_option + '] by Age :green[' + self.age_option + '] for Children Born in 2020')

        # generate and show choropleth map
        fig_map = px.choropleth(map_data, locations = 'State', color = 'Estimate (%)', color_continuous_scale = 'temps_r', locationmode = 'USA-states', scope = 'usa')

        st.plotly_chart(fig_map, use_container_width=True, config = {'displayModeBar': False})

        return

    def show_line_graph(self):
        '''
        Line graph displays estimated vaccination rate (%) for each birth year (2011-2020)
        Data filtered by selections for vaccine, dose, age checkpoint, and geographic area
        Estimated vaccination rate for entire United States will also be plotted for comparison
        '''
        # apply selected filters to generate data subset for line graph (include United States for comparison to selected Geographic Area)
        filter_line = (self.data['Vaccine'] == self.vacc_option) & (self.data['Dose'] == self.dose_option) & (self.data['Age'] == self.age_option) & \
            ((self.data['Geographic Area'] == 'United States') | (self.data['Geographic Area'] == self.geo_option)) & (self.data['Birth Year'].notna())

        line_data = self.data[filter_line]

        # title for line graph
        st.markdown('##### :green[' + self.vacc_option + '] Vaccination Rates by Birth Year')
        st.markdown('##### :green[' + self.dose_option + '] by Age :green[' + self.age_option + '] in :blue[' + self.geo_option +']')

        # generate and show line graph
        fig_line = px.line(line_data, x = 'Birth Year', y = 'Estimate (%)', color = 'Geographic Area')
        fig_line.update_layout(yaxis_range=[0,100]) # use 0-100 for y-axis scale
        fig_line.update_xaxes(type='category') # display all values for x-axis by designating as categories

        st.plotly_chart(fig_line, use_container_width=True, config = {'displayModeBar': False})

        return

    def show_bar_chart(self):
        '''
        Bar chart displays estimated vaccination rate (%) for four-year birth cohorts (2014-2017 & 2016-2019)
        Data filtered by selections for vaccine, dose, age checkpoint, geographic area, and sociodemographic variable
        Note: Sociodemographic data only available for four-year birth cohorts (representing age 24 months) and only for certain doses and geographic areas
        '''
        # apply selected filters to generate data subset that only includes four-year birth cohorts 
        filter_soc_dem_data = (self.data['Vaccine'] == self.vacc_option) & \
            ((self.data['Birth Cohort'] == '2014-2017') | (self.data['Birth Cohort'] == '2016-2019')) & \
            (self.data['Dose'] == self.soc_dem_dose) & (self.data['Geographic Area'] == self.geo_option)
        
        soc_dem_data = self.data[filter_soc_dem_data]

        # get filter that matches selection (and get array for preferred order of categories in bar chart)
        match self.soc_dem_option:
            case 'Race and Ethnicity':
                filter_soc_dem_var = (soc_dem_data['Race and Ethnicity'].notna())
                soc_dem_array = ['Black, Non-Hispanic', 'Hispanic', 'White, Non-Hispanic', 'Other or Multiple Races, Non-Hispanic']
            case 'Poverty Level':
                filter_soc_dem_var = (soc_dem_data['Poverty Level'].notna())
                soc_dem_array = ['<133% FPL', '133% to <400% FPL', '>400% FPL']
            case 'Health Insurance Coverage':
                filter_soc_dem_var = (soc_dem_data['Health Insurance Coverage'].notna())
                soc_dem_array = ['Uninsured', 'Any Medicaid', 'Private Insurance Only', 'Other']
            case 'Urbanicity':
                filter_soc_dem_var = (soc_dem_data['Urbanicity'].notna())
                soc_dem_array = ['Living In a MSA Principal City', 'Living In a MSA Non-Principal City', 'Living In a Non-MSA']

        # apply selected filter to generate data subset for bar chart
        soc_dem_bar_data = soc_dem_data[filter_soc_dem_var]

        # title for bar chart
        st.markdown('##### :green[' + self.vacc_option + '] Vaccination Rates by :violet[' + self.soc_dem_option + ']')
        st.markdown('##### :violet[' + self.soc_dem_dose + '] by Age 24 Months* for Two Birth Cohorts in :blue[' + self.geo_option + ']')

        # generate and show bar chart
        fig_bar = px.bar(soc_dem_bar_data, x = self.soc_dem_option, y = 'Estimate (%)', color = 'Birth Cohort', barmode = 'group')
        fig_bar.update_layout(yaxis_range=[0,100]) # use 0-100 for y-axis scale
        fig_bar.update_xaxes(categoryorder = 'array', categoryarray = soc_dem_array) # set preferred order for x-axis categories

        st.plotly_chart(fig_bar, use_container_width=True, config = {'displayModeBar': False})

        return