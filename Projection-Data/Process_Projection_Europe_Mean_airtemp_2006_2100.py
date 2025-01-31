###################################################################################################################################################
# Title: Script for Concatenating and Regridding Future Climate Scenarios of EURO-CORDEX Mean air temperature data

# Date: 20th January 2025

# Author: Dr Deborah Hemming and Dr Murk Memon, Met Office Hadley Centre, Met Office, UK

# Description: Code to concatenate (if needed) and regrid monthly mean future projection data from EURO-CORDEX regional climate models (RCM) for the variable "mean air temperature"
#              Uses python programming language with the Climate Data Operators - cdo software (https://code.mpimet.mpg.de/projects/cdo)
#              Future projections of climate variables from 2 RCM (HIRHAM5 and RACMO22E) and 3 future scenarios (RCP26, RCP45, RCP85) are used in OptFor-EU
#              Data can be downloaded from the Copernicus CLimate Data Store (CDS) using guidance provided in the Download_Instructions.md file (provided in this repository)
#                 - Data from the CDS downloads as NetCDF files separated in 5-year time chunks (to limit file size)
#                 - If needed, code are provided here (currently commented out) to concatenate these chunks to a single time series
#              Regridding is conducted from the EURO-CORDEX rotated polar to regular lat/long coordinates (EPSG:4326), using an ERA4-Land file as lat/long coordinate template

# Inputs: Years of interest: 2006 to 2100
#         EURO-CORDEX RCM climate projection data for monthly mean air temperature
#            - Downloaded as '2m temperature' in K, see https://cds.climate.copernicus.eu/datasets/projections-cordex-domains-single-levels?tab=overview
#            - With the naming format (for data in 5-year chunks) is "/path/to/EURO-CORDEX/RCP26/HIRHAM5/meantair_mon/meantair_europe_[MODEL]_[SCENARIO]_mon_2006_2100.nc" 
#                 - Or if time series are already concatenated the naming format is "/path/to/EURO-CORDEX/RCP26/HIRHAM5/concat/meantair_europe_[MODEL]_[SCENARIO]_mon_2006_2100.nc" 
#            - For 2 RCM - HIRHAM5 and RACMO22E
#            - And 3 future scenarios - RCP26, RCP45, RCP85

# Outputs: NetCDF time series files (2006-2100) for the variable "mean air temperature" 
#          With the naming format "/path/to/EURO-CORDEX/RCP26/HIRHAM5/concat/meantair_europe_[MODEL]_[SCENARIO]_mon_2006_2100.nc" 
#          The downloaded data (output) has the following proprierties:
#            1. Spatial extent : EURO-CORDEX RCM domain across Europe (regridded to regular lat/long grid)
#            2. Spatial resolution: EUR-11 resolution 0.11 degree, ~12.5 x 12.5 km gridbox
#            3. Temporal resolution: monthly mean
#            4. Units: K
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
   ## files = /path/to/EURO-CORDEX/RCP85/HIRHAM5/meantair_mon/
   ## Save as single NetCDF file 'file_conc' e.g...
   ## file_conc = /path/to/EURO-CORDEX/RCP85/HIRHAM5/concat/
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
def regrid(grid, infile, outfile):
    cdo = Cdo()
    cdo.remapbil(grid, input=infile, output=outfile) # Performs bilinear interpolation to regrid the EURO-CORDEX data to the ERA5-Land grid


def main():
   # Location of the input EURO-CORDEX HIRHAM5 mean air temperature data file/s
   # Assuming input file is already concatenated time series, if 5-year chunks either concatenate to single time series then regrid or regrid then concatenate
   meantair_input = '/path/to/EURO-CORDEX/RCP26/HIRHAM5/meantair_mon/meantair_mon.nc' # Change filenames to correct RCP and MODEL

   # Location of the processed, output EURO-CORDEX HIRHAM5 mean air temperature NetCDF data file
   meantair_output = '/path/to/EURO-CORDEX/RCP26/HIRHAM5/concat/meantair_europe_HIRHAM5_RCP26_mon_2006_2100.nc'

   # Location of the reference ERA5_Land lat/long coordinate file used to regrid the rotated polar EURO-CORDEX data
   latlong_grid = '/path/to/ERA5_Land/era5_land_evap_targetgrid.nc'

    # regrid the input file
    regrid(grid=latlong_grid, infile=meantair_input, outfile=meantair_output)

   # *** If needed *** Concatenate files and save single NetCDF file
   ## filepath_in = "/path/to/EURO-CORDEX/RCP26/HIRHAM5/meantair_mon/" # Change path name to correct RCP and MODEL
   ## filenames = glob.glob(f"{filepath_in}meantair_HIRHAM5_RCP26_*.nc") # Change filenames to correct MODEL and RCP
   ## concatenate_input_files(files=filenames, file_conc=meantair_output)

    # Close datasets
    meantair_output.close()
    meantair_input.close()

if __name__ == '__main__':
    main()
