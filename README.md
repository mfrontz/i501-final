# Protecting Children's Health

[child-vaccinations.streamlit.app](https://child-vaccinations.streamlit.app/)

## Overview

This web app allows users to conduct their own exploratory data analysis of a CDC dataset on vaccination rates of young children in the United States.

The app provides interactive data visualizations that users can customize by changing data filters for vaccine, dose, age checkpoint, geographic location (such as United States, specific state, etc.), and sociodemographic factor (such as race/ethnicity, poverty level, etc.).

The app also provides an overview of the recommended vaccinations for young children and a link to a CDC website for parents, which provides resources on child vaccinations.

The goal of the app is to allow users to explore differences in vaccination rates, which may lead them to want to find answers to questions such as:

- What barriers prevent children from receiving their recommended vaccinations?
- What happens if children don't receive their recommended vaccinations?
- How can we ensure more children receive their recommended vaccinations?
- Where can I learn more about how to best protect my child's health?

## Data Description

The original dataset used in this web app was downloaded from the [CDC Data Catalog](https://data.cdc.gov/Child-Vaccinations/Vaccination-Coverage-among-Young-Children-0-35-Mon/fhky-rtsk/about_data). 

The following steps were performed in Python to clean and prepare the data for use in the web app:

- Pivoted a column named "Dimension Type" (and its corresponding column of values named "Dimension") into multiple columns, as the CDC used this column to store data for multiple sociodemographic variables
- Split a column named "Birth Year/Birth Cohort" into two distinct columns because some of the other columns in the dataset are only applicable to birth years, while other columns are only applicable to birth cohorts
- Dropped rows that were missing data for the column named "Estimated (%)" which is the core data used in all the data visualizations (this only dropped 58 rows out of 118423 total rows)
- Filled blank values for doses of certain vaccines based on CDC documentation that explained what those blank values actually represent (e.g., the "Combined 7 Series" vaccine did not list a dose value, but the rows for this vaccine represent children who have received the "Full Series" of this vaccine, etc.)
- Renamed certain columns to make them more clear (e.g., renamed "Geography" column to "Geographic Area", renamed "Insurance Coverage" column to "Health Insurance Coverage", etc.)
- Added a new column for state abbreviation by translating any state names in the "Geographic Area" column into their corresponding two-letter abbreviation. This was needed for the choropleth map of the United States, which requires two-letter state abbreviations in order to plot data values on the map.

[Code used to clean and prepare data](https://github.com/mfrontz/i501-labs/blob/main/vacc_data/data_cleaned.ipynb)

## Algorithm Description

The app presents 3 pre-designed data visualizations (choropleth map, line graph, and bar chart) which the user can customize using a set of data filters (e.g., by selecting a vaccine, dose, age checkpoint, etc.).

The visualizations were designed to:

- maximize the use of the available variables in the dataset
- match the data to an appropriate visualization type that would be easy to interpret
- present different aspects of the available dataset in each visualization type

The variables used in the data visualizations are set by the filter selections, so when the user changes a filter selection, the visualizations automatically update in real-time.

In addition, there are dependencies among certain data filters. As one example, the choice of vaccine determines what choices are available for vaccine dose. So the filters that have dependencies include function calls that dynamically update the available choices for the "child" filter whenever its "parent" filter is changed.

## Tools Used

- The web app is built in Python using the [Streamlit library](https://docs.streamlit.io/get-started)
- Pandas and Numpy functions are used for data manipulation in the app
- Plotly Express is used to produce the data visualizations in the app
- Streamlit Community Cloud is used to host the app
- Backblaze is used to store the dataset used in the app

## Ethical Concerns

Overall, the data presented in the app is as accurate as possible, but it may not represent the current actual vaccination status of children across the United States.

The web app uses the most recent CDC data available at the time of this project (spring 2024).

The data available within the original dataset is limited by how it is collected. For example, the most recent birth year available in the dataset is 2020 as the CDC collects data on children up to 3 years after their birth (i.e., it took until 2023 to collect data on children born in 2020). Therefore, the data set has no data yet on children born after 2020 because the data is still being collected for those birth years.

The sociodemographic data (i.e., race/ethnicity, poverty level, health insurance coverage, and urbanicity) are only available for the 4-year birth cohorts. There are only two 4-year birth cohorts in the dataset, with the most recent being children born in 2016-2019.

Finally, the data is collected by the CDC through the [National Immunization Survey-Child](https://www.cdc.gov/vaccines/imz-managers/nis/about.html#nis-child). A random sampling of parents is telephoned, and parents choose whether to participate (which includes agreeing to allow the CDC to contact their child's healthcare provider(s) to obtain vaccination history). Obviously, certain parents may be more willing (or less willing) to participate and share this information, which may affect the results.

Thus, the vaccination rates presented in the dataset are **estimated** percentages (which is how they are labeled in the dataset and in the app). The dataset does include a 95% confidence interval for each estimated percent; however, it was decided to not present the 95% CI values in the visualizations.

---

Copyright © 2024 Michael Frontz

This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).  

You are free to use, share, or adapt this material for non-commercial purposes as long as you provide proper attribution and distribute any copies or adaptations under this same license.