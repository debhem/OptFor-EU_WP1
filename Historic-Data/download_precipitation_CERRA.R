###################################################################################################################################################
# Title: Script for Downloading CERRA Daily Total Precipitation data

# Date: 11th December 2024

# Author: Vlad Alexandru AMIHĂESEI, MeteoRomania, National Meteorological Administration, Romania

# Description: Automates the retrieval of CERRA reanalyses data for the variable "precipitation"
#              It uses the R programming language with the "ecmwfr" library to download the CERRA climate data
#              Data are requested in 3-hour intervals from 1984 to 2021, excluding years which have already been downloaded
#              Data are processed in reverse order for prioritization                 
#              It...
#                1. Sets the Copernicus Data Store (CDS) API key for user authentication
#                2. Scans the directory containing already downloaded data to identify years for which data is missing
#                3. Constructs a data request for each missing year, specifying parameters such as the variable (specific humidity), model level, 3-hourly time steps, and output format
#                4. Sends the requests to the CDS API and saves the downloaded files in a specified folder with filenames reflecting the year and data resolution
#              Data are saved in GRIB format with filenames such as '[EFMI_climate_variable]_03h_1984.grib'

# Inputs: Years of interest: 1984 to 2021
#         Existing files in the directory: "nc/cerra/precip"
#         CDS API key and user credentials

# Outputs: GRIB files for the variable "precipitation" 
#          Saved in the folder "nc/cerra/precip/" with the naming 
#          Format "precip_24h_[year].grib"
#          The downloaded data (output) has the following proprierties:
#            1. Spatial extent : domain spans from northern Africa beyond the northern tip of Scandinavia
#            2. Spatial resolution: 5.5 km x 5.5 km hence a grid box has an area of 30.25km
#               In the west it ranges far into the Atlantic Ocean and in the east it reaches to the Ural Mountains. Herewith, it covers the entire area of Europe
#            3. Temporal resolution: 3 hourly time step
#            4. Units: kg/m2
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

# (Optional) Check which years have already been downloaded (currently commented out)
# ani_desc <- 
#   list.files("nc/cerra/precip/", pattern = "*.grib") |>
#   strsplit("_|\\.") %>% do.call(rbind,.) |> as_tibble() |> select(V3) |> unlist() |> as.numeric()
# ani <- ani[!ani %in% ani_desc]

# Loop through the years that still need data
for (i in 1:length(ani)) {
  ## Define the data request parameters
  request <- list(
    "dataset_short_name" = "reanalysis-cerra-single-levels",  # Dataset name (CERRA single levels)
    "variable" = "total_precipitation",                       # Variable to download (total precipitation)
    "data_type" = "reanalysis",                               # Data type (reanalysis data)
    "product_type" = "forecast",                              # Product type (forecast data)
    "year"  = ani[i],                                         # Current year in the loop
    "month" = c(1:12),                                        # All months (January to December)
    "day" = c(1:31),                                          # All days in each month
    "time" = '00:00',                                         # Daily time step (midnight)
    'leadtime_hour' = '24',                                   # Lead time of 24 hours
    "level_type" = "surface_or_atmosphere",                   # Level type (surface or atmosphere)
    "target" = paste0("precip_24h_", ani[i], ".grib")         # File name for the output (e.g., precip_24h_1984.grib)
  )
  
  ## Send the request to the CDS API and download the data
  wf_request(
    request,                   # Request parameters defined above
    user = "9924",             # User ID (replace with your actual user ID)
    path  = "nc/cerra/precip"  # Path where the downloaded file will be saved
  )
}
