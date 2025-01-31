# Instructions and guidance for downloading the EURO-CORDEX future projection data used in OptFor-EU
The EURO-CORDEX RCM output files were downloaded from the ESGF EURO CORDEX portal at https://cordex.org/data-access/cordex-cmip5-data/cordex-cmip5-esgf/
This was carried out using the WGET scripts method on a Linux terminal (see guidance steps below)
Details of this and other methods to access the EURO-CORDEX model output can be found in the user guide at https://esgf.github.io/esgf-user-support/user_guide.html 

Two EURO-CORDEX RCMs were selected for use in OptFor-EU... 
- RACMO22E (Royal Netherlands Meteorological Institute (KNMI) - https://www.wdc-climate.de/ui/entry?acronym=CXEU11KNRA)
- HIRHAM5 (Danish Meteorological Institute (DMI) - https://backend.orbit.dtu.dk/ws/portalfiles/portal/51950450/HIRHAM.pdf)

...and three Representative Concentration Pathways (RCPs)...
RCP2.6, RCP4.5, and RCP8.5 - https://www.metoffice.gov.uk/binaries/content/assets/metofficegovuk/pdf/research/ukcp/ukcp18-guidance---representative-concentration-pathways.pdf

Only monthly average data were downloaded. This is the shortest time averaging needed by the OptFor-EU Decision Support System (DSS), and any longer time averages e.g. seasonal, annual, will be calculated during development of the DSS
#
The following steps were taken to download the future projection data for each RCM and RCP from the ESGF EURO CORDEX portal:

1) Open the ESGF portal (https://esgf-metagrid.cloud.dkrz.de/search/cordex-dkrz/) from a web browser in a Linux terminal
2) Set the required search criteria e.g. for monthly HIRHAM5 RCP2.6 use the following: CORDEX (under the Project tab), output (Product tab), EUR-11 (Domain tab), rcp26 (experiment tab), r1i1p1 (Ensemble tab), HIRHAM5 (RCM tab), MOHC-HadGEM2-ES (driving model tab) and mon (Time Frequency tab). Click on Search
3) Select the required variables from the Variable long name tab (e.g. near-surface temperature, near-surface relative humidity, downwelling shortwave radiation, precipitation...) and click on Search
   ...this search should return the number of results (the variables) which need to be downloaded
5) Download the wget-script for each dataset
6) Place each wget-script in the output folder to save/download the data in
   
   Top tip: Rename the wget-script as e.g. wget-temp.sh for temperature, because the wget names are tedious to type into the terminal in the following steps...keep the wget in the filename because this is needed to run the scripts
8) Open a terminal in the directory where the data needs to be saved and where the wget-script was placed
9) The wget-script for each variable needs to be run separately on the Linux terminal (in the directory where you need it saved) by issuing command...
   bash wget-???.sh -H
   ...from the terminal prompt (the ??? refers to the name you have changed the wget command to e.g. bash wget-temp.sh -H)
11) You will get a prompt to enter your username and password of your ESGF account (you can’t see it, but it is getting typed)
12) The climate data files should start downloading in the relevant directories
13) Enjoy a cup of tea :)
