# OptFor-EU_WP1 - Satellite data

### The scripts provided in this Satellite-Data section provide code to download, process, resample and spatially crop various satellite data for use in the OptFor-EU project. 
### Please take a look below for more information on each script and visit the OptFor-EU project website (https://optforeu.eu/) for more details on the project.

+++

__Code developers__: Dr. Jasdeep Anand and Dr. Rocio Barrio Guillo, University of Leicester, UK

__Date of code release__: 16th January 2025

+++

## Brief description of each file...

__Filename__: Process_Satellite_EURO-CORDEX_EFMI-AGB_2010and2015-2021_Annual.py

__Description__: Produces EFMI #4.1 Carbon Stored in living biomass. Resamples the spatial resolution and subsets to the EURO CORDEX region domain, and is multiplied by 0,5 to get the Carbon stock

__Inputs__: ESA-CCI biomass map v5, at 100m resolution, for 2010 and 2015-2021, with units Mg/ha. Data were downloaded manually from https://data.ceda.ac.uk/neodc/esacci/biomass/data/agb/maps/v5.0/netcdf

__Outputs__: File named rs_veg_europe_agb_none_ann_2010_2021_v1_esacci.nc, at 1km resolution, for 2010 and 2015-2021, with units tonnes/ha
##

__Filename__: Download_Satellite_Global_EFMI-FIRES_2001_2022_Monthly.py

__Description__: Downloads data for EFMI #7 Forest area damaged by fire

__Inputs__: C3S Copernicus burnt area dataset from OLCI, at 300m resolution, monthly for 2017-2022, unitless [presence/absence of fire within cell]

__Outputs__: Files named c3s_pixel_burned_area_v1_1_{year}_monthly.zip
##

__Filename__: Process_Satellite_EURO-CORDEX_EFMI-FIRES_2001_2022_Monthly.py

__Description__: Produces EFMI #7 Forest area damaged by fire. Selects the 'forest' land cover classes, resamples the spatial resolution and subsets to the EURO CORDEX region domain

__Inputs__: C3S Copernicus burnt area dataset from OLCI, at 300m resolution, monthly for 2017-2022, unitless [presence/absence of fire within cell]

__Outputs__: File named rs_veg_europe_fires_none_mon_2010_2021_v1_esacci.nc, at 1km resolution, monthly for 2017-2022, with variables: 'fires' (unitless, presence/absence fire in the cell for all land cover classes), 'forest_fires' (unitless, presence/absence fire in the cell for forest land cover classes), 'cell_area_ha' (Ha, the area of each cell)
##

__Filename__: Download_Satellite_EURO-CORDEX_EFMI-SoilCarbon_2015_2024_Daily.py

__Description__: Downloads the data for the EFMI #4.3 Carbon stored in forest soils

__Inputs__: NASA SMAP L4 Global Daily 9 km EASE-Grid Carbon Net Ecosystem Exchange, Version 7, at 9km resolution, daily for 2015-2024, with units gC/m2

__Outputs__: Files named SMAP_L4_C_mdl_{yyymmdd}T000000_Vv7041_001.h5, at 9km resolution, daily for 2015-2024, subset to EURO-CORDEX region, with units gC/m2
##

__Filename__: Process_Satellite_EURO-CORDEX_EFMI-SoilCarbon_2015_2024_Daily.py

__Description__: Produces EFMI #4.3 Carbon stored in forest soils. Resamples temporal resolution

__Inputs__: NASA SMAP L4 Global Daily 9 km EASE-Grid Carbon Net Ecosystem Exchange, Version 7, at 9km resolution, daily for 2015-2024, with units gC/m2

__Outputs__: File named rs_veg_europe_soilCarbon_none_mon_2015_2024_v1_smap.nc, at 9km resolution, monthly for 2015-2024, with units tonnes C/ha
##

Process_Satellite_EURO-CORDEX_EFMI-DisturbanceInsectsDisease_2010_2021_Events.py
__description__ = "Produces EFMI #5.1 Forest area with damage caused by insects and diseases. Subsets to the EURO CORDEX region domain"
__inputs__ = "DEFID2 database, at day/event of disturbance resolution, for 1963-08-01 to 2021-09-30, with units ha. Data was downloaded from Data was downloaded manually from https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/FOREST/DISTURBANCES/DEFID2/VER1-0/"
__outputs__ = "File named rs_veg_europe_disturbanceInsectsDisease_none_event_1963_2021_v1_defid2.shp, area shapefile, daily/event for 1963-08-01 to 2021-09-30, with units ha; and a file named metadata_rs_veg_europe_disturbanceInsectsDisease_none_event_1963_2021_v1_defid2.txt with the metadata for the shapefile.

