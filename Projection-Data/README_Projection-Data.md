# OptFor-EU_WP1 - Future climate projections
The scripts provided in this Projection-Data section provide code and guidance to download, process and re-project the future climate projections data for use in the OptFor-EU project. Climate projection data are from the EURO-CORDEX (European focused COordinated Regional climate Downscaling EXperiment) Regional Climate Model (RCM) simulations (https://euro-cordex.net/) driven by Climate Model Intercomparison Project Phase 5 Global Climate Model (CMIP5 GCM - https://wcrp-cmip.org/cmip5/) experiments. Details on the EURO-CORDEX models and variables utilised in OptFor-EU can be found in the project deliverable D1.3: "Develop open-access code to harmonise forest-climate data".  

Please take a look below for more information on each script and visit the OptFor-EU project website (https://optforeu.eu/) for more details on the project, including deliverables and outputs as they become available.

+++

#### Code developers: Dr Deborah Hemming and Dr Murk Memon, UK Met Office

#### Date of code release: 20th January 2025

+++
# Brief description of each file:

## Downloading future projection data...

__Filename__: Download_Instructions.md

__Description__: This file provides step-by-step instructions and guidance on how to download the future projected climate variables that are being used in OptFor-EU. These are from the CMIP5 EURO-CORDEX RCM simulations driven by future scenarios from 2006 to 2050, available from the Copernicus Data Store - CDS, https://cds.climate.copernicus.eu/

__Inputs__: List of RCMs, RCPs and variables needed and link to ESGF EURO-CORDEX portal at https://cordex.org/data-access/cordex-cmip5-data/cordex-cmip5-esgf/

__Outputs__: Data files for each variable, RCP and RCM downloaded

## Scripts for processing future projection data variables...

__Filename__: Process_Projection_Europe_??-??_2006_2050_Monthly.py

__Description__: ???

__Inputs__: EURO-CORDEX...

__Outputs__: ???
##

__Filename__: ??.py

__Description__: 

__Inputs__: EURO-CORDEX...

__Outputs__: 
##



???.py
  ii) Harmonise - Rotate and regrid (to 1km) the native rotated polar coordinates to regular latitude/longitude grid for the Europe domain (West -44.75, East 65.25, South 21.75, North 72.75)
  iii) Output - Output the rotated and regridded monthly mean data, for each climate variable separately, for the Europe domain
