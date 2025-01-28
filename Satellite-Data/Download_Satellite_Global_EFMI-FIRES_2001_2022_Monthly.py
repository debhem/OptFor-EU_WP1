__author__ = "Dr. Jasdeep S. Anand, Dr. Rocio Barrio Guillo"
__other_citations__ = "Copernicus Climate Change Service, Climate Data Store, (2019): Fire burned area from 2001 to present derived from satellite observation. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). DOI: 10.24381/cds.f333cf85"
__version__ = "1"
__description__ = "Downloads data for EFMI #7 Forest area damaged by fire."
__inputs__ = "C3S Copernicus burnt area dataset from OLCI, at 300m resolution, monthly for 2017-2022, unitless [presence or absence of fire within cell]"
__outputs__ = "Files named c3s_pixel_burned_area_v1_1_{year}_monthly.zip"

import cdsapi
import os
import glob
import xarray as xr
import numpy as np
import re
from datetime import datetime
from geopy.distance import distance

# Local directory paths to save data in
out_top_dir = '/data/atsr/OptForEU'
ba_dir = f'{out_top_dir}/C3S_Burned_Area'
os.makedirs(ba_dir, exist_ok=True)

# years to loop over when downloading year by year
years = ['2017', '2018', '2019', '2020', '2021', '2022']
# Download the data
c = cdsapi.Client()

for year_d in years:

    dataset = "satellite-fire-burned-area"

    request = {
        "origin": "c3s",
        "sensor": "olci",
        "variable": "pixel_variables",
        "version": "1_1",
        "region": [
            "europe"
        ],
        "year": [
            f"{year_d}"
        ],
        "month": [
            "01", "02", "03",
            "04", "05", "06",
            "07", "08", "09",
            "10", "11", "12"
        ],
        "nominal_day": ["01"]
    }

    ba_filename = os.path.join(ba_dir, f'c3s_pixel_burned_area_v1_1_{year_d}_monthly.zip')

    c.retrieve(dataset, request, ba_filename)
