__author__ = "Dr. Jasdeep S. Anand, Dr. Rocio Barrio Guillo"
__other_citations__ = "Copernicus Climate Change Service, Climate Data Store, (2019): Fire burned area from 2001 to present derived from satellite observation. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). DOI: 10.24381/cds.f333cf85"
__version__ = "1"
__description__ = "Produces EFMI #7 Forest area damaged by fire. Selects the 'forest' land cover classes, resamples the spatial resolution and subsets to the EURO CORDEX region domain"
__inputs__ = "C3S Copernicus burnt area dataset from OLCI, at 300m resolution, monthly for 2017-2022, unitless [presence or absence of fire within cell]"
__outputs__ = "File named rs_veg_europe_fires_none_mon_2010_2021_v1_esacci.nc, at 1km resolution, monthly for 2017-2022, with variables: 'fires' (unitless, presence/absence fire in the cell for all land cover classes), 'forest_fires' (unitless, presence/absence fire in the cell for forest land cover classes), 'cell_area_ha' (Ha, the area of each cell)"

import os
import glob
import xarray as xr
import numpy as np
import re
from datetime import datetime
from geopy.distance import distance

# Local directory paths to open downloaded data
out_top_dir = '/data/atsr/OptForEU'
ba_dir = f'{out_top_dir}/C3S_Burned_Area'
os.makedirs(ba_dir, exist_ok=True)
# Local directory path to save outputs in
out_ba_dir = f'{ba_dir}/Europe/input/remote_sensing/vegetation/'
if not os.path.exists(out_ba_dir):
    os.makedirs(out_ba_dir)

# EURO-CORDEX Domain
eur_min_lon = -44.75
eur_max_lon = 65.25
eur_min_lat = 21.75
eur_max_lat = 72.75

# Search for all downloaded files
ba_filename_yr = glob.glob(f'{ba_dir}/*/*.nc')
# Open all files in an xarray
ba_data = xr.open_mfdataset(ba_filename_yr, engine="netcdf4")
# Convert time to datetime
dates = ba_data.time.values
year_month = dates.astype('datetime64[M]').astype(str)
# Select the data within the EURO-CORDEX domain
ba_lat, ba_lon = ba_data.lat.values, ba_data.lon.values
ba_lon_ind_range = np.where((ba_lon >= eur_min_lon) & (ba_lon <= eur_max_lon))[0]
ba_lat_ind_range = np.where((ba_lat >= eur_min_lat) & (ba_lat <= eur_max_lat))[0]
# Crop the data to the domain
ba_data_eur = ba_data.isel(
                            lat = ba_lat_ind_range,
                            lon = ba_lon_ind_range
                            )
# Save the classification data in two separate variables to get all files and forest fires separately
ba_data_eur_fire = ba_data_eur.LC
ba_data_eur_forest_fire = ba_data_eur.LC

ba_data.close()

# Calculate a 2D mask where ANY fires have occurred in the region
ba_data_eur_fire = ba_data_eur_fire.where(ba_data_eur_fire != 0
                                         ).notnull()
# And calculate a 2D mask where FOREST fires have occurred in the region
ba_data_eur_forest_fire = ba_data_eur_forest_fire.where(
                                    (
                                    (ba_data_eur_forest_fire >= 50)
                                    & (ba_data_eur_forest_fire <= 90))
                                    | (ba_data_eur_forest_fire == 160)
                                    | (ba_data_eur_forest_fire == 170)
                                    ).notnull()

# Resample the spatial resolution from 300m to 1km
ba_data_eur_fire_1km = ba_data_eur_fire.coarsen(lat=3, lon=3, boundary="trim").any()
ba_data_eur_forest_fire_1km = ba_data_eur_forest_fire.coarsen(lat=3, lon=3, boundary="trim").any()

ds_ba_data_eur_fire_1km = ba_data_eur_fire_1km.to_dataset(name="fires")
ds_ba_data_eur_fire_1km['forest_fires'] = ba_data_eur_forest_fire_1km

# Caculate area of grid cells
R = 6371.0 # Earth's radius in kilometers
# Get lat and lon
lat_1km_grid = ds_ba_data_eur_fire_1km['lat']
lon_1km_grid = ds_ba_data_eur_fire_1km['lon']
# Get lat and lon resolution
lat_res = np.abs(lat_1km_grid[1] - lat_1km_grid[0])  # Latitude resolution in degrees
lon_res = np.abs(lon_1km_grid[1] - lon_1km_grid[0])  # Longitude resolution in degrees
# Convert from degrees to radians
lat_res_rad = np.deg2rad(lat_res)
lon_res_rad = np.deg2rad(lon_res)
# Calculate cell area
cell_area = (R**2 * lat_res_rad * lon_res_rad * np.cos(np.deg2rad(lat_1km_grid)))
# Convert cell area to data coordinates
cell_area_3d = cell_area.broadcast_like(ds_ba_data_eur_fire_1km)
# Convert units from km2 to hectares
ds_ba_data_eur_fire_1km['cell_area_ha'] = cell_area_3d * 100
# Rearrange order of coordinates to match data
ds_ba_data_eur_fire_1km['cell_area_ha'] = ds_ba_data_eur_fire_1km['cell_area_ha'].transpose('time', 'lat', 'lon')

# Remove metadata from original data
ds_ba_data_eur_fire_1km.attrs.clear()
# Output filename
ba_eur_flname_output = 'rs_veg_europe_fires_none_mon_2010_2021_v1_esacci.nc'

# Metadata
ds_ba_data_eur_fire_1km.attrs['Filename'] = ba_eur_flname_output
ds_ba_data_eur_fire_1km.attrs['Variables'] = 'fires, forest_fires, cell_area_ha'
ds_ba_data_eur_fire_1km.attrs['Units'] = 'ha'
ds_ba_data_eur_fire_1km.attrs['Data_source'] = 'ECMWF C3S Pixel OLCI Burned Area product'
ds_ba_data_eur_fire_1km.attrs['Time_period'] = '2017-2022'
ds_ba_data_eur_fire_1km.attrs['Time_averaging'] = 'Monthly'
ds_ba_data_eur_fire_1km.attrs['Spatial_extent'] = 'Europe'
ds_ba_data_eur_fire_1km.attrs['Coordinate_system'] = 'EPSG:4326'
ds_ba_data_eur_fire_1km.attrs['Author_names'] = 'Dr. Rocio Barrio Guillo, Dr. Jasdeep S. Anand'
# Save as a netcdf
ds_ba_data_eur_fire_1km.to_netcdf(f'{out_ba_dir}/{ba_eur_flname_output}')
