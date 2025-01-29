__author__ = "Dr. Jasdeep S. Anand, Dr. Rocio Barrio Guillo"
__credits__ = ["Dr. Jasdeep S. Anand", "Dr. Rocio Barrio Guillo", "Dr. Darren Ghent", ]
__other_citations__ = "Generated using European Union's Copernicus Land Monitoring Service information; https://doi.org/10.2909/299ad2d6-f2b8-4716-b169-1d621250fc3c, https://doi.org/10.2909/264d4e20-de6d-4f88-b1be-b592303452af, https://doi.org/10.2909/c7bf34ea-755c-4dbd-85b6-4efc5fd302a2"
__version__ = "1"
__description__ = "Downloads the data for the EFMI #8 Changes in Tree Cover Density."
__inputs__ = "Sentinel-2 Copernicus High-Resolution Layer Tree Cover Density dataset, at 100m resolution, annually for 2012, 2015 and 2018, with units %"
__outputs__ = "Files named TCD_{yyyy}_100m_eu_03035_d04_full.tif, at 100m resolution, annually for 2012, 2015 and 2018, with units %"

from pathlib import Path
from hda import Client, Configuration
import glob
import os
import requests
import zipfile
import rasterio
import geopandas as gpd
import numpy as np
from IPython import embed

from pyproj import Transformer
from rasterio.enums import Resampling
from rasterio.warp import calculate_default_transform, reproject, transform_bounds
from rasterio.mask import mask
from shapely.geometry import box
from rasterio.io import MemoryFile

def download_tcd_wekeo(tcd_dir, year):

    query_tcd = {
        'dataset_id': 'EO:CLMS:DAT:HRL',
        "product_type": f"Tree cover density {year}",
        "resolution": "100m",
        "itemsPerPage": 200,
        "startIndex": 0
        }

    matches_tcd = c.search(query_tcd)

    print('Downloading data')

    path_yr_dir = f"{tcd_dir}/TCD_{year}"
    os.makedirs(path_yr_dir, exist_ok=True)

    #print(matches_tcd.results)

    matches_tcd[-1].download(download_dir=path_yr_dir)

    print(f'Downloading complete for {year}!')

    zip_filename = matches_tcd.results[-1]['id']

    with zipfile.ZipFile(f"{path_yr_dir}/{zip_filename}.zip", 'r') as zip_ref:
        zip_ref.extractall(path_yr_dir)

    print(f'Unzipped file for {year}!')

# Local paths to directories where data is downloaded to
out_top_dir = '/data/atsr/OptForEU'
tcd_dir = f'{out_top_dir}/CLMS_TCD'
os.makedirs(tcd_dir, exist_ok=True)

# Download the data
# Default location expected by hda package
hdarc = Path(Path.home() / '.hdarc') # You must create this file with Wekeo username and password

# Create it only if it does not already exists
if not hdarc.is_file():
    import getpass
    USERNAME = input('Enter your username: ')
    PASSWORD = getpass.getpass('Enter your password: ')

    with open(Path.home() / '.hdarc', 'w') as f:
        f.write(f'user:{USERNAME}\n')
        f.write(f'password:{PASSWORD}\n')

hda_client = Client()

config = Configuration()

c = Client(config=config)

download_tcd_wekeo(tcd_dir, "2012")
download_tcd_wekeo(tcd_dir, "2015")
download_tcd_wekeo(tcd_dir, "2018")
