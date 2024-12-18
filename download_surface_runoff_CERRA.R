# Script Description:
# This script automates the retrieval of 3-hourly surface pressure data from the Copernicus Climate Data Store (CDS) using the ECMWF Reanalysis (CERRA) dataset.
# It:
# 1. Sets the CDS API key for user authentication.
# 2. Scans the directory containing already downloaded surface pressure data to identify years for which data is missing.
# 3. Constructs a data request for each missing year, specifying parameters such as the variable (surface pressure), 3-hourly time steps, and output format.
# 4. Sends the requests to the CDS API and saves the downloaded files in a specified folder with filenames reflecting the year and data resolution.
# The data is saved in GRIB format with filenames such as 'surface_pressure_03h_1984.grib'.
## The downloaded data (output) has the following properties:
# 1. spatial extend : domain spans from northern Africa beyond the northern tip of Scandinavia.
# 2. spatial resolution: 5.5 km x 5.5 km hence a grid box has an area of 30.25km2
# In the west it ranges far into the Atlantic Ocean and in the east it reaches to the Ural Mountains. Herewith, it covers entire Europe.
# 3. temporal resolution: 3 hourly time step
# 4. units: kg m-2
# 5. projection: Lambert Conformal Conic EPSG:9802.
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
  strsplit("_|\\.") |>                                          # Split filenames into components
  do.call(rbind, .) |>                                           # Combine results into a matrix
  as_tibble() |>                                                 # Convert to tibble for easier manipulation
  filter(V2 == "03h") |>                                        # Filter for files with "03h" in their name
  select(V3) |>                                                  # Extract the year information (assumed in column V3)
  unlist() |>                                                    # Flatten to a numeric vector
  as.numeric()                                                   # Convert to numeric

# Exclude years for which data already exists
ani <- ani[!ani %in% ani_desc]

# Loop through the remaining years to request and download data
for (i in 1:length(ani)) {
  # Print the current year being processed
  print(ani[i])
  
  # Define the request parameters for the CDS API
  request <- list(
    "dataset_short_name" = "reanalysis-cerra-land",  # Dataset identifier
    "variable" = "surface_runoff",                 # Variable of interest
    "level_type" = "surface",                      # Data level type
    "product_type" = "forecast",                   # Product type (forecast data)
    "year"  = ani[i],                                # Year of interest
    "month" = c(1:12),                              # All months
    "day" = c(1:31),                                # All days
    "time" = seq(0, 21, 3),                         # 3-hourly intervals
    'leadtime_hour' = '3',                            # Forecast lead time in hours
    "target" = paste0("surface_runoff_03h_", ani[i], ".grib")  # Output filename
  )
  
  # Send the data request and download the data
  wf_request(
    request,
    user = "vlad.amihaesei@meteoromania.ro",        # CDS user identifier
    path  = "nc/cerra/surface_runoff"               # Directory to save the downloaded files
  )
}
