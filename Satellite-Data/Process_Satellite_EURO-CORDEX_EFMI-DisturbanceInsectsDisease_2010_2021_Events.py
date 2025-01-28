__author__ = "Dr. Jasdeep S. Anand, Dr. Rocio Barrio Guillo"
__other_citations__ = "Forzieri G et al. (2023). The Database of European Forest Insect and Disease Disturbances: DEFID2. Global Change Biology"
__version__ = "1"
__description__ = "Produces EFMI #5.1 Forest area with damage caused by insects and diseases. Subsets to the EURO CORDEX region domain"
__inputs__ = "DEFID2 database, at day/event of disturbance resolution, for 1963-08-01 to 2021-09-30, with units ha. Data was downloaded from Data was downloaded manually from https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/FOREST/DISTURBANCES/DEFID2/VER1-0/"
__outputs__ = "File named rs_veg_europe_disturbanceInsectsDisease_none_event_1963_2021_v1_defid2.shp, area shapefile, daily/event for 1963-08-01 to 2021-09-30, with units ha; and a file named metadata_rs_veg_europe_disturbanceInsectsDisease_none_event_1963_2021_v1_defid2.txt with the metadata for the shapefile."

import xarray as xr
import numpy as np
import pandas as pd
import geopandas as gpd
from matplotlib import pyplot as plt
import cartopy.crs as ccrs
from shapely.geometry import mapping
from shapely.geometry import box
from IPython import embed
import os
from datetime import datetime

# Local paths to directories where data has been downloaded to
out_top_dir = '/data/atsr/OptForEU'
ins_dir = f'{out_top_dir}/DEFID2'
os.makedirs(ins_dir, exist_ok=True)
# Local path to directory for outputs to be saved to
out_ins_dir = f'{ins_dir}/Europe/input/remote_sensing/vegetation/'
if not os.path.exists(out_ins_dir):
    os.makedirs(out_ins_dir)

# EURO-CORDEX Domain
eur_min_lon = -44.75
eur_max_lon = 65.25
eur_min_lat = 21.75
eur_max_lat = 72.75

# DEFID2 insect/disease disturbance downloaded dataset filename
ins_loc = f'{ins_dir}/defid2.gpkg'

# First, read in DEFID2 data into geopandas
ins_data = gpd.read_file(ins_loc)

# Next, create bounding box
gdf = box(eur_min_lon, eur_min_lat, eur_max_lon, eur_max_lat)

# Convert this into a geodataframe
gdf = gpd.GeoDataFrame([1], geometry = [gdf], crs = ins_data.crs)

# Clip DEFID2 to bounding box - although the extent is smaller than the EURO-CORDEX so remains the same
ins_gdf = ins_data.clip(gdf)
# Convert date to datetime
ins_gdf['survey_date'] = pd.to_datetime(ins_gdf['survey_date'])

# Calculate total area covered by all instances in ha
# Reproject to equal area projection
ins_gdf_eqcrs = ins_gdf.to_crs("EPSG:6933")
# Area in m2 passed to ha
# Are these units correct?
ins_gdf_eqcrs['area_ha'] = ins_gdf_eqcrs.geometry.area / 10000
# Final output with geometry in EPSG 6933, date of event and affected area in ha
ins_final_gdf = ins_gdf_eqcrs[['survey_date', 'geometry', 'area_ha']]
# Change back to WGS84 for DSS
if ins_final_gdf.crs != "EPSG:4326":
    ins_final_gdf = ins_final_gdf.to_crs("EPSG:4326")

# Filename to save output as
ins_eur_flname_output = 'rs_veg_europe_disturbanceInsectsDisease_none_event_1963_2021_v1_defid2.shp'
# Some geometries were corrupt but if we fix them we lose data
# if ins_final_gdf.is_valid.all() == False:
#     ins_final_gdf["geometry"] = ins_final_gdf["geometry"].apply(lambda geom: geom.buffer(0) if not geom.is_valid else geom)
# Save as a shapefile
ins_final_gdf.to_file(f'{out_ins_dir}{ins_eur_flname_output}', driver='ESRI Shapefile')

# Save metadata to a sidecar file
metadata = {
    "Filename": ins_eur_flname_output,
    "Variables": "area_ha",
    "Units": "Ha",
    "Data source": "DEFID2 database",
    "Time period": "1963-08-01 to 2021-09-30",
    "Spatial extent": "Europe",
    "Coordinate system": "EPSG:4326",
    "Author names": "Dr. Rocio Barrio Guillo, Dr. Jasdeep S. Anand"
}

# Write metadata to a text file
with open(f'{out_ins_dir}metadata_rs_veg_europe_disturbanceInsectsDisease_none_event_1963_2021_v1_defid2.txt', 'w') as f:
    for key, value in metadata.items():
        f.write(f"{key}: {value}\n")
