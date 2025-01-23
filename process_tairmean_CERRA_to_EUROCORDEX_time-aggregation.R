# Script for Aggregating Hourly Runoff Data from CERRA
# Author: [MeteoRo]
# Date: [20/01/2025]
# Description:
#   This script processes 3 hourly air temperature data from the CERRA (Copernicus European Regional Reanalysis) dataset.
# It performs temporal aggregation to generate daily, monthly, yearly, and seasonal summaries.
# The script also standardizes units and remaps the data to align with the EURO-CORDEX grid.
# Inputs:
#   - Hourly air temperature data files in GRIB format located in the directory /media/vlad/Elements2/CERRA/raw/tair/.
# - EURO-CORDEX-compatible grid file: CERRA_lonlatgrid.txt.
# Outputs:
#   - NetCDF files for daily, monthly, yearly, and seasonal aggregated runoff data saved in the same directory.
# - The naming convention for outputs follows the format: tair_[TIMEFRAME]_[YEAR].nc.
# Prerequisites:
#   - CDO (Climate Data Operators) must be installed and accessible from the command line.
# - A valid EURO-CORDEX grid file (CERRA_lonlatgrid.txt).
# Instructions:
#   - Adjust file paths and directories to your local environment.
# - Ensure temporary file management is handled correctly by the script.
# Data Properties:
#   - Spatial extent: Covers Europe from northern Africa to the Ural Mountains, spanning the Atlantic Ocean in the west to Scandinavia in the north.
# - Spatial resolution: 5.5 km x 5.5 km grid cells (30.25 km² per grid cell).
# - Temporal resolution: Aggregation is performed on 3-hourly inputs.
# - Units: degree celsius (°C).
# - Projection: WGS64 (EPSG:4326).

# Set working directory
setwd("~/D/2024/OPTforEU/")

# Define the directory containing input GRIB files and the EURO-CORDEX grid file
input_dir <- "/media/vlad/Elements2/CERRA/raw/tair"
eurocordex <- "~/D/2024/OPTforEU/CERRA_lonlatgrid.txt"

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
  
  ### Generate output file names for daily, monthly, and yearly aggregations
  name.day <- gsub("grib", "nc", gsub("03h", "DAY", files[i]))
  name.mon <- gsub("grib", "nc", gsub("03h", "MON", files[i]))
  name.year <- gsub("grib", "nc", gsub("03h", "YEAR", files[i]))
  
  ### Daily Mean Calculation
  # Use CDO to calculate daily mean from 3-hourly data:
  # - Adjust time by shifting 1 hour back (-1 hour)
  # - Convert temperature units from Kelvin to Celsius (subtract 273.15)
  system(paste0(
    "cdo -O daymean -shifttime,-1hour -sub,273.15 ", files[i], " tmp/tmp_daymean.nc"
  ))
  
  ### Monthly Aggregation
  # Change units from Kelvin to Celsius and remap data to EURO-CORDEX grid
  system(paste0(
    "cdo chunit,K,C tmp/tmp_daymean.nc tmp/tmp_monmean.nc"
  ))
  system(paste0(
    "cdo -P 7 remapbil,", eurocordex, " tmp/tmp_monmean.nc ", name.mon
  ))
  
  ### Yearly Aggregation
  # Compute yearly mean and remap to EURO-CORDEX grid
  system("cdo -O yearmean tmp/tmp_monmean.nc tmp/tmp_yearmean.nc")
  system(paste0(
    "cdo -P 7 remapbil,", eurocordex, " tmp/tmp_yearmean.nc ", name.year
  ))
  
  # Clean up temporary files to save disk space
  unlink(list.files("tmp", full.names = TRUE))
}

### Seasonal Aggregation
# List all monthly files ("MON") and calculate seasonal sums
files.mon <- list.files("/media/vlad/Elements2/CERRA/raw/precip/", pattern = "MON", full.names = TRUE)
name.seas <- "/media/vlad/Elements2/CERRA/raw/precip/precip_SEAS_1984-2021.nc"

# Merge all monthly files into a single file and calculate seasonal sums
system(paste0(
  "cdo -O mergetime ", gsub(",", " ", noquote(toString(files.mon))), " tmp/tmp_merged.nc"))
system(paste0(
  "cdo delete,timestep=1,146 -seasmean  tmp/tmp_merged.nc ", name.seas))

### Optional: Validate Outputs Using R (Commented Out)
# library(terra)
# vf.day  <- terra::rast(name.day)
# vf.mon  <- terra::rast(name.mon)
# vf.year <- terra::rast(name.year)
# vf.seas <- terra::rast(name.seas)
