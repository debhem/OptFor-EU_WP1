# ============================================================
# Script for Downloading CERRA 10m Wind Speed Data
# Author: [MeteoRo]
# Date: [11/12/2024]
#
# Description:
# This script automates the retrieval of CERRA reanalysis data 
# for the "10m wind speed" variable. The data is requested for 
# years between 1984 and 2021 at 3-hour intervals. 
# It excludes years for which the data has already been downloaded.
#
# Inputs:
# - Years of interest: 1984 to 2021
# - Existing files in the directory: "nc/cerra/ws"
# - CDS API key and user credentials
#
# Outputs:
# - GRIB files for the variable "10m wind speed" 
#   saved in the folder "nc/cerra/ws" with the naming format "ws_[year].grib".
#
# Prerequisites:
# - A valid CDS API key configured using `ecmwfr`.
# - Ensure the required libraries (`ecmwfr`, `dplyr`) are installed.
#
# Instructions:
# - Replace placeholder API key and user details with your own.
# - Run the script to fetch and save the data locally.
#
# ============================================================
# The data is saved in GRIB format with filenames such as 'tmin_03h_1984.grib'.

## The downloaded data (output) has the following proprierties:
# 1. spatial extend : domain spans from northern Africa beyond the northern tip of Scandinavia.
# 2. spatial resolution: 5.5 km x 5.5 km hence a grid box has an area of 30.25km2
# In the west it ranges far into the Atlantic Ocean and in the east it reaches to the Ural Mountains. Herewith, it covers entire Europe.
# 3. temporal resolution: 3 hourly time step
# 4. units: m/s
# 5. projection: Lambert Conformal Conic EPSG:9802.

# Load the required libraries
library(ecmwfr)  # Provides tools to interact with the Copernicus Climate Data Store (CDS) API.
library(dplyr)   # Used for data manipulation, such as filtering and working with data frames.

# Set the CDS API key for authentication. Replace with your own key and user details.
# wf_set_key(
#   service = "cds",                                  # Specifies the CDS service.
#   key = "47b85274-0e3f-40fa-8b3d-7e2ef2294bd9",    # Your personal API key for accessing CDS.
#   user = "9924"                                    # Your user ID for the CDS service.
# )

# Uncomment the following line to retrieve the stored key for verification.
# wf_get_key(user = "alexandru.dumitrescu@gmail.com")

# Define the range of years for which data is being requested
ani <- 1984:2021  # A sequence of years from 1984 to 2021.

# Identify which years already have data downloaded
ani_desc <-
  list.files("nc/cerra/ws", pattern = "*.grib") |>  # List all files in the specified directory matching the `.grib` pattern.
  strsplit("_|\\.") |>                              # Split file names by underscores (_) and periods (.).
  do.call(rbind, .) |>                              # Combine the split results into a matrix.
  as_tibble() |>                                    # Convert the matrix into a tibble (data frame).
  select(V2) |>                                     # Select the second column (V2), which corresponds to years in file names.
  unlist() |>                                       # Convert the tibble column into a simple vector.
  as.numeric()                                      # Convert the character vector into numeric values.

# Filter out years for which data has already been downloaded
ani <- ani[!ani %in% ani_desc]  # Retain only the years not present in `ani_desc`.

# Loop through each year and request data for "10m wind speed"
for (i in 1:length(ani)) {  # Iterate over each remaining year in `ani`.
  
  # Define the request parameters for the CDS API
  request <- list(
    "dataset_short_name" = "reanalysis-cerra-single-levels",  # CERRA reanalysis dataset for single levels.
    "variable" = "10m_wind_speed",                           # Variable: 10m wind speed.
    "data_type" = "reanalysis",                              # Data type: reanalysis.
    "product_type" = "analysis",                             # Product type: analysis (fixed typo in original script).
    "year"  = ani[i],                                        # Year for the data request.
    "month" = c(1:12),                                       # All months of the year.
    "day" = c(1:31),                                         # All possible days in a month.
    "time" = seq(0, 21, 3),                                  # Time steps every 3 hours (00:00 to 21:00).
    "level_type" = "surface_or_atmosphere",                  # Data is at surface or atmosphere level.
    "target" = paste0("ws_", ani[i], ".grib")                # Name of the output file, including year.
  )
  
  # Submit the request to the CDS API
  wf_request(
    request,                             # Request parameters defined above.
    user = "9924",                       # User ID for the CDS service.
    path = "nc/cerra/ws"                 # Directory to save the output data files.
  )
}
