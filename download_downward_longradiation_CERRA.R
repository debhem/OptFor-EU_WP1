# ============================================================
# Script for Downloading CERRA Longwave Radiation Data
# Author: [MeteoRO]
# Date: [11/12/2024]
#
# Description:
# This script automates the retrieval of CERRA reanalysis data 
# for the variable "surface thermal radiation downwards."
# The data is requested for years 1984 to 2021 at 3-hour intervals.
# It excludes years for which the data has already been downloaded.
# The years are processed in reverse order for prioritization.
#
# Inputs:
# - Years of interest: 1984 to 2021
# - Existing files in the directory: "nc/cerra/solar_downward_long/"
# - CDS API key and user credentials.
#
# Outputs:
# - GRIB files for the variable "surface thermal radiation downwards" 
#   saved in the folder "nc/cerra/solar_downward_long/" with the naming 
#   format "solar_downward_long_03h_[year].grib".
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
## The downloaded data (output) has the following proprierties:
# 1. spatial extend : domain spans from northern Africa beyond the northern tip of Scandinavia.
# 2. spatial resolution: 5.5 km x 5.5 km hence a grid box has an area of 30.25km2
# In the west it ranges far into the Atlantic Ocean and in the east it reaches to the Ural Mountains. Herewith, it covers entire Europe.
# 3. temporal resolution: 3 hourly time step
# 4. units: J m-2
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
  list.files("nc/cerra/solar_downward_long/", pattern = "*.grib") |>  # List files in the specified directory matching `.grib`.
  strsplit("_|\\.") |>                                                # Split file names by underscores (_) and periods (.).
  do.call(rbind, .) |>                                                # Combine split results into a matrix.
  as_tibble() |>                                                      # Convert the matrix into a tibble (data frame).
  filter(V4 == "03h") |>                                              # Filter rows where the fourth column (V4) equals "03h".
  select(V5) |>                                                       # Select the fifth column (V5), which corresponds to years.
  unlist() |>                                                         # Convert the tibble column into a simple vector.
  as.numeric()                                                        # Convert the character vector into numeric values.

# Filter out years for which data has already been downloaded, then reverse the order
ani <- ani[!ani %in% ani_desc] |> rev()  # Retain only the years not present in `ani_desc` and reverse the order.

# Loop through each year and request data for the variable
for (i in 1:length(ani)) {  # Iterate over each remaining year in `ani`.
  
  # Define the request parameters for the CDS API
  request <- list(
    "dataset_short_name" = "reanalysis-cerra-single-levels",          # CERRA reanalysis dataset for single levels.
    "variable" = "surface_thermal_radiation_downwards",               # Variable: surface thermal radiation downwards.
    "data_type" = "reanalysis",                                      # Data type: reanalysis.
    "product_type" = "forecast",                                     # Product type: forecast.
    "year"  = ani[i],                                                # Year for the data request.
    "month" = c(1:12),                                               # All months of the year.
    "day" = c(1:31),                                                 # All possible days in a month.
    "time" = seq(0, 21, 3),                                          # Time steps every 3 hours (00:00 to 21:00).
    "leadtime_hour" = "3",                                           # Lead time in hours.
    "level_type" = "surface_or_atmosphere",                          # Data is at surface or atmosphere level.
    "target" = paste0("solar_downward_long_03h_", ani[i], ".grib")   # Name of the output file, including year.
  )
  
  # Submit the request to the CDS API
  wf_request(
    request,                                  # Request parameters defined above.
    user = "9924",                            # User ID for the CDS service.
    path = "nc/cerra/solar_downward_long",    # Directory to save the output data files.
    time_out = 3600 * 4                       # Timeout set to 4 hours to accommodate larger data requests.
  )
}