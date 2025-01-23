# OptFor-EU_WP1 - Historic climate data (from CERRA reanalysis)

The scripts provided in this Historic-CERRA Data section provide code to download, re-project, time aggregate (e.g., monthly, seasonal scales), and spatially crop the Copernicus Regional Reanalyses for Europe - CERRA (https://climate.copernicus.eu/copernicus-regional-reanalysis-europe-cerra) reanalyses data covering the recent past (1984-2021) for use in the OptFor-EU project. 

Please take a look below for more information on each script and visit the OptFor-EU project website (https://optforeu.eu/) for more details on the project.

+++

#### Authors: [Alex Dumitrescu; Vlad Amihaesei- MeteoRo]

#### Date: 10th December 2024

+++

## Brief description of each file

## Scripts for Downloading CERRA climate variables...

__Filename__: download_[EFMI_climate_variable]_CERRA.R

__Description__: Automates the retrieval of CERRA reanalyses data for climate variables to be used in OptFor-EU. 
                 Uses the R programming language with the "ecmwfr" library to download the CERRA climate data.
                 Data are requested in 3-hour intervals from 1984 to 2021, excluding years which have already been downloaded.

__Inputs__: Years of interest: 1984 to 2021.
            Existing files in the directory: "nc/cerra/ws".
            CDS API key and user credentials

__Outputs__: GRIB files for the climate variable saved in the folder "nc/cerra/[name_of_variable]" with the naming format "ws_[year].grib"

__Prerequisites__: A valid CDS API key configured using `ecmwfr`.
                   Ensure the required libraries (`ecmwfr`, `dplyr`) are installed.

__Instructions__: Replace the placeholder API key and user details with your own. 
                  Run the script to fetch and save the data locally
##

## Scripts for processing CERRA climate variables...

__Filename__: process_[EFMI_climate_variable]_CERRA_to_EURO-CORDEX_1984-2021_MonthlyMean.R

__Description__: Processes hourly precipitation data from the CERRA dataset.
                 Performs temporal aggregation to generate daily, monthly, yearly, and seasonal summaries.
                 Standardizes units and remaps the data to align with the EURO-CORDEX grid

__Inputs__: Hourly runoff data files in GRIB format located in the directory /media/vlad/Elements2/CERRA/raw/runoff/.
            EURO-CORDEX-compatible grid file: CERRA_lonlatgrid.txt
            
__Outputs__: NetCDF files for daily, monthly, yearly, and seasonal aggregated runoff data saved in the same directory.
             The naming convention for outputs follows the format: [climate_variable]_[TIMEFRAME]_[YEAR].nc
             
__Prerequisites__: CDO (Climate Data Operators) must be installed and accessible from the command line.
                   A valid EURO-CORDEX grid file (CERRA_lonlatgrid.txt)
##
