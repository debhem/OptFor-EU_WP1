__author__ = "Dr. Jasdeep S. Anand, Dr. Rocio Barrio Guillo"
__other_citations__ = "Copernicus Climate Change Service, Climate Data Store, (2019): Fire burned area from 2001 to present derived from satellite observation. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). DOI: 10.24381/cds.f333cf85"
__version__ = "1"
__description__ = "Downloads data for EFMI #11 Leaf Area Index."
__inputs__ = "Copernicus Global Land Service LAI dataset, at 300m resolution, 10-daily for 2014 to present, globally, unitless. Note that data was used From January 2014 to August 2016 based upon RT5 PROBA-V and to June 2020 based upon RT0 PROBA-V data with version 1.0 and from July 2020 onwards based upon RT0 Sentinel-3/OLCI data with version 1.1. RT0 is the Near Real Time product while RT5 is the final consolidated Real Time product."
__outputs__ = "Files named c_gls_LAI300-RT0_{yyyymmdd}0000_GLOBE_OLCI_V1.1.2.nc or c_gls_LAI300-RT0_{yyymmdd}0000_GLOBE_PROBAV_V1.0.1.nc or c_gls_LAI300_{yyyymmdd}0000_GLOBE_PROBAV_V1.0.1.nc"

from pathlib import Path
from hda import Client, Configuration
import glob
import os
import time
from datetime import datetime
from datetime import timedelta
import requests
import numpy as np
import pandas as pd
import xarray as xr

# Default location expected by hda package
hdarc = Path(Path.home() / '.hdarc')

# Create it only if it does not already exists
if not hdarc.is_file():
    import getpass
    USERNAME = input('Enter your username: ')
    PASSWORD = getpass.getpass('Enter your password: ')

    with open(Path.home() / '.hdarc', 'w') as f:
        f.write(f'user:{USERNAME}\n')
        f.write(f'password:{PASSWORD}\n')

hda_client = Client()

# Select product
var_product = 'LAI'

# Output directory for variable
d_dir = f'/data/atsr/OptForEU/CopernicusLand/{var_product}/'
if not os.path.exists(d_dir):
    os.makedirs(d_dir)

config = Configuration()

c = Client(config=config)

d_id = 'EO:CLMS:DAT:CLMS_GLOBAL_LAI_300M_V1_10DAILY_NETCDF'
var_nm = 'LAI'

query = {
    'dataset_id': d_id,
    'productGroupId': ['RT0'],
    'start': '2014-01-10T00:00:00.000Z',
    'end': '2023-12-31T23:59:59.999Z',
    }

# LAI RT0 from 20160910-20231231, RT5 product does not include the RT5
# productGroupId in the filename and covers 20140110-20160910.
query = {
    'dataset_id': d_id,
    'productType': 'LAI300',
    'start': '2014-01-10T00:00:00.000Z',
    'end': '2016-09-10T00:00:00.000Z',
    }

# Discover all files within region & time period
matches_gdmp = c.search(query)

matches_gdmp.download(download_dir=d_dir)

session = requests.Session()


for res in np.arange(0, len(matches_gdmp.results)):
    #matches_gdmp[res] # indicates volume but not sure how to extract it
    url = matches_gdmp.results[res]['properties']['location']
    file = session.get(url)
    prName = matches_gdmp.results[res]['id']
    thisfilepath = f'{d_dir}{prName}.nc'
    if file.status_code != 200:
        print('Request code is not correct, data will not download correctly: ')
        print(prName)
    else:
        with open(thisfilepath, 'wb') as p:
            for chunk in file.iter_content(chunk_size=8192):
                if chunk:
                    p.write(chunk)
        print('Downloaded: ', prName)
        print(str(res+1) + '/' + str(len(matches_gdmp.results)))


# Check missing dates
#ex_cp_filename = glob.glob(f'{d_dir}*RT5*.nc')
#ex_cp_filename = glob.glob(f'{d_dir}*LAI300_*.nc') # equivalent to RT5
ex_cp_filename = glob.glob(f'{d_dir}*RT0*.nc')

# Some files don't exist/are corrupt, so save them to a list to download again
# and remove corrupt files
corrupt_files = []
for fl in ex_cp_filename:
    try:
        ds_example = xr.open_dataset(f'{fl}')
    except OSError:
        corrupt_files.append(fl)
        pass

s_corrupt_files = sorted(corrupt_files)

if len(s_corrupt_files) != 0:
    print('Download these again:')
    for corrupt in s_corrupt_files:
        print(corrupt)
        try:
            os.remove(corrupt)
        except OSError:
            pass

# Fill time in with a random date if there is no time variable
def add_time_dim(xda):
    xda = xda.expand_dims(time = [datetime.now()])
    return xda

try:
    ds_example = xr.open_mfdataset(ex_cp_filename, engine='netcdf4', preprocess=add_time_dim)
except:
    ds_example = xr.open_mfdataset(ex_cp_filename, engine='netcdf4')

# Create a list of datetimes expected to have been downloaded for the time range
start_dates = pd.date_range(start='2014-01', end='2024-01', freq='MS') + timedelta(days=9)
mid_dates = pd.date_range(start='2014-01', end='2023-12', freq='MS') + timedelta(days=19)
end_dates = pd.date_range(start='2014-01', end='2024-01', freq='ME')

start_and_mid_dates = start_dates.append(mid_dates)
all_dates = start_and_mid_dates.append(end_dates)
all_dates_sorted = sorted(all_dates)
all_dates_sorted_dt = np.array(all_dates_sorted, dtype='datetime64')

# Compare to files downloaded
# Assign the actual date from the data file
dates = []
for dd in np.arange(0,len(ex_cp_filename)):
    # LAI RT0
    dates.append(ex_cp_filename[dd][56:64])

dates_df = pd.to_datetime(dates, format='%Y%m%d')
ds_example['time'] = dates_df

downloaded_dates = ds_example.time.values
mask_missing_dates = np.isin(all_dates_sorted_dt, downloaded_dates)

idx_missing_dates = np.where(mask_missing_dates==False)[0]
missing_dates = all_dates_sorted_dt[idx_missing_dates]
