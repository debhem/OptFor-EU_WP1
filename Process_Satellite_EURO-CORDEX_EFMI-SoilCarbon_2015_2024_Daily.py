__author__ = "Dr. Rocio Barrio Guillo, Dr. Jasdeep S. Anand"
__other_citations__ = "Kimball, J. S., Endsley, A., Jones, L. A., Kundig, T. & Reichle, R. (2022). SMAP L4 Global Daily 9 km EASE-Grid Carbon Net Ecosystem Exchange. (SPL4CMDL, Version 7). [Data Set]. Boulder, Colorado USA. NASA National Snow and Ice Data Center Distributed Active Archive Center. https://doi.org/10.5067/3K9F0S1Q5J2U."
__version__ = "1"
__description__ = "Produces EFMI #4.3 Carbon stored in forest soils. Resamples temporal resolution"
__inputs__ = "NASA SMAP L4 Global Daily 9 km EASE-Grid Carbon Net Ecosystem Exchange, Version 7, at 9km resolution, daily for 2015-2024, with units g C/m2"
__outputs__ = "File named rs_veg_europe_soilCarbon_none_mon_2015_2024_v1_smap.nc, at 9km resolution, monthly for 2015-2024, with units tonnes C/ha"

import os
import xarray as xr
import numpy as np
from datetime import datetime
import h5py
import re

# Local paths to directories where data has been downloaded to
out_top_dir = '/data/atsr/OptForEU'
soc_dir = f'{out_top_dir}/SMAP_Soil_Carbon'
soc_dir_input = f'{soc_dir}/input_data'
os.makedirs(soc_dir, exist_ok=True)
os.makedirs(soc_dir_input, exist_ok=True)
# Local path to directory for outputs
out_soc_dir = f'{soc_dir}/Europe/input/remote_sensing/vegetation/'
os.makedirs(out_soc_dir, exist_ok=True)

# EURO-CORDEX Domain
eur_min_lon = -44.75
eur_max_lon = 65.25
eur_min_lat = 21.75
eur_max_lat = 72.75

# Define lists to populate in the loop with the filenames and dates of the data
soc_data_list = []
dates_list = []
# List names of files in downloaded data directory
filenames = os.listdir(soc_dir)
# Define a regex pattern to capture the date in filenames
date_pattern = re.compile(r'_([0-9]{8}T[0-9]{6})_')
# Filter and sort filenames by date
sorted_filenames = sorted(
    [fname for fname in filenames if date_pattern.search(fname)],
    key=lambda x: datetime.strptime(date_pattern.search(x).group(1), "%Y%m%dT%H%M%S")
)
# Get rid of 31/03/2015
sorted_filenames = sorted_filenames[1:]
# Open data and read in relevant variables like soil carbon and lat, lon
for filename in sorted_filenames:
    if filename.endswith('.h5'):
        date_str = filename.split('_')[4]
        date_str = date_str[:8]
        date = datetime.strptime(date_str, '%Y%m%d')
        print(f"Processing file: {filename}, Date: {date}")
        print('------------------------------------------')

        with h5py.File(os.path.join(soc_dir, filename), "r") as h5_file:
            # Extract SOC data and coordinates
            soc_group = h5_file['SOC']
            geo_group = h5_file['GEO']

            soc_mean_data = soc_group['soc_mean'][:]  # (y, x) SOC data in g C m-2
            lat_data = geo_group['latitude'][:]  # (y, x) latitude data
            lon_data = geo_group['longitude'][:]  # (y, x) longitude data

            # Append the SOC data and the corresponding date to the lists
            soc_data_list.append(soc_mean_data)
            dates_list.append(date)

# Convert lists into a 3D numpy array (time, y, x)
soc_data_array = np.stack(soc_data_list)  # Shape will be (time, y, x)
# Convert list of dates into a time dimension for xarray
time_coord = np.array(dates_list)
# Create the xarray DataArray
xr_soc_data = xr.DataArray(
    soc_data_array,
    dims=["time", "y", "x"],
    coords={
        "time": time_coord,
        "lat": (["y", "x"], lat_data),
        "lon": (["y", "x"], lon_data)
    }
)

