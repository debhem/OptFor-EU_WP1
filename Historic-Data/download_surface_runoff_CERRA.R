###################################################################################################################################################
# Title: Script for Downloading CERRA 3-hourly Surface Runoff data

# Date: 11th December 2024

# Author: Vlad Alexandru AMIHĂESEI, MeteoRomania, National Meteorological Administration, Romania

# Description: Automates the retrieval of CERRA reanalyses data for the variable "surface runoff"
#              It uses the R programming language with the "ecmwfr" library to download the CERRA climate data
#              Data are requested in 3-hour intervals from 1984 to 2021, excluding years which have already been downloaded
#              Data are processed in reverse order for prioritization                 
#              It...
#                1. Sets the Copernicus Data Store (CDS) API key for user authentication
#                2. Scans the directory containing already downloaded data to identify years for which data is missing
#                3. Constructs a data request for each missing year, specifying parameters such as the variable (surface runoff), model level, 3-hourly time steps, and output format
#                4. Sends the requests to the CDS API and saves the downloaded files in a specified folder with filenames reflecting the year and data resolution
#              Data are saved in GRIB format with filenames such as 'surface_runoff_03h_1984.grib'

# Inputs: Years of interest: 1984 to 2021
#         Existing files in the directory: "nc/cerra/surface_runoff"
#         CDS API key and user credentials

# Outputs: GRIB files for the variable "surface_runoff" 
#          Saved in the folder "nc/cerra/surface_runoff/" with the naming 
#          Format "surface_runoff_3h_[year].grib"
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

# Load necessary libraries
library(ecmwfr)  # For interacting with the Copernicus Climate Data Store (CDS) API
library(dplyr)   # For data manipulation

# Key setup for the CDS API (commented out since the key should already be configured)
# wf_set_key(service = "cds",
#            key = "6ceb11e4-6bb1-4274-8a40-8e5b41628b9e")
# wf_get_key()

# Define the range of years for which data is required
ani <- 1984:2021

# Identify existing files in the target directory to avoid redundant downloads
ani_desc <-
  list.files("nc/cerra/surface_runoff/", pattern = "*.grib") |>  # List GRIB files in the directory
  strsplit("_|\\.") |>                                           # Split filenames into components
  do.call(rbind, .) |>                                           # Combine results into a matrix
  as_tibble() |>                                                 # Convert to tibble for easier manipulation
  filter(V2 == "03h") |>                                         # Filter for files with "03h" in their name
  select(V3) |>                                                  # Extract the year information (assumed in column V3)
  unlist() |>                                                    # Flatten to a numeric vector
  as.numeric()                                                   # Convert to numeric

# Exclude years for which data already exists
ani <- ani[!ani %in% ani_desc]

# Loop through the remaining years to request and download data
for (i in 1:length(ani)) {
  ## Print the current year being processed
  print(ani[i])
  
  ## Define the request parameters for the CDS API
  request <- list(
    "dataset_short_name" = "reanalysis-cerra-land",            # Dataset identifier
    "variable" = "surface_runoff",                             # Variable of interest
    "level_type" = "surface",                                  # Data level type
    "product_type" = "forecast",                               # Product type (forecast data)
    "year"  = ani[i],                                          # Year of interest
    "month" = c(1:12),                                         # All months
    "day" = c(1:31),                                           # All days
    "time" = seq(0, 21, 3),                                    # 3-hourly intervals
    'leadtime_hour' = '3',                                     # Forecast lead time in hours
    "target" = paste0("surface_runoff_03h_", ani[i], ".grib")  # Output filename
  )
  
  # Send the data request and download the data
  wf_request(
    request,
    user = "vlad.amihaesei@meteoromania.ro",        # CDS user identifier
    path  = "nc/cerra/surface_runoff"               # Directory to save the downloaded files
  )
}
