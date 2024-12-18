# Script Description:
# This script automates the download of daily total precipitation data from the Copernicus Climate Data Store (CDS) using the ECMWF Reanalysis (CERRA) dataset.
# It:
# 1. Defines the range of years for which data is needed (1984-2021).
# 2. (Optional) Allows checking a directory for already downloaded files to avoid redundancy (currently commented out).
# 3. Constructs a data request for each year, specifying parameters such as variable (total precipitation), daily aggregation, and output format.
# 4. Sends the requests to the CDS API and saves the downloaded data files in the designated folder.
# The data downloaded is in GRIB format and is saved with filenames corresponding to the year (e.g., 'precip_24h_1984.grib').
### The downloaded data has the following proprierties:
# 1. spatial extend : domain spans from northern Africa beyond the northern tip of Scandinavia.
# 2. spatial resolution: 5.5 km x 5.5 km hence a grid box has an area of 30.25km2
# In the west it ranges far into the Atlantic Ocean and in the east it reaches to the Ural Mountains. Herewith, it covers entire Europe.
# 3. temporal resolution: 3 hourly time step
# 4. units: kg/m2 
# 5. projection: Lambert Conformal Conic EPSG:9802.

#########################################################################################################################################
####################################start downloading####################################################################################
#########################################################################################################################################

# Load required libraries
library(ecmwfr) # For accessing ECMWF data services and handling data requests.
library(dplyr)  # For data manipulation (e.g., filtering, transforming data).

# Note: Uncomment and configure the following lines to set up the ECMWF CDS API key.
# The API key is used to authenticate the user and access data from the Copernicus Data Store (CDS).
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
  # Define the data request parameters
  request <- list(
    "dataset_short_name" = "reanalysis-cerra-single-levels", # Dataset name (CERRA single levels)
    "variable" = "total_precipitation",                    # Variable to download (total precipitation)
    "data_type" = "reanalysis",                            # Data type (reanalysis data)
    "product_type" = "forecast",                           # Product type (forecast data)
    "year"  = ani[i],                                       # Current year in the loop
    "month" = c(1:12),                                      # All months (January to December)
    "day" = c(1:31),                                        # All days in each month
    "time" = '00:00',                                       # Daily time step (midnight)
    'leadtime_hour' = '24',                                   # Lead time of 24 hours
    "level_type" = "surface_or_atmosphere",                # Level type (surface or atmosphere)
    "target" = paste0("precip_24h_", ani[i], ".grib")     # File name for the output (e.g., precip_24h_1984.grib)
  )
  
  # Send the request to the CDS API and download the data
  wf_request(
    request,                 # Request parameters defined above
    user = "9924",          # User ID (replace with your actual user ID)
    path  = "nc/cerra/precip" # Path where the downloaded file will be saved
  )
}



