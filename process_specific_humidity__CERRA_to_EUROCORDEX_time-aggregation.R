###################################################################################################################################################
# Title: Script for processing CERRA Specific Humidity data

# Date: 20th January 2025

# Author: Vlad Alexandru AMIHĂESEI, MeteoRomania, National Meteorological Administration, Romania

# Description: Processes specific humidity data from CERRA (Copernicus European Regional Reanalysis) files
#              The data, available in 3-hour intervals, is aggregated to daily, monthly, yearly, and seasonal resolutions
#              The outputs are remapped to the EURO-CORDEX-compatible grid and units are standardized

# Inputs: Directory: "/media/vlad/Elements2/CERRA/raw/specific_humidity" (contains .grib files)
#                    EURO-CORDEX grid file: "CERRA_lonlatgrid.txt"

# Outputs: NetCDF files for daily, monthly, yearly, and seasonal aggregated data
#          Monthly specific humidity (NetCDF): "*_MON.nc"
#          Yearly specific humidity (NetCDF): "*_YEAR.nc"
#          Seasonal mean specific humidity (NetCDF): "specific_humidity_SEAS_1984-2021.nc"

# Prerequisites: CDO (Climate Data Operators) must be installed and accessible from the command line
#                Directory structure set up with write permissions for temporary files
#                Ensure the R libraries `terra` are installed if output verification is required

# Data Properties:
#   - Spatial extent: Covers Europe from northern Africa to the Ural Mountains, spanning the Atlantic Ocean in the west to Scandinavia in the north
#     The domain corners are shown below (larger than the EURO-CORDEX domain):
#          min_lon = -58.21
#          max_lon = 74.15
#          min_lat = 20.26
#          max_lat = 75.30
#   - Spatial resolution: 5.5 km x 5.5 km grid cells (30.25 km² per grid cell)
#   - Temporal resolution: Aggregation is performed on 3-hourly inputs
#   - Units: g of water vapour within a kg of air (g/kg)
#   - Projection: WGS64 (EPSG:4326)

# Instructions:
#   - Replace placeholder directories and filenames with the actual paths
#   - Execute the script to process all available .grib files for specific humidity
###################################################################################################################################################

# Set working directory
setwd("~/D/2024/optforeu/")

# List all input files and filter for 3-hour interval GRIB files
files <- list.files("/media/vlad/Elements2/CERRA/raw/specific_humidity", pattern = ".grib$", full.names = TRUE)
files <- grep("03h", files, value = TRUE)

# Specify the EURO-CORDEX grid file
eurocordex <- "CERRA_lonlatgrid.txt"

# Remove any temporary files from previous runs
unlink(list.files("tmp", full.names = TRUE))

# Create a temporary directory if it doesn't exist
if (!dir.exists("tmp")) dir.create("tmp")

# Process each file
for (i in 1:length(files)) {
  
  print(paste("Processing file:", files[i]))
  
  ## Define output filenames
  name.day <- gsub("grib", "nc", gsub("03h", "DAY", files[i]))
  name.mon <- gsub("grib", "nc", gsub("03h", "MON", files[i]))
  name.year <- gsub("grib", "nc", gsub("03h", "YEAR", files[i]))
  
  ## Compute daily sum
  system(paste0("cdo -O daysum -shifttime,-1hour -setattribute,q@units=kg/kg ", files[i], " tmp/tmp_daysum.nc"))
  system(paste0("cdo -P 7 remapbil,", eurocordex, " tmp/tmp_daysum.nc ", name.day))
  
  ## Compute monthly sum
  system(paste0("cdo -O monsum -shifttime,-1hour -setattribute,q@units=kg/kg ", files[i], " tmp/tmp_monsum.nc"))
  system(paste0("cdo -P 7 remapbil,", eurocordex, " tmp/tmp_monsum.nc ", name.mon))
  
  ## Compute yearly sum
  system("cdo -O yearsum tmp/tmp_monsum.nc tmp/tmp_yearsum.nc")
  system(paste0("cdo -P 7 remapbil,", eurocordex, " tmp/tmp_yearsum.nc ", name.year))
  
  ## Remove temporary files
  unlink(list.files("tmp", full.names = TRUE))
}

# Process seasonal mean
files.mon <- list.files("/media/vlad/Elements2/CERRA/raw/specific_humidity", pattern = "MON", full.names = TRUE)
name.seas <- "/media/vlad/Elements2/CERRA/raw/specific_humidity/specific_humidity_SEAS_1984-2021.nc"
system(paste0("cdo -O mergetime ", gsub(",", " ", noquote(toString(files.mon))), " tmp/tmp_merged.nc"))
system(paste0("cdo delete,timestep=1,144 -seasmean tmp/tmp_merged.nc ", name.seas))

# Optional: Verify outputs using the `terra` package
# library(terra)
# vf.day <- terra::rast(name.day)
# vf.mon <- terra::rast(name.mon)
# vf.year <- terra::rast(name.year)
# vf.seas <- terra::rast(name.seas)
# plot(vf.seas[[1:4]])
