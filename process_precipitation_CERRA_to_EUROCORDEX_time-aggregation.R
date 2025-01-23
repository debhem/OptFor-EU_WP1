###################################################################################################################################################
# Title: Script to aggregate CERRA Hourly Runoff Data

# Date: 20th January 2025

# Author: Vlad Alexandru AMIHĂESEI, MeteoRomania, National Meteorological Administration, Romania

# Description: Processes hourly precipitation data from the CERRA (Copernicus European Regional Reanalysis) dataset
#              Performs temporal aggregation to generate daily, monthly, yearly, and seasonal summaries
#              Standardizes units and remaps the data to align with the EURO-CORDEX gridProduces EFMI #8 Changes in Tree Cover Density
#              Resamples spatial resolution and subsets to the EURO CORDEX region domain

# Inputs: Hourly runoff data files in GRIB format located in the directory /media/vlad/Elements2/CERRA/raw/runoff/
#         EURO-CORDEX-compatible grid file: CERRA_lonlatgrid.txt

# Outputs: NetCDF files for daily, monthly, yearly, and seasonal aggregated runoff data saved in the same directory
#          Note: The naming convention of outputs follows the format: runoff_[TIMEFRAME]_[YEAR].nc

# Prerequisites: CDO (Climate Data Operators) must be installed and accessible from the command line
#                A valid EURO-CORDEX grid file is needed (CERRA_lonlatgrid.txt)

# Data Properties:
#   - Spatial extent: Covers Europe from northern Africa to the Ural Mountains, spanning the Atlantic Ocean in the west to Scandinavia in the north
#     The domain corners are shown below (larger than the EURO-CORDEX domain):
#          min_lon = -58.21
#          max_lon = 74.15
#          min_lat = 20.26
#          max_lat = 75.30
#   - Spatial resolution: 5.5 km x 5.5 km grid cells (30.25 km² per grid cell)
#   - Temporal resolution: Aggregation is performed on 3-hourly inputs
#   - Units: millimeters (mm)
#   - Projection: WGS64 (EPSG:4326)

# Instructions:
#   - Adjust file paths and directories to your local environment
#   - Ensure temporary file management is handled correctly by the script
###################################################################################################################################################

# Set working directory
setwd("~/D/2024/optforeu/")

# Define the directory containing input GRIB files and the EURO-CORDEX grid file
input_dir <- "/media/vlad/Elements2/CERRA/raw/precip"
eurocordex <- "CERRA_lonlatgrid.txt"

# List all GRIB files matching the pattern, specifically 3-hourly data ("03h")
files <- list.files(input_dir, pattern = ".grib$", full.names = TRUE)
files <- grep("03h", files, value = TRUE)

# Clean up temporary files from previous runs
unlink(list.files("tmp", full.names = TRUE))

# Create a temporary folder for intermediate processing, if not already existing
if (!dir.exists("tmp")) dir.create("tmp")

# Loop over each GRIB file for processing
for (i in seq_along(files)) {
  print(paste("Processing file:", files[i]))
  
  ## Generate output file names for daily, monthly, and yearly aggregations
  name.day <- gsub("grib", "nc", gsub("03h", "DAY", files[i]))
  name.mon <- gsub("grib", "nc", gsub("03h", "MON", files[i]))
  name.year <- gsub("grib", "nc", gsub("03h", "YEAR", files[i]))
  
  ## Daily Sum Calculation
  ## Use CDO to calculate daily sum from 3-hourly precip data:
  ## Adjust time by shifting 1 hour back (-1 hour)
  ## Set the attribute for precipitation units to mm
  system(paste0(
    "cdo -O daysum -shifttime,-1hour -setattribute,sro@units=mm ", files[i], " tmp/tmp_daysum.nc"
  ))
  
  ## Remap the daily data to EURO-CORDEX grid
  system(paste0(
    "cdo -P 7 remapbil,", eurocordex, " tmp/tmp_daysum.nc ", name.day
  ))
  
  ## Monthly Sum Calculation
  ## Use CDO to calculate monthly sum from 3-hourly data and remap to EURO-CORDEX grid
  system(paste0(
    "cdo -O monsum -shifttime,-1hour -setattribute,sro@units=mm ", files[i], " tmp/tmp_monsum.nc"
  ))
  system(paste0(
    "cdo -P 7 remapbil,", eurocordex, " tmp/tmp_monsum.nc ", name.mon
  ))
  
  ## Yearly Sum Calculation
  ## Compute yearly sum and remap to EURO-CORDEX grid
  system("cdo -O yearsum tmp/tmp_monsum.nc tmp/tmp_yearsum.nc")
  system(paste0(
    "cdo -P 7 remapbil,", eurocordex, " tmp/tmp_yearsum.nc ", name.year
  ))
  
  ## Clean up temporary files to save disk space
  unlink(list.files("tmp", full.names = TRUE))
}

# Seasonal Aggregation
# List all monthly files ("MON") and calculate seasonal sums
files.mon <- list.files("/media/vlad/Elements2/CERRA/raw/precip/", pattern = "MON", full.names = TRUE)
name.seas <- "/media/vlad/Elements2/CERRA/raw/precip/precip_SEAS_1984-2021.nc"

# Merge all monthly files into a single file and calculate seasonal sums
system(paste0(
  "cdo -O mergetime ", gsub(",", " ", noquote(toString(files.mon))), " tmp/tmp_merged.nc"
))
system(paste0(
  "cdo delete,timestep=1,145 -seassum tmp/tmp_merged.nc ", name.seas
))

# Optional: Validate Outputs Using R (Commented Out)
# library(terra)
# vf.day  <- terra::rast(name.day)
# vf.mon  <- terra::rast(name.mon)
# vf.year <- terra::rast(name.year)
# vf.seas <- terra::rast(name.seas)
# plot(vf.seas[[1:10]])
