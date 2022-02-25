# Imports
import pandas as pd
from datetime import date, timedelta
import folium
from folium import Marker
from folium.plugins import MarkerCluster
import math
import matplotlib.pyplot as plt
import seaborn as sns

# Population Data
populationData = pd.read_csv('2019_Census_US_Population_Data_By_State_Lat_Long.csv')

# Get the most recent date for filtering
freshDate = date.today() - timedelta(days=1)
freshDate = date.strftime(freshDate,"%Y%m%d")
freshDate = freshDate[0:4] + "-" + freshDate[4:6] + "-" + freshDate[6:8]

# Vaccination data, for most recent date
vaccinationData = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/us_state_vaccinations.csv')
vaccinationByLocation = vaccinationData.loc[(vaccinationData.date == freshDate)][["location", "people_vaccinated"]]

# Vaccination and population data
vaccinationAndPopulationByLocation = pd.merge(populationData, vaccinationByLocation, left_on='STATE',right_on='location').drop(columns="location")

# Calculate percentage vaccinated by state
vaccinationAndPopulationByLocation["percent_vaccinated"] = vaccinationAndPopulationByLocation["people_vaccinated"] / vaccinationAndPopulationByLocation["POPESTIMATE2019"]

print("Date ran:", date.today())

# Calculate the total percent vaccinated in the US
percentageTotal = vaccinationAndPopulationByLocation["people_vaccinated"].sum() / vaccinationAndPopulationByLocation["POPESTIMATE2019"].sum()
print('Percentage Vaccinated in the US: {}%'.format(round(percentageTotal*100, 2))) 

# Create the map
v_map = folium.Map(location=[42.32,-71.0589], tiles='cartodbpositron', zoom_start=4) 

# Add points to the map
mc = MarkerCluster()
for idx, row in vaccinationAndPopulationByLocation.iterrows(): 
    if not math.isnan(row['long']) and not math.isnan(row['lat']):
        mc.add_child(Marker(location=[row['lat'], row['long']],
                            tooltip=str(round(row['percent_vaccinated']*100, 2))+"%"))
v_map.add_child(mc)

# Display the map
v_map.save("vaccie_tracker_map.html")
