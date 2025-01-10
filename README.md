# OptFor-EU_WP1

### The scripts provided in the Historic-CERRA Data section provide code to download, reproject, time aggregate (e.g., monthly, seasonal scales), and crop the Copernicus Regional Reanalyses for Europe - CERRA (https://climate.copernicus.eu/copernicus-regional-reanalysis-europe-cerra) data for use in the OptFor-EU project. Please take a look below for more information on each script and visit the OptFor-EU project website (https://optforeu.eu/) for more details on the project.

### ============================================================
### Script for Downloading CERRA climate  variables
### Authors: [Alex Dumitrescu; Vlad Amihaesei- MeteoRo]
### Date: [10/12/2024]
#### download_[EFMI_climate_variable]_CERRA.R
## Description:
#### This script automates the retrieval of CERRA reanalysis data  for the "EFMI" climate variables. It uses the R programming language with the "ecmwfr" library to download the CERRA climate data. 
#### The data is requested in 3-hour intervals from 1984 to 2021, excluding years for which the data has already been downloaded. 
#### It:
#### 1. Sets the CDS API key for user authentication.
#### 2. Scans the directory containing already downloaded  data to identify years for which data is missing.
#### 3. Constructs a data request for each missing year, specifying parameters such as the variable (specific humidity), model level, 3-hourly time steps, and output format.
#### 4. Sends the requests to the CDS API and saves the downloaded files in a specified folder with filenames reflecting the year and data resolution.
#### The data is saved in GRIB format with filenames such as '[EFMI_climate_variable]_03h_1984.grib'.

### Inputs:
#### - Years of interest: 1984 to 2021
#### - Existing files in the directory: "nc/cerra/ws"
#### - CDS API key and user credentials

### Outputs:
#### - GRIB files for the climate variable saved in the folder "nc/cerra/[name_of_variable]" with the naming format "ws_[year].grib".

### Prerequisites:
#### - A valid CDS API key configured using `ecmwfr`.
#### - Ensure the required libraries (`ecmwfr`, `dplyr`) are installed.

### Instructions:
#### - Replace the placeholder API key and user details with your own.
#### - Run the script to fetch and save the data locally.

#### process_[EFMI_climate_variable]_CERRA_to_EURO-CORDEX_1984-2021_MonthlyMean.R
#### ============================================================
#### crop_[EFMI_climate_variable]_CSA_CERRA_monthly.R
#### ============================================================
