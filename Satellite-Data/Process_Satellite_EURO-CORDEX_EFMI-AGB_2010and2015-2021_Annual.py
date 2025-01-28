__author__ = "Dr. Rocio Barrio Guillo, Dr. Jasdeep S. Anand"
__other_citations__ = ["Millington, J., & This EDS book notebook contributors. Exploring Land Cover Data (Impact Observatory) (Jupyter Notebook) published in the Environmental Data Science book (Version v1.0.2) [Computer software]",
                    "Santoro, M.; Cartus, O. (2024): ESA Biomass Climate Change Initiative (Biomass_cci): Global datasets of forest above-ground biomass for the years 2010, 2015, 2016, 2017, 2018, 2019, 2020 and 2021, v5. NERC EDS Centre for Environmental Data Analysis, 22 August 2024. doi:10.5285/02e1b18071ad45a19b4d3e8adafa2817"]
__version__ = "1"
__description__ = "Produces EFMI #4.1 Carbon Stored in living biomass. Resamples the spatial resolution and subsets to the EURO CORDEX region domain, and is multiplied by 0,5 to get the Carbon stock"
__inputs__ = "ESA-CCI biomass map v5, at 100m resolution, for 2010 and 2015-2021, with units Mg/ha. Data was downloaded manually from https://data.ceda.ac.uk/neodc/esacci/biomass/data/agb/maps/v5.0/netcdf"
__outputs__ = "File named rs_veg_europe_agb_none_ann_2010_2021_v1_esacci.nc, at 1km resolution, for 2010 and 2015-2021, with units tonnes/ha"

import glob
import xarray as xr
import numpy as np
import os
import re
from datetime import datetime

# Local directory path where downloaded data is stored
out_top_dir = '/data/atsr/OptForEU'
agb_dir = f'{out_top_dir}/ESACCI_AGB'
# Local directory path where output will be saved
out_agb_dir = f'{agb_dir}/Europe/input/remote_sensing/vegetation/'
if not os.path.exists(out_agb_dir):
    os.makedirs(out_agb_dir)

# EURO-CORDEX Domain
eur_min_lon = -44.75
eur_max_lon = 65.25
eur_min_lat = 21.75
eur_max_lat = 72.75
# Search for files within download local directory
agb_filename_yr = glob.glob(f'{agb_dir}/*.nc')
# Open files as an xarray
agb_data = xr.open_mfdataset(agb_filename_yr, engine="h5netcdf")
# Get rid of variables we don't need
agb_data = agb_data.drop_vars(['time_bnds',
                                'lat_bnds',
                                'lon_bnds',
                                'crs',
                                'agb_sd'
                                ])
# Convert dates to datetime
dates = agb_data.time.values
year = dates.astype('datetime64[Y]').astype(int) + 1970
# Select data within the EURO-CORDEX domain
agb_lat, agb_lon = agb_data.lat.values, agb_data.lon.values
agb_lon_ind_range = np.where((agb_lon >= eur_min_lon) & (agb_lon <= eur_max_lon))[0]
agb_lat_ind_range = np.where((agb_lat >= eur_min_lat) & (agb_lat <= eur_max_lat))[0]
# Crop the data to the EURO-CORDEX domain
agb_data_eur = agb_data.isel(
                            lat = agb_lat_ind_range,
                            lon = agb_lon_ind_range
                            )

# Resample from 100m resolution to 1km
agb_data_eur_1km = agb_data_eur.coarsen(lon=10, lat=10, boundary="trim").mean()
agb_data_eur_1km = agb_data_eur_1km.assign_coords(time=year)
agb_data.close()

# Mutiply AGB by 0.5 to get Carbon stock
agb_data_eur_1km['carbon_stock'] = agb_data_eur_1km['agb'] * 0.5
agb_data_eur_1km = agb_data_eur_1km.drop_vars(['agb'])

# Erase previous metadata
agb_data_eur_1km.attrs.clear()
# Filename
agb_eur_flname_output = 'rs_veg_europe_agb_none_ann_2010_2021_v1_esacci.nc'
# Metadata
agb_data_eur_1km.attrs['Filename'] = agb_eur_flname_output
agb_data_eur_1km.attrs['Variables'] = 'carbon_stock'
agb_data_eur_1km.attrs['Units'] = 'tons_per_ha'
agb_data_eur_1km.attrs['Data_source'] = 'ESA-CCI biomass map v5'
agb_data_eur_1km.attrs['Time_period'] = '2010 and 2015-2021'
agb_data_eur_1km.attrs['Time_averaging'] = 'Annual'
agb_data_eur_1km.attrs['Spatial_extent'] = 'Europe'
agb_data_eur_1km.attrs['Coordinate_system'] = 'EPSG:4326'
agb_data_eur_1km.attrs['Author_names'] = 'Dr. Rocio Barrio Guillo, Dr. Jasdeep S. Anand'

# Save processed data to a netcdf
agb_data_eur_1km.to_netcdf(f'{out_agb_dir}/{agb_eur_flname_output}')