# Save intermediate file for daily soil carbon - optional
#soc_flname_output = 'rs_veg_europe_soc_day_2016_to_2023_v7_smap.nc'
#xr_soc_data.to_netcdf(f'{out_soc_dir}/{soc_flname_output}')
#
# soc_flname_output = 'rs_veg_europe_soc_day_2016_to_2023_v7_smap.nc'
# xr_soc_data = xr.open_dataset(f'{out_soc_dir}/{soc_flname_output}', engine='netcdf4')

xr_soc_data = xr_soc_data.rename_vars({'__xarray_dataarray_variable__': 'SOC'}) # SOC data in g C m-2

# First, ensure the 'time' dimension is in a proper datetime format (if it's not already)
# xr_soc_data['time'] = xr.cftime_range(start=xr_soc_data['time'].values[0],
#                                        periods=len(xr_soc_data['time']), freq='D')

# Mask -9999 values before monthly averages
xr_soc_data_masked = xr_soc_data.where(xr_soc_data != -9999, np.nan)

# Resample by month and calculate the mean
monthly_avg = xr_soc_data_masked.resample(time='1MS').mean(dim='time')  # '1MS' means first of the month

# Clip to European extent
lat_2d = monthly_avg['lat']
lon_2d = monthly_avg['lon']

mask_eur = (
            (lat_2d >= eur_min_lat) & (lat_2d <= eur_max_lat) &
            (lon_2d >= eur_min_lon) & (lon_2d <= eur_max_lon)
            )

eur_soc_data = monthly_avg.where(mask_eur, drop=True)

# 9km to 10km
#new_lat = np.linspace(lat_2d.min(), lat_2d.max(), int(lat_2d.shape[0] * 9/10))
#new_lon = np.linspace(lon_2d.min(), lon_2d.max(), int(lon_2d.shape[1] * 9/10))
# TODO: 9 to 10km resolution change not working - SIMAVI can do this?
#xr_soc_data_10km = eur_soc_data.interp(y=new_lat, x=new_lon)

# Convert the units from g C m-2 to tons C m-2
eur_soc_data['SOC'] = eur_soc_data['SOC'] / 1e6 # tons C m-2

# Caculate the area of the grid cells
R = 6371000  # Earth's radius in meters
lat = eur_soc_data['lat']
lon = eur_soc_data['lon']
lat_radians = np.radians(lat)
lon_radians = np.radians(lon)
# Calculate the differences between adjacent grid points in radians
# Assuming uniform spacing, use the spacing between the first two points
dlat = np.abs(lat_radians[1, 0] - lat_radians[0, 0])  # latitude increment in radians
dlon = np.abs(lon_radians[0, 1] - lon_radians[0, 0])  # longitude increment in radians
# Calculate the area for each cell
# Area of a spherical quadrilateral: A = R^2 * dlat * dlon * cos(lat)
# This accounts for the cell's position on the globe by using cos(lat)
cell_area = (R**2) * dlat * dlon * np.cos(lat_radians)
# Now 'cell_area' is a 2D array with the area of each grid cell in square meters
eur_soc_data['cell_area_m2'] = xr.DataArray(cell_area, dims=('y', 'x'))

# Remove metadata from original data
eur_soc_data.attrs.clear()

# Filename to save outputs as
soc_flname_output = 'rs_veg_europe_soilCarbon_none_mon_2015_2024_v1_smap.nc'

# Metadata
eur_soc_data.attrs['Filename'] = soc_flname_output
eur_soc_data.attrs['Variables'] = 'SOC, cell_area_m2'
eur_soc_data.attrs['Units'] = 'tons C m-2, m2'
eur_soc_data.attrs['Data_source'] = 'SMAP L4 Global Daily 9 km EASE-Grid Carbon Net Ecosystem Exchange, Version 7 product'
eur_soc_data.attrs['Time_period'] = 'April 2015 to December 2023'
eur_soc_data.attrs['Time_averaging'] = 'Monthly'
eur_soc_data.attrs['Spatial_extent'] = 'Europe'
eur_soc_data.attrs['Coordinate_system'] = 'EPSG:4326'
eur_soc_data.attrs['Author_names'] = 'Dr. Rocio Barrio Guillo, Dr. Jasdeep S. Anand'
# Save to netcdf
eur_soc_data.to_netcdf(f'{out_soc_dir}/{soc_flname_output}')
