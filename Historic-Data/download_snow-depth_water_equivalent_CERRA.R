###################################################################################################################################################
# Title: Script for Downloading CERRA 3-hourly snow-depth water equivalent (swe) data

# Date: 11th December 2024

# Author: Vlad Alexandru AMIHĂESEI, MeteoRomania, National Meteorological Administration, Romania

# Description: Automates the retrieval of CERRA reanalyses data for the variable "snow-depth water equivalent"
#              It uses the R programming language with the "ecmwfr" library to download the CERRA climate data
#              Data are requested in 3-hour intervals from 1984 to 2021, excluding years which have already been downloaded
#              Data are processed in reverse order for prioritization                 
#              It...
#                1. Sets the Copernicus Data Store (CDS) API key for user authentication
#                2. Scans the directory containing already downloaded data to identify years for which data is missing
#                3. Constructs a data request for each missing year, specifying parameters such as the variable (specific humidity), model level, 3-hourly time steps, and output format
#                4. Sends the requests to the CDS API and saves the downloaded files in a specified folder with filenames reflecting the year and data resolution
#              Data are saved in GRIB format with filenames such as 'swe_03h_1984.grib'

# Inputs: Years of interest: 1984 to 2021
#         Existing files in the directory: "nc/cerra/swe"
#         CDS API key and user credentials

# Outputs: GRIB files for the variable "snow-depth water equivalent" 
#          Saved in the folder "nc/cerra/swe/" with the naming 
#          Format "swe_3h_[year].grib"
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

# Load the required libraries
library(ecmwfr)  # Provides tools to interact with the CDS API
library(dplyr)   # Used for data manipulation, such as filtering and working with data frames

# Set the CDS API key for authentication. Replace with your own key and user details
wf_set_key(
  service = "cds",                                  # Specifies the CDS service
  key = "47b85274-0e3f-40fa-8b3d-7e2ef2294bd9",     # Your personal API key for accessing CDS
  user = "9924"                                     # Your user ID for the CDS service
)

# Define the range of years for which data is being requested
ani <- 1984:2021  # A sequence of years from 1984 to 2021

# Identify which years already have data downloaded
ani_desc <-
  list.files("nc/cerra/swe/", pattern = "*.grib") |>  # List all files in the specified directory matching the `.grib` pattern
  strsplit("_|\\.") |>                                # Split file names by underscores (_) and periods (.)
  do.call(rbind, .) |>                                # Combine the split results into a matrix
  as_tibble() |>                                      # Convert the matrix into a tibble (data frame)
  filter(V2 == "03h") |>                              # Keep only rows where the second column (V2) is "03h" (3-hourly data)
  select(V3) |>                                       # Select the third column (V3), which corresponds to years in file names
  unlist() |>                                         # Convert the tibble column into a simple vector
  as.numeric()                                        # Convert the character vector into numeric values

# Filter out years for which data has already been downloaded
ani <- ani[!ani %in% ani_desc]  # Retain only the years not present in `ani_desc`

# Loop through each year and request data for "snow depth water equivalent"
for (i in 1:length(ani)) {  # Iterate over each remaining year in `ani`
  
  # Define the request parameters for the CDS API
  request <- list(
    "dataset_short_name" = "reanalysis-cerra-single-levels",  # CERRA reanalysis dataset for single levels
    "variable" = "snow_depth_water_equivalent",               # Variable of interest: snow depth water equivalent
    "data_type" = "reanalysis",                               # Data type: reanalysis
    "product_type" = "forecast",                              # Product type: forecast
    "year"  = ani[i],                                         # Year for the data request
    "month" = c(1:12),                                        # All months of the year
    "day" = c(1:31),                                          # All possible days in a month
    "time" = seq(0, 21, 3),                                   # Time steps every 3 hours (00:00 to 21:00)
    "leadtime_hour" = "3",                                    # Lead time of 3 hours
    "level_type" = "surface_or_atmosphere",                   # Data is at surface or atmosphere level
    "target" = paste0("swe_03h_", ani[i], ".grib")            # Name of the output file, including year
  )
  
  # Submit the request to the CDS API
  wf_request(
    request,                             # Request parameters defined above
    user = "9924",                       # User ID for the CDS service
    path = "nc/cerra/swe"                # Directory to save the output data files
  )
}
