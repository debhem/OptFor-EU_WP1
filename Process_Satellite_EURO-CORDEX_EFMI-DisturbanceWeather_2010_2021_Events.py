__author__ = "Dr. Jasdeep S. Anand, Dr. Rocio Barrio Guillo"
__credits__ = ["Dr. Jasdeep S. Anand", "Dr. Rocio Barrio Guillo", "Dr. Darren Ghent", ]
__other_citations__ = "Forzieri, Giovanni; Pecchi, Matteo; Girardello, Marco; Mauri, Achille; Klaus, Marcus; Nikolov, Christo; et al. (2019). A spatially-explicit database of wind disturbances in European forests over the period 2000-2018. figshare. Dataset. https://doi.org/10.6084/m9.figshare.9555008.v2"
__version__ = "1"
__description__ = "Produces EFMI #6.1 Forest area with damage caused by severe weather events. Subsets to the EURO CORDEX region domain"
__inputs__ = "FORWIND database, at day/event of disturbance resolution, for 2000-07-25 to 2018-10-28, with units ha. Data was downloaded manually from https://figshare.com/articles/dataset/A_spatially-explicit_database_of_wind_disturbances_in_European_forests_over_the_period_2000-2018/9555008"
__outputs__ = "File named rs_veg_europe_disturbanceWeather_none_event_2000_2018_v1_forwind.shp, area shapefile, daily/event for 2000-07-25 to 2018-10-28, with units ha"


import xarray as xr
import numpy as np
import pandas as pd
import geopandas as gpd
from matplotlib import pyplot as plt
import cartopy.crs as ccrs
from shapely.geometry import mapping
from shapely.geometry import box
import os
from datetime import datetime

# Paths to local directories where data has been downloaded to
out_top_dir = '/data/atsr/OptForEU'
wea_dir = f'{out_top_dir}/FORWIND'
os.makedirs(wea_dir, exist_ok=True)
# Path to local directory for output
out_wea_dir = f'{wea_dir}/Europe/input/remote_sensing/vegetation/'
if not os.path.exists(out_wea_dir):
    os.makedirs(out_wea_dir)

# EURO-CORDEX Domain
eur_min_lon = -44.75
eur_max_lon = 65.25
eur_min_lat = 21.75
eur_max_lat = 72.75

# FORWIND wind/storm disturbance downloaded dataset filename
wea_loc = f'{wea_dir}/FORWIND_v2.shp'

# First, read in FORWIND data into geopandas
wea_data = gpd.read_file(wea_loc)

# Next, create bounding box
gdf = box(eur_min_lon, eur_min_lat, eur_max_lon, eur_max_lat)

# Convert this into a geodataframe
gdf = gpd.GeoDataFrame([1], geometry=[gdf], crs=wea_data.crs)

wind_gdf = gdf.overlay(wea_data, how = 'intersection')

# First, convert the EventDate into datetime (some entries have the event date as: %Y/%m/%d, while
# some have them as: %Y-%m-%d. Have to account for both!
wind_gdf['EventDate_dt'] = pd.Series(dtype = 'datetime64[ns]')
wind_gdf.loc[wind_gdf['EventDate'].str.contains('/'), 'EventDate_dt'] = pd.to_datetime(wind_gdf.loc[wind_gdf['EventDate'].str.contains('/'), 'EventDate'])
wind_gdf.loc[wind_gdf['EventDate'].str.contains('-'), 'EventDate_dt'] = pd.to_datetime(wind_gdf.loc[wind_gdf['EventDate'].str.contains('-'), 'EventDate'])

# Calculate total area covered by all instances in ha
# Reproject to equal area projection
wind_gdf_eqcrs = wind_gdf.to_crs(epsg = 6933)
# Convert area to ha for every polygon
wind_gdf_eqcrs['area_m2'] = wind_gdf_eqcrs['geometry'].area
wind_gdf_eqcrs['area_ha'] = wind_gdf_eqcrs['area_m2'] / 10000

wind_final_gdf = wind_gdf_eqcrs[['EventDate_dt', 'geometry', 'area_ha']]
# Change back to WGS84 for DSS
if wind_final_gdf.crs != "EPSG:4326":
    wind_final_gdf = wind_final_gdf.to_crs("EPSG:4326")

# Save to shapefile
wind_eur_flname_output = 'rs_veg_europe_disturbanceWeather_none_event_2000_2018_v1_forwind.shp'
wind_final_gdf.to_file(f'{out_wea_dir}{wind_eur_flname_output}', driver='ESRI Shapefile')

# Save metadata to a sidecar file
metadata = {
    "Filename": wind_eur_flname_output,
    "Variables": "area_ha",
    "Units": "Ha",
    "Data source": "FORWIND database",
    "Time period": "2000-07-25 to 2018-10-28",
    "Spatial extent": "Europe",
    "Coordinate system": "EPSG:6933",
    "Author names": "Dr. Rocio Barrio Guillo, Dr. Jasdeep S. Anand"
}

# Write metadata to a text file
with open(f'{out_wea_dir}metadata_rs_veg_europe_disturbanceWeather_none_event_2000_2018_v1_forwind.txt', 'w') as f:
    for key, value in metadata.items():
        f.write(f"{key}: {value}\n")
