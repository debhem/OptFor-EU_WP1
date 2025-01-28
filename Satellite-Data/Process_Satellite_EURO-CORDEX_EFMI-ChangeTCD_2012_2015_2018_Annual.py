__author__ = "Dr. Jasdeep S. Anand, Dr. Rocio Barrio Guillo"
__credits__ = ["Dr. Jasdeep S. Anand", "Dr. Rocio Barrio Guillo", "Dr. Darren Ghent", ]
__other_citations__ = "Generated using European Union's Copernicus Land Monitoring Service information; https://doi.org/10.2909/299ad2d6-f2b8-4716-b169-1d621250fc3c, https://doi.org/10.2909/264d4e20-de6d-4f88-b1be-b592303452af, https://doi.org/10.2909/c7bf34ea-755c-4dbd-85b6-4efc5fd302a2"
__version__ = "1"
__description__ = "Produces EFMI #8 Changes in Tree Cover Density. Resamples spatial resolution and subsets to the EURO CORDEX region domain"
__inputs__ = "Sentinel-2 Copernicus High-Resolution Layer Tree Cover Density dataset, at 100m resolution, annually for 2012, 2015 and 2018, with units %"
__outputs__ = "Files named rs_veg_europe_changeTCD_none_ann_2015_v1_clms.tif and rs_veg_europe_changeTCD_none_ann_2018_v1_clms.tif, at 1km resolution, annually for 2015 and 2018 with respect to 2012, with units %"

from pathlib import Path
from hda import Client, Configuration
import glob
import os
import requests
import zipfile
import rasterio
import geopandas as gpd
import numpy as np
from IPython import embed

from pyproj import Transformer
from rasterio.enums import Resampling
from rasterio.warp import calculate_default_transform, reproject, transform_bounds
from rasterio.mask import mask
from shapely.geometry import box
from rasterio.io import MemoryFile

def read_clip_resample_raster(tcd_dir, year, bounding_box, scale_factor):

    if year != '2018':
        tcd_this_yr = glob.glob(f'{tcd_dir}/TCD_{year}/*/*.tif')
    else:
        tcd_this_yr = glob.glob(f'{tcd_dir}/TCD_{year}/*/*/*.tif')

    with rasterio.open(tcd_this_yr[0]) as src:

        tcd_data_og = src.read(1)

        profile = src.profile
        transform = src.transform
        crs = src.crs

        bbox_projected = transform_bounds("EPSG:4326", src.crs, *bounding_box)
        bbox_geom = box(*bbox_projected)
        #bbox_gdf = gpd.GeoDataFrame({"geometry": [bbox_geom]}, crs=src.crs)

        tcd_data_og_m = np.where((tcd_data_og == 255) | (tcd_data_og == 254), np.nan, tcd_data_og)

        # Resample the raster to 1km resolution (scale factor = 1000m / 100m = 10)
        new_width = int(src.width / scale_factor)
        new_height = int(src.height / scale_factor)
        new_transform = src.transform * src.transform.scale(scale_factor, scale_factor)
        resampled_data = np.empty((new_height, new_width), dtype=np.float32)

        reproject(
            source=tcd_data_og_m,
            destination=resampled_data,
            src_transform=transform,
            src_crs=crs,
            dst_transform=new_transform,
            dst_crs=crs,
            resampling=Resampling.nearest, # nearest method keeps values within original 0-100%
        )

        # Update profile for resampled raster
        profile.update({
            "height": new_height,
            "width": new_width,
            "transform": new_transform,
            "dtype": 'float32',
            "nodata": np.nan,
        })

        # Clip to bounding box
        with MemoryFile() as memfile:
            with memfile.open(**profile) as mem:
                # Write the resampled raster to the in-memory dataset
                mem.write(resampled_data, 1)

                # Perform the clipping on the resampled data
                clipped_data, clipped_transform = mask(
                    dataset=mem,
                    shapes=[bbox_geom],
                    crop=True,
                    nodata=np.nan
                )

        # Update profile for clipped raster
        profile.update({
            "height": clipped_data.shape[1],
            "width": clipped_data.shape[2],
            "transform": clipped_transform,
        })

        resampled_tcd_data_og_m = clipped_data[0,:,:]

        return resampled_tcd_data_og_m, profile, tcd_data_og

