###################################################################################################################################################
# Title: Script for Downloading CERRA Maximum 2m Temperature data

# Date: 10th December 2024

# Author: Vlad Alexandru AMIHĂESEI, MeteoRomania, National Meteorological Administration, Romania

# Description: Automates the retrieval of CERRA reanalyses data for the variable "maximum 2m temperature since previous post-processing"
#              It uses the R programming language with the "ecmwfr" library to download the CERRA climate data
#              Data are requested in 3-hour intervals from 1984 to 2021, excluding years which have already been downloaded
#              Data are processed in reverse order for prioritization                 
#              It...
#                1. Sets the Copernicus Data Store (CDS) API key for user authentication
#                2. Scans the directory containing already downloaded data to identify years for which data is missing
#                3. Constructs a data request for each missing year, specifying parameters 3-hourly time steps, and output format
#                4. Sends the requests to the CDS API and saves the downloaded files in a specified folder with filenames reflecting the year and data resolution
#              Data are saved in GRIB format with filenames such as '[EFMI_climate_variable]_03h_1984.grib'

# Inputs: Years of interest: 1984 to 2021
#         Existing files in the directory: "nc/cerra/tmax"
#         CDS API key and user credentials

# Outputs: GRIB files for the variable "maximum air temperature" 
#          Saved in the folder "nc/cerra/tmax" with the naming format "tmax_[year].grib" 
#          The downloaded data (output) has the following proprierties:
#            1. Spatial extent : domain spans from northern Africa beyond the northern tip of Scandinavia
#            2. Spatial resolution: 5.5 km x 5.5 km hence a grid box has an area of 30.25km
#               In the west it ranges far into the Atlantic Ocean and in the east it reaches to the Ural Mountains. Herewith, it covers the entire area of Europe
#            3. Temporal resolution: 3 hourly time step
#            4. Units: K (kelvin)
#            5. Projection: Lambert Conformal Conic EPSG:9802

# Prerequisites: A valid CDS API key configured using `ecmwfr`
#                Ensure the required libraries (`ecmwfr`, `dplyr`) are installed

# Instructions: Replace the placeholder API key and user details with your own
#               Run the script to fetch and save the data locally
###################################################################################################################################################

# Load required libraries
library(ecmwfr) # For accessing ECMWF data services and handling data requests
library(dplyr)  # For data manipulation (e.g., filtering, transforming data)

# Note: Uncomment and configure the following lines to set up the ECMWF CDS API key
# The API key is used to authenticate the user and access data from the CDS
# wf_set_key(service = "cds",
#            key = "47b85274-0e3f-40fa-8b3d-7e2ef2294bd9", # Replace with your actual key
#            user = "9924") # Replace with your user ID

# You can retrieve the key using:
# wf_set_key(service = "cds")

# The output should be the key you previously provided, for example:
# "XXXXXXXXXXXXXXXXXXXXXX"

# Retrieve your user key (example shown)
# wf_get_key(user = "alexandru.dumitrescu@gmail.com")

# Define the range of years for which data is required
ani <- 1984:2021  # Years from 1984 to 2021

# Loop through the years that still need data
for (i in 1:length(ani)) {
  ## Define the data request parameters
  request <- list(
    "dataset_short_name" = "reanalysis-cerra-single-levels",               # Dataset name (CERRA single levels)
    "variable" = "maximum_2m_temperature_since_previous_post_processing",  # Variable to download ()
    "data_type" = "reanalysis",                                            # Data type (reanalysis data)
    "product_type" = "forecast",                                           # Product type (forecast data)
    "year"  = ani[i],                                                      # Current year in the loop
    "month" = c(1:12),                                                     # All months (January to December)
    "day" = c(1:31),                                                       # All days in each month
    "time" = seq(0,21,3),                                                  # Daily time step (midnight)
    'leadtime_hour' = '3',                                                 # Lead time of 3 hours
    "level_type" = "surface_or_atmosphere",                                # Level type (surface or atmosphere)
    "target" = paste0("tmax_", ani[i], ".grib")                            # File name for the output (e.g., precip_24h_1984.grib)
  )
  
  ## Send the request to the CDS API and download the data
  wf_request(
    request,                   # Request parameters defined above
    user = "9924",             # User ID (replace with your actual user ID)
    path  = "nc/cerra/tmax"    # Path where the downloaded file will be saved
  )
}
