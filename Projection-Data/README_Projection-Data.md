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

__Filename__: Process_Projection_Europe_Downward_longradiation_2006_2050_Monthly.py

__Description__: Radiative longwave flux of energy incinding on the surface from the above per unit area. This is from the CMIP5 EURO-CORDEX RCM simulations driven by future scenarios from 2006 to 2050, for details on the variable, see: https://cds.climate.copernicus.eu/datasets/projections-cordex-domains-single-levels?tab=overview

__Inputs__: "Surface thermal radiation downward" variable monthly mean data for each MODEL and RCP used in OptFor-EU. The data can either be in 5-year chunks (directly from the EURO-CORDEX portal, see Download_Instructions.md) or as a concatenated time series file from 2006-2100.

__Outputs__: Surface thermal radiation dowward flux monthly mean time series from 2006-2100 with European (West -44.75, East 65.25, South 21.75, North 72.75) lat/long coordinates.
##

__Filename__: Process_Projection_Europe_Downward_shortradiation_2006_2050_Monthly.py

__Description__: The downward shortwave radiative flux of energy per unit area. The data represents the mean over the aggregation period at the surface. This is from the CMIP5 EURO-CORDEX RCM simulations driven by future scenarios from 2006 to 2050, for details on the variable, see: https://cds.climate.copernicus.eu/datasets/projections-cordex-domains-single-levels?tab=overview

__Inputs__: "Surface solar radiation downward" variable monthly mean data for each MODEL and RCP used in OptFor-EU. The data can either be in 5-year chunks (directly from the EURO-CORDEX portal, see Download_Instructions.md) or as a concatenated time series file from 2006-2100.

__Outputs__: Surface solar radiation dowward flux monthly mean time series from 2006-2100 with European (West -44.75, East 65.25, South 21.75, North 72.75) lat/long coordinates.
##

__Filename__: Process_Projection_Europe_Evaporation_2006_2050_Monthly.py

__Description__: Mass of surface and sub-surface liquid water per unit area ant time, which evaporates from land. The data includes conversion to vapour phase from both the liquid and solid phase, i.e., includes sublimation, and represents the mean over the aggregation period. This is from the CMIP5 EURO-CORDEX RCM simulations driven by future scenarios from 2006 to 2050, for details on the variable, see: https://cds.climate.copernicus.eu/datasets/projections-cordex-domains-single-levels?tab=overview

__Inputs__: "Evaporation" variable monthly mean data for each MODEL and RCP used in OptFor-EU. The data can either be in 5-year chunks (directly from the EURO-CORDEX portal, see Download_Instructions.md) or as a concatenated time series file from 2006-2100.

__Outputs__: Evaporation flux monthly mean time series from 2006-2100 with European (West -44.75, East 65.25, South 21.75, North 72.75) lat/long coordinates.
##

__Filename__: Process_Projection_Europe_Max_airtemp_2006_2050_Monthly.py

__Description__: Maximum temperature of the air near the surface. The data represents the daily maximum at 2m above the surface. This is from the CMIP5 EURO-CORDEX RCM simulations driven by future scenarios from 2006 to 2050, for details on the variable, see: https://cds.climate.copernicus.eu/datasets/projections-cordex-domains-single-levels?tab=overview

__Inputs__: "Maximum 2m temperature in the last 24 hours" variable monthly mean data for each MODEL and RCP used in OptFor-EU. The data can either be in 5-year chunks (directly from the EURO-CORDEX portal, see Download_Instructions.md) or as a concatenated time series file from 2006-2100.

__Outputs__: Maximum air temperature flux monthly mean time series from 2006-2100 with European (West -44.75, East 65.25, South 21.75, North 72.75) lat/long coordinates.
##

__Filename__: Process_Projection_Europe_Mean_airtemp_2006_2050_Monthly.py

__Description__: Mean temperature of the air near the surface. Ambient air temperature. The data represents the mean over the aggregation period at 2m above the surface. This is from the CMIP5 EURO-CORDEX RCM simulations driven by future scenarios from 2006 to 2050, for details on the variable, see: https://cds.climate.copernicus.eu/datasets/projections-cordex-domains-single-levels?tab=overview

__Inputs__: "2m temperature" variable monthly mean data for each MODEL and RCP used in OptFor-EU. The data can either be in 5-year chunks (directly from the EURO-CORDEX portal, see Download_Instructions.md) or as a concatenated time series file from 2006-2100.

__Outputs__: Mean air temperature flux monthly mean time series from 2006-2100 with European (West -44.75, East 65.25, South 21.75, North 72.75) lat/long coordinates.
##

__Filename__: Process_Projection_Europe_Min_airtemp_2006_2050_Monthly.py

__Description__: Minimum temperature of the air near the surface. The data represents the daily minimum at 2m above the surface. This is from the CMIP5 EURO-CORDEX RCM simulations driven by future scenarios from 2006 to 2050, for details on the variable, see: https://cds.climate.copernicus.eu/datasets/projections-cordex-domains-single-levels?tab=overview

