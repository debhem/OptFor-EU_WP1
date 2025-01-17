# OptFor-EU_WP1 - Future climate projections
The scripts provided in this Projection-Data section provides code and guidance to download, re-project, time aggregate (e.g., monthly, seasonal scales, where needed), and crop future climate projections data from EURO-CORDEX (https://euro-cordex.net/) regional climate model runs driven by CMIP5 GCM simulations.

(https://climate.copernicus.eu/copernicus-regional-reanalysis-europe-cerra) reanalyses data covering the recent past (1984-2021) for use in the OptFor-EU project. Please take a look below for more information on each script and visit the OptFor-EU project website (https://optforeu.eu/) for more details on the project.
============================================================
Downloading future climate variables
Authors: [Deborah Hemming, Murk Memon- Met Office UK]
Date: [15/01/2025]


**************************************
download_[EFMI_climate_variable]_CERRA.R
Description:
This script automates the retrieval of CERRA reanalyses data for climate variables to be used in OptFor-EU. It uses the R programming language with the "ecmwfr" library to download the CERRA climate data.
The data is requested in 3-hour intervals from 1984 to 2021, excluding years for which the data has already been downloaded.
**************************************

Description:
This set of python code does the following tasks:
  i) Download - Provides steps and guidance needed to download future projected climate variables for use in the OptFor-EU project that are available from the CMIP5 EURO-CORDEX monthly data for future projections (2006-2050) covering the Europe domain
  ii) Harmonise - Rotate and regrid (to 1km) the native rotated polar coordinates to regular latitude/longitude grid for the Europe domain (West -44.75, East 65.25, South 21.75, North 72.75)
  iii) Output - Output the rotated and regridded monthly mean data, for each climate variable separately, for the Europe domain