# Local paths to directories where data has been downloaded to
out_top_dir = '/data/atsr/OptForEU'
tcd_dir = f'{out_top_dir}/CLMS_TCD'
os.makedirs(tcd_dir, exist_ok=True)
# Local path to directory for output data
out_tcd_dir = f'{tcd_dir}/Europe/input/remote_sensing/vegetation/'
if not os.path.exists(out_tcd_dir):
    os.makedirs(out_tcd_dir)

# EURO-CORDEX Domain
eur_min_lon = -44.75
eur_max_lon = 65.25
eur_min_lat = 21.75
eur_max_lat = 72.75

bounding_box = [eur_min_lon, eur_min_lat, eur_max_lon, eur_max_lat]

# Desired resolution (1km) and current 100m
factor = 10

tcd_data_2012, metadata, tcd_2012_og = read_clip_resample_raster(tcd_dir, '2012', bounding_box, factor)
tcd_data_2015, metadata, tcd_2015_og = read_clip_resample_raster(tcd_dir, '2015', bounding_box, factor)
tcd_data_2018, metadata, tcd_2018_og = read_clip_resample_raster(tcd_dir, '2018', bounding_box, factor)

# Subtract to get change in tree cover density from 2012
# If 0 it stayed the same, if >0 higher density in 2015, if <0 higher density in 2012
change_2012_2015 = tcd_data_2015 - tcd_data_2012
change_2012_2018 = tcd_data_2018 - tcd_data_2012

# Filename for 2015 output
output_raster_nm_15 = f"{out_tcd_dir}rs_veg_europe_changeTCD_none_ann_2015_v1_clms.tif"
# Save as raster file
with rasterio.open(
    output_raster_nm_15,
    'w',
    height=metadata['height'],
    width=metadata['width'],
    count=1,
    dtype=metadata['dtype'],
    crs=metadata['crs'],
    transform=metadata['transform'],
    nodata=metadata['nodata'],
) as dst:
    dst.write(change_2012_2015.astype(rasterio.float32), 1)
    # Add custom metadata using tags (stored as string tags)
    dst.update_tags(
        1,  # The band number to associate the tags with (1 for the first band)
        filename='rs_veg_europe_changeTCD_none_ann_2015_v1_clms.tif',
        variables='% change in tree cover density from 2012',
        units='%',
        data_source='Sentinel-2 Copernicus High-Resolution Layer Tree Cover Density dataset',
        time_period='2015',
        time_averaging='Annual',
        spatial_extent='Europe',
        coordinate_system='EPSG:4326',
        author_names='Dr. Rocio Barrio Guillo, Dr. Jasdeep S. Anand'
    )

# Filename for 2018 output
output_raster_nm_18 = f"{out_tcd_dir}rs_veg_europe_changeTCD_none_ann_2018_v1_clms.tif"
# Save as raster file
with rasterio.open(
    output_raster_nm_18,
    'w',
    height=metadata['height'],
    width=metadata['width'],
    count=1,
    dtype=metadata['dtype'],
    crs=metadata['crs'],
    transform=metadata['transform'],
    nodata=metadata['nodata'],
) as dst:
    dst.write(change_2012_2018.astype(rasterio.float32), 1)
    # Add custom metadata using tags (stored as string tags)
    dst.update_tags(
        1,  # The band number to associate the tags with (1 for the first band)
        filename='rs_veg_europe_changeTCD_none_ann_2018_v1_clms.tif',
        variables='% change in tree cover density from 2012',
        units='%',
        data_source='Sentinel-2 Copernicus High-Resolution Layer Tree Cover Density dataset',
        time_period='2018',
        time_averaging='Annual',
        spatial_extent='Europe',
        coordinate_system='EPSG:4326',
        author_names='Dr. Rocio Barrio Guillo, Dr. Jasdeep S. Anand'
    )
