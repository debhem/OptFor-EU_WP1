__author__ = "Dr. Jasdeep S. Anand, Dr. Rocio Barrio Guillo"
__other_citations__ = "Viana-Soto, A., & Senf, C. (2024). European Forest Disturbance Atlas (Version 2.1.1.). DOI: 10.5281/zenodo.13333034"
__version__ = "1"
__description__ = "Produces EFMI #5.1 Forest area with damage caused by insects and diseases"
__inputs__ = "Disturbance agent layer mosaic for Europe, at ~50m resolution, annual for 1985-2023, unitless [presence or absence of disturban agents within cell]"
__outputs__ = "File named rs_veg_europe_disturbance_none_ann_1985_2023_v1_efda.nc, at ~50m resolution, annual for 1985-2023, with data for undisturbed (0) or disturbed (1) by wind and/or bark beetle complex in the cell"

import xarray as xr
import rioxarray as rxr
import sys
import os
import glob
import gc

# European Forest Disturbance Atlas (Version 2.1.1.) data for disturbance agents yearly
path = "/gws/pw/j07/leicester/OPTFOREU/EFMI_EFDA/agents_v211"
# Path to save yearly processed files
out_dir = "/gws/pw/j07/leicester/OPTFOREU/EFMI_EFDA/tmp_binary"
os.makedirs(out_dir, exist_ok=True)

years = [str(y) for y in range(1985, 2024)]

# Process each year to avoid running into memory limitations
for year in years:

    matches = glob.glob(f"{path}/{year}*.tif")

    if len(matches) == 0:
        print(f"No file found for {year}, skipping.")
        continue

    if len(matches) > 1:
        print(f"Warning: multiple files found for {year}, using first: {matches[0]}")

    infile = matches[0]

    outfile = f"{out_dir}/{year}.nc"

    da = rxr.open_rasterio(infile[0]).squeeze()
    # Reproject from EPSG 3035 to 4326
    da = da.rio.reproject("EPSG:4326")
    # Make data binary, where 1 is disburtance by Wind and/or Bark Beetle and the rest is 0 (original data has other disturbances such as fire (2), harvest (3) and mixed agents (4, where more than one agent occurred))
    da = (da == 1).astype("uint8")
    da = da.rename("disturbance")
    da = da.assign_coords(year=year).expand_dims("year")

    da.to_netcdf(outfile)
    
    del da
    gc.collect()

    print(f'Processed {year}')

# Combine all years
da_eur_flname_output = 'rs_veg_europe_disturbance_none_ann_1985_2023_v1_efda.nc'

files = sorted(glob.glob('/gws/pw/j07/leicester/OPTFOREU/EFMI_EFDA/tmp_binary/*.nc'))
ds = xr.open_mfdataset(files, combine="nested", concat_dim="year")

# rename coordinates for clarity
ds = ds.rename({"y": "lat", "x": "lon"})
ds = ds.drop_vars(["spatial_ref", "band"])
ds = ds.rename({"disturbance": "Wind & Bark Beetle Disturbance"})

ds.attrs['Filename'] = da_eur_flname_output
ds.attrs['Variables'] = 'Wind & Bark Beetle Disturbance'
ds.attrs['Units'] = 'unitless (presence (1) or absence (0))'
ds.attrs['Data_source'] = 'European Forest Disturbance Atlas (Version 2.1.1.)'
ds.attrs['Time_period'] = '1985-2023'
ds.attrs['Time_averaging'] = 'Annual'
ds.attrs['Spatial_extent'] = 'Europe'
ds.attrs['Coordinate_system'] = 'EPSG:4326'
ds.attrs['Author_names'] = 'Dr. Rocio Barrio Guillo, Dr. Jasdeep S. Anand'

# Compress to upload and use with more ease
encoding = {
    "Wind & Bark Beetle Disturbance": {
        "zlib": True,
        "complevel": 4,
        "dtype": "int8",
        "chunksizes": (1, 500, 500)
    }
}

# Save final product
ds.to_netcdf(
    f'/gws/pw/j07/leicester/OPTFOREU/EFMI_EFDA/{da_eur_flname_output}',
    encoding=encoding
)