__Inputs__: "Minimum 2m temperature in the last 24 hours" variable monthly mean data for each MODEL and RCP used in OptFor-EU. The data can either be in 5-year chunks (directly from the EURO-CORDEX portal, see Download_Instructions.md) or as a concatenated time series file from 2006-2100.

__Outputs__: Minimum air temperature flux monthly mean time series from 2006-2100 with European (West -44.75, East 65.25, South 21.75, North 72.75) lat/long coordinates.
##

__Filename__: Process_Projection_Europe_Precipitation_2006_2050_Monthly.py

__Description__: Deposition of water to the Earth s surface in the form of rain, snow, ice or hail. The precipitation flux is the mass of water per unit area and time. The data represents the mean over the aggregation period. This is from the CMIP5 EURO-CORDEX RCM simulations driven by future scenarios from 2006 to 2050, for details on the variable, see: https://cds.climate.copernicus.eu/datasets/projections-cordex-domains-single-levels?tab=overview

__Inputs__: "Mean precipitation flux" variable monthly mean data for each MODEL and RCP used in OptFor-EU. The data can either be in 5-year chunks (directly from the EURO-CORDEX portal, see Download_Instructions.md) or as a concatenated time series file from 2006-2100.

__Outputs__: Mean precipitation flux monthly mean time series from 2006-2100 with European (West -44.75, East 65.25, South 21.75, North 72.75) lat/long coordinates.
##

__Filename__: Process_Projection_Europe_Runoff_2006_2050_Monthly.py

__Description__: The mass of surface and sub-surface liquid water per unit area and time, which drains from land. The data represents the mean over the aggregation period. This is from the CMIP5 EURO-CORDEX RCM simulations driven by future scenarios from 2006 to 2050, for details on the variable, see: https://cds.climate.copernicus.eu/datasets/projections-cordex-domains-single-levels?tab=overview

__Inputs__: "Total run-off flux" variable monthly mean data for each MODEL and RCP used in OptFor-EU. The data can either be in 5-year chunks (directly from the EURO-CORDEX portal, see Download_Instructions.md) or as a concatenated time series file from 2006-2100.

__Outputs__: Total runoff flux monthly mean time series from 2006-2100 with European (West -44.75, East 65.25, South 21.75, North 72.75) lat/long coordinates.
##

__Filename__: Process_Projection_Europe_Sealevel_pressure_2006_2050_Monthly.py

__Description__: Pressure of air at the lower boundary of the atmosphere. The data represents the mean over the aggregation period. This is from the CMIP5 EURO-CORDEX RCM simulations driven by future scenarios from 2006 to 2050, for details on the variable, see: https://cds.climate.copernicus.eu/datasets/projections-cordex-domains-single-levels?tab=overview

__Inputs__: "Surface pressure" variable monthly mean data for each MODEL and RCP used in OptFor-EU. The data can either be in 5-year chunks (directly from the EURO-CORDEX portal, see Download_Instructions.md) or as a concatenated time series file from 2006-2100.

__Outputs__: Surface pressure monthly mean time series from 2006-2100 with European (West -44.75, East 65.25, South 21.75, North 72.75) lat/long coordinates.
##

__Filename__: Process_Projection_Europe_Specific_humidity_2006_2050_Monthly.py

__Description__: Amount of moisture in the air at 2m above the surface divided by the amount of air plus moisture at that location. This is from the CMIP5 EURO-CORDEX RCM simulations driven by future scenarios from 2006 to 2050, for details on the variable, see: https://cds.climate.copernicus.eu/datasets/projections-cordex-domains-single-levels?tab=overview

__Inputs__: "2m specific humidity" variable monthly mean data for each MODEL and RCP used in OptFor-EU. The data can either be in 5-year chunks (directly from the EURO-CORDEX portal, see Download_Instructions.md) or as a concatenated time series file from 2006-2100.

__Outputs__: Specific humidity monthly mean time series from 2006-2100 with European (West -44.75, East 65.25, South 21.75, North 72.75) lat/long coordinates.
##

__Filename__: Process_Projection_Europe_Wind_speed_2006_2050_Monthly.py

__Description__: The magnitude of the two-dimensional horizontal air velocity. The data represents the mean over the aggregation period at 10m above the surface. This is from the CMIP5 EURO-CORDEX RCM simulations driven by future scenarios from 2006 to 2050, for details on the variable, see: https://cds.climate.copernicus.eu/datasets/projections-cordex-domains-single-levels?tab=overview

__Inputs__: "10m Wind Speed" variable monthly mean data for each MODEL and RCP used in OptFor-EU. The data can either be in 5-year chunks (directly from the EURO-CORDEX portal, see Download_Instructions.md) or as a concatenated time series file from 2006-2100.

__Outputs__: Wind speed monthly mean time series from 2006-2100 with European (West -44.75, East 65.25, South 21.75, North 72.75) lat/long coordinates.
##

