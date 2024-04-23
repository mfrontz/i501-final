# Protecting Children's Health

<a href="https://child-vaccinations.streamlit.app/" target="_blank">child-vaccinations.streamlit.app</a>

## Overview

This web app allows users to conduct their own exploratory data analysis of a CDC dataset on vaccination rates of young children in the United States.

The app provides interactive data visualizations that users can customize by changing data filters for vaccine, dose, age checkpoint, geographic location (such as United States, specific state, etc.), and sociodemographic factor (such as race/ethnicity, poverty level, etc.).

The app also provides an overview of the recommended vaccinations for young children and links to a CDC website on child vaccinations designed for parents.

The goal of the app is allow users to explore differences in vaccination rates, which may lead them to want to find answers to questions such as:

- What barriers prevent children from receiving their recommended vaccinations?
- What happens if children don't receive their recommended vaccinations?
- How can we ensure more children receive their recommended vaccinations?

## Data Description

The original dataset used in this web app was downloaded from the <a href="https://data.cdc.gov/Child-Vaccinations/Vaccination-Coverage-among-Young-Children-0-35-Mon/fhky-rtsk/about_data" target="_blank">CDC Data Catalog</a>. 

The following steps were performed to clean and prepare the data for use in the web app:

- Pivoted a column named "Dimension Type" (and its corresponding column of values named "Dimension") into multiple columns, as the CDC used this column to store data for multiple sociodemographic variables
- Split a column named "Birth Year/Birth Cohort" into two distinct columns because some of the other columns in the dataset are only applicable to birth years, while other columns are only applicable to birth cohorts
- Dropped rows that were missing data for the column named "Estimated (%)" which is the core data used in all the data visualizations (this only dropped 58 rows out of 118423 total rows)
- Filled blank values for doses of certain vaccines based on CDC documentation that explained what those blank values actually represent (e.g., the "Combined 7 Series" vaccine did not list a dose value, but the rows for this vaccine represent children who have received the "Full Series" of this vaccine, etc.)
- Renamed certain columns to make them more clear (e.g., renamed "Geography" column to "Geographic Area", renamed "Insurance Coverage" column to "Health Insurance Coverage", etc.)
- Added a new column for state abbreviation by translating any state names in the "Geographic Area" column to their corresponding two-letter abbreviation. This was needed for the choropleth map of the United States, which requires state abbreviations to plot data values in the map.

## Algorithm Description

The app presents 3 pre-designed data visualizations (choropleth map, line graph, and bar chart) which the user can customize using a set of data filters.

The variables used in the data visualizations are set by the filter selections, so when the user changes a filter selection, the visualizations update automatically in real-time.

In addition, there are dependencies among certain filters. For example, the choice of vaccine determines what choices are available for vaccine dose. The choice of vaccine dose affects what choices are available for the age checkpoints. So functions are used to dynamically update the choices of a "child" filter whenever its "parent" filter is changed.

## Tools Used

- The app is built in Python using the Streamlit library
- Pandas and Numpy functions are used for data manipulation in the app
- Plotly Express is used for producing the data visualizations in the app
- Streamlit Community Cloud is used to host the app

## Ethical Concerns

Overall, the data presented in the app is as accurate as possible, but it may not represent the current actual vaccination status of children across the United States.

The web app uses the most recent CDC data available at the time of this project (i.e., as of spring 2024).

The data available within the original dataset is limited by how it is collected. For example, the most recent birth year available in the dataset is 2020 as the CDC collects data on children up to 3 years after their birth (i.e., it took until 2023 to collect data on children born in 2020). Therefore, the data set has no data yet on children born after 2020 because the data is still being collected for those birth years.

The sociodemographic data (i.e., race/ethnicity, poverty level, health insurance coverage, and urbanicity) are only available for the 4-year birth cohorts. There are only two 4-year birth cohorts in the dataset, with the most recent being children born in 2016-2019.

Finally, the data is collected by the CDC through a survey. A random sampling of parents is called, and parents choose whether to participate (which includes agreeing to allow the CDC to contact their child's pediatrician(s) to obtain vaccination history). The vaccination rates presented in the dataset are thus estimated percentages (which is how they are labeled in the dataset and in the app). The dataset does include a 95% confidence interval for each estimated percent. However, the 95% CI values were not presented in the app.