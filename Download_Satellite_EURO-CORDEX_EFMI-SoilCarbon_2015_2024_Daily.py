__author__ = "Dr. Rocio Barrio Guillo, Dr. Jasdeep S. Anand"
__other_citations__ = "Kimball, J. S., Endsley, A., Jones, L. A., Kundig, T. & Reichle, R. (2022). SMAP L4 Global Daily 9 km EASE-Grid Carbon Net Ecosystem Exchange"
                      "(SPL4CMDL, Version 7). [Data Set]. Boulder, Colorado USA. NASA National Snow and Ice Data Center Distributed Active Archive Center. https://doi.org/10.5067/3K9F0S1Q5J2U"
__version__ = "1"
__description__ = "Downloads the data for the EFMI #4.3 Carbon stored in forest soils"
__inputs__ = "NASA SMAP L4 Global Daily 9 km EASE-Grid Carbon Net Ecosystem Exchange, Version 7, at 9km resolution, daily for 2015-2024, with units gC/m2"
__outputs__ = "Files named SMAP_L4_C_mdl_{yyymmdd}T000000_Vv7041_001.h5, at 9km resolution, daily for 2015-2024, with units gC/m2"

import earthaccess
import os
import xarray as xr
import numpy as np
from datetime import datetime
import h5py
import re

# Paths to local directories to save the data in
out_top_dir = '/data/atsr/OptForEU'
soc_dir = f'{out_top_dir}/SMAP_Soil_Carbon'
soc_dir_input = f'{soc_dir}/input_data'
os.makedirs(soc_dir, exist_ok=True)
os.makedirs(soc_dir_input, exist_ok=True)

# EURO-CORDEX Domain
eur_min_lon = -44.75
eur_max_lon = 65.25
eur_min_lat = 21.75
eur_max_lat = 72.75

# Data download
earthaccess.login() # will ask for a username and password

results = earthaccess.search_data(
    short_name="SPL4CMDL",
    version = "007",
    cloud_hosted=False,
    bounding_box=(eur_min_lon, eur_min_lat, eur_max_lon, eur_max_lat), # (lower_left_lon, lower_left_lat, upper_right_lon, upper_right_lat)
    temporal=("2015-04", "2023-12")
)

files = earthaccess.download(results, soc_dir_input)
