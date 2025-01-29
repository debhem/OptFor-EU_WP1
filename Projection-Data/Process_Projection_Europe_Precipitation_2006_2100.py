###################################################################################################################################################
# Title: Script for Concatenating and Regridding Future Climate Scenarios of EURO-CORDEX Precipitation data

# Date: 20th January 2025

# Author: Dr Deborah Hemming and Dr Murk Memon, Met Office Hadley Centre, Met Office, UK

# Description: Code to concatenate (if needed) and regrid future projection data from EURO-CORDEX regional climate models (RCM) for monthly mean climate variables
#              Uses python programming language with the Climate Data Operators - cdo software (https://code.mpimet.mpg.de/projects/cdo)
#              Future projections of climate variables from 2 RCM (HIRHAM5 and RACMO22E) and 3 future scenarios (RCP26, RCP45, RCP85) are used in OptFor-EU
#              Data can be downloaded from the Copernicus CLimate Data Store (CDS) using guidance provided in the Download_Instructions.md file (provided in this repository)
#                 - Data from the CDS downloads as NetCDF files separated in 5-year time chunks (to limit file size)
#                 - If needed, code are provided here (currently commented out) to concatenate these chunks to a single time series
#              Regridding is conducted from the EURO-CORDEX rotated polar to regular lat/long coordinates (EPSG:4326), using an ERA4-Land file as lat/long coordinate template

# Inputs: Years of interest: 2006 to 2100
#         With the naming format "/path/to/Europe/[MODEL]/[SCENARIO]/[variable]/
#         EURO-CORDEX RCM climate projection data for monthly mean variable: e.g. precipitation flux
#            - for 2 RCM - HIRHAM5 and RACMO22E
#            - and 3 future scenarios - RCP26, RCP45, RCP85

# Outputs: NetCDF time series files (2006-2100) for monthly mean variable: e.g. precipitation flux
#          With the naming format "/path/to/Europe/[MODEL]/[SCENARIO]/[variable]/concat/[variable]_Europe_[MODEL]_[SCENARIO]_mon_2006_2100.nc" # Insert correct variable, MODEL and RCP
#          The downloaded data (output) has the following proprierties:
#            1. Spatial extent : EURO-CORDEX RCM domain across Europe (regridded to regular lat/long grid)
#            2. Spatial resolution: EUR-11 resolution 0.11 degree, ~12.5 x 12.5 km gridbox
#            3. Temporal resolution: monthly mean
#            4. Units: e.g. kg m-2 
#            5. Projection/coordinate system/reference code: EPSG:4326 (based on WGS84)

# Instructions: See Download_Instruction.md file for guidance on downloading these data from the CDS
#               ***Note***: There may be memory issues when slicing and regridding large datasets. If faced with memory errors, process 5-year files first then concatenate at the end
###################################################################################################################################################

#Load the required modules/packages
# import glob   # Un-comment this if using def concatenate_input_files(files, file_conc):
import os
from cdo import Cdo
import iris
import netCDF

# *** If needed *** If data have been downloaded from CDS it will be in 5-year time chunks, these will need concatenating into a single NetCDF file
   ## The function 'concatenate_input_files(files, file_conc) does the following...
   ## Concatenate data files from saved folder 'files' e.g...
   ## files = /path/to/Europe/[MODEL]/[SCENARIO]/[variable]/
   ## Save as single NetCDF file 'file_conc' e.g...
   ## file_conc = /path/to/Europe/[MODEL]/[SCENARIO]/[variable]/concat/
   ## To run this function remove commented out code in def concatenate_input_files(files, file_conc): and the call to this in def main() below

# def concatenate_input_files(files, file_conc):
#    cube_list = iris.load(files)
#    for item in cube_list:
#       item.attributes = []
#    cube = cube_list.concatenate_cube()
#    iris.save(cube, file_conc)
#    print()

# If the time series of data are available as a single NetCDF file continue below...

# Regrid the native EURO-CORDEX rotated polar coordinate system to regular lat/long using ERA5_Land file 'latlong_grid' as template
def regrid(infile, grid, outfile):
    cdo = Cdo()
    cdo.remapbil(grid, input=infile, output=outfile) # Performs bilinear interpolation to regrid the EURO-CORDEX data to the ERA5-Land grid


def main():
   # Location of the input model NetCDF data file
   [variable]_input_nc = '/path/to/EURO-CORDEX/[MODEL]/[SCENARIO]/[variable]/concat/[variable]_EURO-CORDEX_[MODEL]_[SCENARIO]_mon_2006_2100.nc' # Insert correct variable, MODEL and SCENARIO
   ## e.g... precipitation_output_nc = '/path/to/EURO-CORDEX/HIRHAM5/RCP26/concat/precipitation_EURO-CORDEX_HIRHAM5_RCP26_mon_2006_2100.nc' # Example path/filename for concatenated data
   
   # Location of the processed, output NetCDF data file
   [variable]_output_nc = '/path/to/Europe/[MODEL]/[SCENARIO]/[variable]/concat/[variable]_Europe_[MODEL]_[SCENARIO]_mon_2006_2100.nc' # Insert correct variable, MODEL and SCENARIO
   ## e.g... precipitation_output_nc = '/path/to/Europe/HIRHAM5/RCP26/concat/precipitation_Europe_HIRHAM5_RCP26_mon_2006_2100.nc' # Example path/filename for concatenated data

   # Location of the reference ERA5_Land lat/long coordinate file used to regrid the rotated polar EURO-CORDEX data
   latlong_grid = '/path/to/ERA5_Land/era5_land_t2.nc'

   # *** If needed *** Concatenate files and save single NetCDF file
   ## filepath_in = "/path/to/EURO-CORDEX/[MODEL]/[SCENARIO]/[variable]_monthly/" # Insert correct MODEL, RCP and variable
   ## filenames = glob.glob(f"{filepath_in}[variable]_[MODEL]_[SCENARIO]_*.nc") # Insert correct MODEL, RCP and variable
   ## concatenate_input_files(files=filenames, file_conc=[variable]_input.nc) # Insert correct variable

    # regrid the input file
    regrid(infile=[variable]_input_nc, grid=latlong_grid, outfile=[variable]_output_nc) # Insert correct variable

    # Close datasets
    [variable]_output_nc.close() # Insert correct variable
    [variable]_input_nc.close() # Insert correct variable

if __name__ == '__main__':
    main()
