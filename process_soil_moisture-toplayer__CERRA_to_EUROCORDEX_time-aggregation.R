###################################################################################################################################################
# Title: Script for processing CERRA 3-hourly Soil Moisture data

# Date: 20th January 2025

# Author: Vlad Alexandru AMIHĂESEI, MeteoRomania, National Meteorological Administration, Romania

# Description: This script processes CERRA soil moisture data for the topsoil layer at 3-hourly intervals. It performs temporal aggregation to 
#              daily, monthly, and yearly timescales, along with seasonal averages. The outputs are remapped to a common grid (EURO-CORDEX).

# Inputs:  Source data files: GRIB files for soil moisture data located in "/media/vlad/Elements2/CERRA/raw/soilmoisture-top/"
#          EURO-CORDEX grid file: "CERRA_lonlatgrid.txt"
#          Temporal resolution: 3-hourly data ("03h" included in file names)

# Outputs: NetCDF files for daily, monthly, yearly, and seasonal aggregated data
#          Daily soil moisture (NetCDF): "*_DAY.nc"
#          Monthly soil moisture (NetCDF): "*_MON.nc"
#          Yearly soil moisture (NetCDF): "*_YEAR.nc"
#          Seasonal mean soil moisture (NetCDF): "soilmoisture-top_SEAS_1984-2021.nc"

# Prerequisites: CDO (Climate Data Operators) must be installed and accessible from the command line
#                Required permissions to read/write in the specified directories

# File naming conventions:
#   Daily: Replace "03h" with "DAY"
#   Monthly: Replace "03h" with "MON"
#   Yearly: Replace "03h" with "YEAR"
#   Seasonal: "soilmoisture-top_SEAS_1984-2021.nc"

# Data Properties:
#   - Spatial extent: Covers Europe from northern Africa to the Ural Mountains, spanning the Atlantic Ocean in the west to Scandinavia in the north
#     The domain corners are shown below (larger than the EURO-CORDEX domain):
#          min_lon = -58.21
#          max_lon = 74.15
#          min_lat = 20.26
#          max_lat = 75.30
#   - Spatial resolution: 5.5 km x 5.5 km grid cells (30.25 km² per grid cell)
#   - Temporal resolution: Aggregation is performed on 3-hourly inputs
#   - Units: mm
#   - Projection: WGS64 (EPSG:4326)

# Instructions:
#   - Adjust file paths and directories to your local environment
#   - Ensure temporary file management is handled correctly by the script
###################################################################################################################################################

# Set working directory
setwd("~/D/2024/optforeu/")

# List and filter input files
files <- list.files("/media/vlad/Elements2/CERRA/raw/soilmoisture-top/", pattern = ".grib$", full.names = TRUE)
files <- grep("03h", files, value = TRUE)
eurocordex <- "CERRA_lonlatgrid.txt"

# Remove temporary files
unlink(list.files("tmp", full.names = TRUE))

# Create temporary directory if it does not exist
if (!dir.exists("tmp")) dir.create("tmp")

# Process each file
for (i in 1:length(files)) {
  print(files[i])
  
  ## Define output file names
  name.day <- gsub("grib", "nc", gsub("03h", "DAY", files[i]))
  name.mon <- gsub("grib", "nc", gsub("03h", "MON", files[i]))
  name.year <- gsub("grib", "nc", gsub("03h", "YEAR", files[i]))
  
  ## Daily sum
  system(paste0("cdo -O daysum -shifttime,-1hour -setattribute,vsw@units=m3/m3 ", files[i], " tmp/tmp_daysum.nc"))
  system(paste0("cdo -P 7 remapbil,", eurocordex, " tmp/tmp_daysum.nc ", name.day))
  
  ## Monthly sum
  system(paste0("cdo -O monsum -shifttime,-1hour -setattribute,vsw@units=m3/m3 ", files[i], " tmp/tmp_monsum.nc"))
  system(paste0("cdo -P 7 remapbil,", eurocordex, " tmp/tmp_monsum.nc ", name.mon))
  
  ## Yearly sum
  system("cdo -O yearsum tmp/tmp_monsum.nc tmp/tmp_yearsum.nc")
  system(paste0("cdo -P 7 remapbil,", eurocordex, " tmp/tmp_yearsum.nc ", name.year))
  
  ## Clean temporary files
  unlink(list.files("tmp", full.names = TRUE))
}

# Calculate seasonal means
files.mon <- list.files("/media/vlad/Elements2/CERRA/raw/soilmoisture-top/", pattern = "MON", full.names = TRUE)
name.seas <- "/media/vlad/Elements2/CERRA/raw/soilmoisture-top/soilmoisture-top_SEAS_1984-2021.nc"
system(paste0("cdo -O mergetime ", gsub(",", " ", noquote(toString(files.mon))), " tmp/tmp_merged.nc"))
system(paste0("cdo delete,timestep=1,149 -seasmean tmp/tmp_merged.nc ", name.seas))

# Optional: Check the outputs using the 'terra' package
# library(terra)
# vf.day <- terra::rast(name.day)
# vf.mon <- terra::rast(name.mon)
# vf.year <- terra::rast(name.year)
# vf.seas <- terra::rast(name.seas)
# plot(vf.seas[[1:4]])