Process_Satellite_EURO-CORDEX_EFMI-DisturbanceWeather_2010_2021_Events.py
__description__ = "Produces EFMI #6.1 Forest area with damage caused by severe weather events. Subsets to the EURO CORDEX region domain"
__inputs__ = "FORWIND database, at day/event of disturbance resolution, for 2000-07-25 to 2018-10-28, with units ha. Data was downloaded manually from https://figshare.com/articles/dataset/A_spatially-explicit_database_of_wind_disturbances_in_European_forests_over_the_period_2000-2018/9555008"
__outputs__ = "File named rs_veg_europe_disturbanceWeather_none_event_2000_2018_v1_forwind.shp, area shapefile, daily/event for 2000-07-25 to 2018-10-28, with units ha; and a file named metadata_rs_veg_europe_disturbanceWeather_none_event_2000_2018_v1_forwind.txt with the metadata for the shapefile."

Download_Satellite_Global_EFMI-ChangeTCD_2012_2015_2018_Annual.py
__description__ = "Downloads the data for the EFMI #8 Changes in Tree Cover Density."
__inputs__ = "Sentinel-2 Copernicus High-Resolution Layer Tree Cover Density dataset, at 100m resolution, annually for 2012, 2015 and 2018, with units %"
__outputs__ = "Files named TCD_{yyyy}_100m_eu_03035_d04_full.tif, at 100m resolution, annually for 2012, 2015 and 2018, with units %"

Process_Satellite_EURO-CORDEX_EFMI-ChangeTCD_2012_2015_2018_Annual.py
__description__ = "Produces EFMI #8 Changes in Tree Cover Density. Resamples spatial resolution and subsets to the EURO CORDEX region domain"
__inputs__ = "Sentinel-2 Copernicus High-Resolution Layer Tree Cover Density dataset, at 100m resolution, annually for 2012, 2015 and 2018, with units %"
__outputs__ = "Files named rs_veg_europe_changeTCD_none_ann_2015_v1_clms.tif and rs_veg_europe_changeTCD_none_ann_2018_v1_clms.tif, at 1km resolution, annually for 2015 and 2018 with respect to 2012, with units %"

Download_Satellite_Global_EFMI-LAI_2014_2024_10-Daily.py
__description__ = "Downloads data for EFMI #11 Leaf Area Index."
__inputs__ = "Copernicus Global Land Service LAI dataset, at 300m resolution, 10-daily for 2014 to present, globally, unitless. Note that data was used From January 2014 to August 2016 based upon RT5 PROBA-V and to June 2020 based upon RT0 PROBA-V data with version 1.0 and from July 2020 onwards based upon RT0 Sentinel-3/OLCI data with version 1.1. RT0 is the Near Real Time product while RT5 is the final consolidated Real Time product."
__outputs__ = "Files named c_gls_LAI300-RT0_{yyyymmdd}0000_GLOBE_OLCI_V1.1.2.nc or c_gls_LAI300-RT0_{yyymmdd}0000_GLOBE_PROBAV_V1.0.1.nc or c_gls_LAI300_{yyyymmdd}0000_GLOBE_PROBAV_V1.0.1.nc"

Process_Satellite_EURO-CORDEX_EFMI-LAI_2014_2024_10-Daily.py
__description__ = "Produces EFMI #11 Leaf Area Index. Resamples spatial resolution, resampled temporal resolution and subsets to the EURO CORDEX region domain"
__inputs__ = "Copernicus Global Land Service LAI dataset, at 300m resolution, 10-daily for 2014 to present, unitless. Note that data was used From January 2014 to August 2016 based upon RT5 PROBA-V and to June 2020 based upon RT0 PROBA-V data with version 1.0 and from July 2020 onwards based upon RT0 Sentinel-3/OLCI data with version 1.1. RT0 is the Near Real Time product while RT5 is the final consolidated Real Time product."
__outputs__ = "File named rs_veg_europe_lai_none_mon_2014_2024_v1_clms.nc, at 1km resolution, monthly from January 2014 to December 2023, unitless"

Process_Satellite_EURO-CORDEX_EFMI-LST_2000_2021_Daily.py
__description__ = "Produces EFMI #17.6 Mean monthly land surface temperature. Subsets to the EURO CORDEX region domain and gets LST monthly mean by averaging daily day-time data and daily night-time and then taking the mean of day-time and night-time monthly averages."
__inputs__ = "ESA-CCI MODIS Terra dataset, at 1km resolution, daily for 2000 to 2018, with units of Kelvin, K. The data was already downloaded in a JASMIN server from the CEDA Archive."
__outputs__ = "Files named rs_veg_europe_lst_none_mon_2000_2018_v1_esacci.nc, at 1km resolution, monthly mean from March 2000 to December 2018, in Kelvin."
