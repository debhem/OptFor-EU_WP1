__author__ = "Dr. Jasdeep S. Anand, Dr. Rocio Barrio Guillo"
__credits__ = ["Dr. Jasdeep S. Anand", "Dr. Rocio Barrio Guillo", "Dr. Darren Ghent", ]
__other_citations__ = "Ghent, D.; Veal, K.; Perry, M. (2022): ESA Land Surface Temperature Climate Change Initiative (LST_cci): Monthly land surface temperature from MODIS (Moderate resolution Infra-red Spectroradiometer) on Terra, level 3 collated (L3C) global product (2000-2018), version 3.00. NERC EDS Centre for Environmental Data Analysis, 28 June 2022. doi:10.5285/32d7bc64c7b740e9ad7a43589ab91592. https://dx.doi.org/10.5285/32d7bc64c7b740e9ad7a43589ab91592"
__version__ = "1"
__description__ = "Produces EFMI #17.6 Mean monthly land surface temperature. Subsets to the EURO CORDEX region domain and gets LST monthly mean by averaging daily day-time data and daily night-time and then taking the mean of day-time and night-time monthly averages."
__inputs__ = "ESA-CCI MODIS Terra dataset, at 1km resolution, daily for 2000 to 2018, with units of Kelvin, K. The data was already downloaded in a JASMIN server from the CEDA Archive."
__outputs__ = "Files named rs_veg_europe_lst_none_mon_2000_2018_v1_esacci.nc, at 1km resolution, monthly mean from March 2000 to December 2018, in Kelvin."

from glob import glob
from pathlib import Path
import xarray as xr
from functools import partial
import pandas as pd
import numpy as np
import time
import datetime
import csv
import os
import logging
import sys

def process_month(this_year, month_n, p_terra_modis, tod='DAY'):
    # Find daily files for daytime
    terra_modis_daily_files = glob(f'{p_terra_modis}{this_year}/{month_n}/*/*{tod}*.nc')

    # Open data and get monthly mean
    with xr.open_mfdataset(terra_modis_daily_files, engine='netcdf4') as terra_daily_data_og:
        # Remove unnecessary variables
        terra_daily_data_lst = terra_daily_data_og.drop_vars(list_vars_drop)
        # Crop to European domain
        terra_daily_data_eur = terra_daily_data_lst.sel(
                                    lat=slice(min_lat_eur, max_lat_eur),
                                    lon=slice(min_lon_eur, max_lon_eur)
                                )
        # Take monthly mean
        # Add a new 'year_month' coordinate
        terra_daily_data_eur_my = terra_daily_data_eur.assign_coords(
            year_month=pd.to_datetime(terra_daily_data_eur['time'].values).to_period('M')
        )

        terra_daily_data_eur_my = terra_daily_data_eur_my.drop_vars('time')
        terra_daily_data_eur_my = terra_daily_data_eur_my.rename({'time': 'year_month'})

        # Group by 'year_month' and compute the mean
        terra_monthly_mean = terra_daily_data_eur_my.groupby('year_month').mean(dim='year_month')

        return terra_monthly_mean

# Make list of year-month for all files
date_list = pd.date_range(start='2000-03', end='2021-12', freq='MS').strftime('%Y-%m').tolist()

for slurm_arr_yr in date_list:
    # Validate the format "YYYY-MM"
    try:
        this_year, this_month = slurm_arr_yr.split('-')
        if len(this_year) != 4 or len(this_month) != 2:
            raise ValueError
    except ValueError:
        print("Error: Date must be in 'YYYY-MM' format.")
        sys.exit(1)

    print(f"Year: {this_year}, Month: {this_month}")

    # Local path to directory in JASMIN where data has been downloaded to
    path_terra_modis = '/gws/nopw/j04/esacci_lst/public/TERRA_MODIS_L3C_0.01/4.00/'
    #path_terra_modis = '/data/atsr/OptForEU/ESACCI_LST/Terra_MODIS/'

    # Local path to directory in JASMIN to save outputs
    out_data_topdir = '/gws/pw/j07/leicester/OPTFOREU/EFMI_LST'
    #out_data_topdir = '/data/atsr/OptForEU/ESACCI_LST'
    if not os.path.exists(out_data_topdir):
        os.makedirs(out_data_topdir)

    # EURO-CORDEX Domain
    min_lon_eur = -44.75
    max_lon_eur = 65.25
    min_lat_eur = 21.75
    max_lat_eur = 72.75

    # List of variables in dataset that we don't need
    list_vars_drop = ['dtime', 'satze', 'sataz', 'solze', 'solaz', 'qual_flag',
                        'lst_uncertainty','lst_unc_ran', 'lst_unc_loc_atm',
                        'lst_unc_loc_sfc', 'lst_unc_sys', 'lcc', 'ndvi', 'emis',
                        't2m', 'n', 'ncld', 'skt', 'channel']


    terra_monthly_day_mean = process_month(this_year, this_month, path_terra_modis, tod='DAY')
    terra_monthly_night_mean = process_month(this_year, this_month, path_terra_modis, tod='NIGHT')

    terra_combined_mean = (terra_monthly_day_mean + terra_monthly_night_mean) / 2
    terra_combined_mean = terra_combined_mean.assign_coords(year_month=terra_combined_mean["year_month"].astype(str))
    terra_combined_mean.load()
    lst_out_filename = f'{this_year}_{this_month}.nc'
    terra_combined_mean.to_netcdf(f'{out_data_topdir}/{lst_out_filename}', format='NETCDF4')

# Once all the above has ran, we can join all months in one netcdf
terra_modis_mon_files = glob(f'{out_data_topdir}/*.nc')
lst_mon_data = xr.open_mfdataset(terra_modis_mon_files, engine='netcdf4')

lst_mon_data.attrs = {}
# Filename to save output as
lst_out_filename = 'rs_veg_europe_lst_none_mon_2000_2018_v1_esacci.nc'

# Metadata
lst_mon_data.attrs['Filename'] = lst_out_filename
lst_mon_data.attrs['Variables'] = 'lst'
lst_mon_data.attrs['Units'] = 'K'
lst_mon_data.attrs['Data_source'] = 'ESA LST CCI MODIST L3U V3.00'
lst_mon_data.attrs['Time_period'] = 'March 2000-December 2018'
lst_mon_data.attrs['Time_averaging'] = 'Monthly'
lst_mon_data.attrs['Spatial_extent'] = 'Europe'
lst_mon_data.attrs['Coordinate_system'] = 'EPSG:4326'
lst_mon_data.attrs['Author_names'] = 'Dr. Rocio Barrio Guillo, Dr. Jasdeep S. Anand'
# Save as netcdf
lst_mon_data.to_netcdf(f'{out_data_topdir}/{lst_out_filename}', format='NETCDF4')
