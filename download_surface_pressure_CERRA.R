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
# 4. units: Pa
# 5. projection: Lambert Conformal Conic EPSG:9802.


# Load required libraries
library(ecmwfr) # For accessing ECMWF data services and handling data requests.
library(dplyr)  # For data manipulation (e.g., filtering, transforming data).

# Set the CDS API key for user authentication (replace with your actual key and user ID)
wf_set_key(service = "cds",
           key = "47b85274-0e3f-40fa-8b3d-7e2ef2294bd9", # Replace with your actual key
           user = "9924") # Replace with your user ID

# You can retrieve the key using:
# wf_set_key(service = "cds")

# The output should be the key you previously provided, for example:
# "XXXXXXXXXXXXXXXXXXXXXX"

# Retrieve your user key (example shown)
# wf_get_key(user = "alexandru.dumitrescu@gmail.com")

# Define the range of years for which data is required
ani <- 1984:2021  # Years from 1984 to 2021

# Check which years have already been downloaded
ani_desc <-
  list.files("nc/cerra/surface_pressure/", pattern = "*.grib") |>
  strsplit("_|\\.") %>% do.call(rbind, .) |> as_tibble() |> filter(V2 == "03h") |>
  select(V3) |> unlist() |> as.numeric()

# Identify years that are missing from the existing data
ani <- ani[!ani %in% ani_desc] # Exclude years already downloaded

# Loop through the missing years and request data
for (i in 1:length(ani)) {
  # Define the data request parameters
  request <- list(
    "dataset_short_name" = "reanalysis-cerra-single-levels",       # Dataset name (CERRA single levels)
    "variable" = "surface_pressure",                              # Variable to download (surface pressure)
    "data_type" = "reanalysis",                                   # Data type (reanalysis data)
    "product_type" = "analysis",                                  # Product type (analysis data)
    "year"  = ani[i],                                              # Current year in the loop
    "month" = c(1:12),                                             # All months (January to December)
    "day" = c(1:31),                                               # All days in each month
    "time" = seq(0, 21, 3),                                        # 3-hourly time steps
    'leadtime_hour' = '3',                                           # Lead time of 3 hours
    "level_type" = "surface_or_atmosphere",                       # Level type (surface or atmosphere)
    "target" = paste0("surface_pressure_03h_", ani[i], ".grib") # File name for the output (e.g., surface_pressure_03h_1984.grib)
  )
  
  # Send the request to the CDS API and download the data
  wf_request(
    request,                 # Request parameters defined above
    user = "9924",          # User ID (replace with your actual user ID)
    path  = "nc/cerra/surface_pressure" # Path where the downloaded file will be saved
  )
}
