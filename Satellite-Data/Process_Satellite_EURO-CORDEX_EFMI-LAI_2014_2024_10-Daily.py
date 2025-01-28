__author__ = "Dr. Jasdeep S. Anand, Dr. Rocio Barrio Guillo"
__credits__ = ["Dr. Jasdeep S. Anand", "Dr. Rocio Barrio Guillo", "Dr. Darren Ghent", ]
__other_citations__ = "European Commission Directorate-General Joint Research Centre. Leaf Area Index 2014-present (raster 300 m), global, 10-daily - version 1."
__version__ = "1"
__description__ = "Produces EFMI #11 Leaf Area Index. Resamples spatial resolution, resampled temporal resolution and subsets to the EURO CORDEX region domain"
__inputs__ = "Copernicus Global Land Service LAI dataset, at 300m resolution, 10-daily for 2014 to present, unitless. Note that data was used From January 2014 to August 2016 based upon RT5 PROBA-V and to June 2020 based upon RT0 PROBA-V data with version 1.0 and from July 2020 onwards based upon RT0 Sentinel-3/OLCI data with version 1.1. RT0 is the Near Real Time product while RT5 is the final consolidated Real Time product."
__outputs__ = "File named rs_veg_europe_lai_none_mon_2014_2024_v1_clms.nc, at 1km resolution, monthly from January 2014 to December 2023, unitless"

from matplotlib import pyplot as plt
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import datetime
import pandas as pd
import cordex as cx
import os
import xesmf as xe
import cartopy.crs as ccrs
import datetime
from IPython import embed
from netCDF4 import Dataset

# Local path to directory where downloaded data has been saved
var_dir = '/data/atsr/OptForEU/CopernicusLand/LAI/'
# Local path to directory where output will be saved
out_dir_top = '/data/atsr/OptForEU/CLMS_LAI'
out_dir = f'{out_dir_top}/Europe/input/remote_sensing/vegetation/'
if not os.path.exists(out_dir):
     os.makedirs(out_dir)

# EURO-CORDEX Domain
min_lon_eur = -44.75
max_lon_eur = 65.25
min_lat_eur = 21.75
max_lat_eur = 72.75

# Define time for the whole timeframe
time_start = pd.Timestamp('2014-01-01')
time_end = pd.Timestamp('2023-12-31')
var_times = pd.date_range(start = time_start, end = time_end, freq = 'MS')

# We use different products to cover the longest timeframe, the times for each are defined here
rt5_time_start = pd.Timestamp('2014-01-01')
rt5_time_end = pd.Timestamp('2016-08-01')
rt5_var_times = pd.date_range(start = rt5_time_start, end = rt5_time_end, freq = 'MS')
rt0_probav_time_start = pd.Timestamp('2016-09-01')
rt0_probav_time_end = pd.Timestamp('2020-10-01')
rt0_probav_var_times = pd.date_range(start = rt0_probav_time_start, end = rt0_probav_time_end, freq = 'MS')
rt0_olci_time_start = pd.Timestamp('2020-11-01')
rt0_olci_time_end = pd.Timestamp('2023-12-31')
rt0_olci_var_times = pd.date_range(start = rt0_olci_time_start, end = rt0_olci_time_end, freq = 'MS')

# Define lists to append to in the loop for each month
monthly_averages = []
yr_mn_list = []
# Loop through each month of data, resampling and cropping
for i in range(var_times.size):

    mn = var_times[i]

    if mn in rt5_var_times:
        var_files = sorted(glob('%s/c_gls_LAI300_%i%02d*.nc' % (var_dir, mn.year, mn.month)))
    elif mn in rt0_probav_var_times:
        var_files = sorted(glob('%s/c_gls_LAI300-RT0_%i%02d*_PROBAV_*.nc' % (var_dir, mn.year, mn.month)))
    elif mn in rt0_olci_var_times:
        var_files = sorted(glob('%s/c_gls_LAI300-RT0_%i%02d*_OLCI_*.nc' % (var_dir, mn.year, mn.month)))
    else:
        print('Month not within range of the timestamp for RT0 and RT5 programmed')

    # Open datasets
    var_data = xr.open_mfdataset(var_files, combine = 'nested', concat_dim = [pd.Index(np.arange(len(var_files)), name = 'time'),])

    # Resample temporal resolution
    da_month_mean_lai = var_data.mean(dim='time')

    var_lon = var_data.lon.values
    var_lat = var_data.lat.values
    # Select lats and lons within European domain
    var_lon_in_range = np.where((var_lon <= max_lon_eur) & (var_lon >= min_lon_eur))[0]
    var_lat_in_range = np.where((var_lat <= max_lat_eur) & (var_lat >= min_lat_eur))[0]
    var_data_subset = da_month_mean_lai.isel(lon=slice(int(var_lon_in_range[0]), int(var_lon_in_range[-1])+1), lat=slice(int(var_lat_in_range[0]), int(var_lat_in_range[-1])+1)) # , time = 0)
    # Resample spatial resolution from 333m to 1km
    coarsening_factor = 1000 // 333
    var_data_coarsen = var_data_subset['LAI'].coarsen(lon=coarsening_factor, lat=coarsening_factor, boundary = "pad").mean()

    month = mn.strftime("%m")
    time_mn_yr = f'{mn.year}-{month}'

    monthly_averages.append(var_data_coarsen)
    yr_mn_list.append(time_mn_yr)

# Join all months in a dataset
combined_dataset = xr.concat(monthly_averages, dim='time')
combined_dataset = combined_dataset.assign_coords(time=yr_mn_list)

# Filename for output netcdf
lai_out_filename = 'new_rs_veg_europe_lai_none_mon_2014_2024_v1_clms.nc'

# Metadata
combined_dataset.attrs['Filename'] = lai_out_filename
combined_dataset.attrs['Variables'] = 'LAI'
combined_dataset.attrs['Units'] = 'none'
combined_dataset.attrs['Data_source'] = 'Copernicus Global Land Service Leaf Area Index dataset'
combined_dataset.attrs['Time_period'] = 'January 2014-December2023'
combined_dataset.attrs['Time_averaging'] = 'Monthly'
combined_dataset.attrs['Spatial_extent'] = 'Europe'
combined_dataset.attrs['Coordinate_system'] = 'EPSG:4326'
combined_dataset.attrs['Author_names'] = 'Dr. Rocio Barrio Guillo, Dr. Jasdeep S. Anand'

combined_dataset.to_netcdf(f'{out_dir}{lai_out_filename}')
