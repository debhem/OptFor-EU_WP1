# OptFor-EU_WP1 - Future climate projections
The scripts provided in this Projection-Data section provides code and guidance to download, re-project and time aggregate (e.g., monthly, seasonal scales, where needed) the future climate projections data from EURO-CORDEX Regional Climate Model (RCM) simulations (https://euro-cordex.net/) driven by Climate Model Intercomparison Project Phase 5 Global Climate Model (CMIP5 GCM - https://wcrp-cmip.org/cmip5/) experiments.

Please take a look below for more information on each script and visit the OptFor-EU project website (https://optforeu.eu/) for more details on the project.
============================================================
Downloading future climate variables
Authors: [Deborah Hemming, Murk Memon- Met Office UK]
Date: [15/01/2025]


**************************************

Description:
This set of python code and the ReadMe_Download file does the following tasks:
  i) Download - Provides steps and guidance needed to download future projected climate variables for use in the OptFor-EU project that are available from the CMIP5 EURO-CORDEX monthly data for future projections (2006-2050) covering the Europe domain
  ii) Harmonise - Rotate and regrid (to 1km) the native rotated polar coordinates to regular latitude/longitude grid for the Europe domain (West -44.75, East 65.25, South 21.75, North 72.75)
  iii) Output - Output the rotated and regridded monthly mean data, for each climate variable separately, for the Europe domain
