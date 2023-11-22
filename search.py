"""
This module provide search functionality for a single instance or for a bulk search operation via csv file.
Author: Muhammad Salah
Email: msalah.29.10@gmail.com
"""

from argparse import Namespace
from api_types import *
from download import download, download_csv_gportal, download_csv_jasmes
from gportal import GportalApi
import pandas as pd
import numpy as np
from tqdm import tqdm
from gportal import GPortalLvlProd

from gportal import GPortalResolution
from jasmes import JasmesApi
from jasmes import JASMESProd

"""
Utility function to get the value from a dict and validate it
"""
def get_value(d: dict, key: str):
    """
    Utility function to get the value from a dict and validate it
    """
    if key in d and d[key]:
        return d[key]
    
def fill_group(df, g):
    for j in range(len(g)):
        df.loc[df.index[g.index[j]], "identifier"] = g.iloc[0]["identifier"]
        df.loc[df.index[g.index[j]], "file_status"] = g.iloc[0]["file_status"]
        df.loc[df.index[g.index[j]], "resolution"] = g.iloc[0]["resolution"]
        df.loc[df.index[g.index[j]], "path_number"] = g.iloc[0]["path_number"]
        df.loc[df.index[g.index[j]], "scene_number"] = g.iloc[0]["scene_number"]
        df.loc[df.index[g.index[j]], "download_url"] = g.iloc[0]["download_url"]
        df.loc[df.index[g.index[j]], "preview_url"] = g.iloc[0]["preview_url"]
        df.loc[df.index[g.index[j]], "cloud_coverage"] = g.iloc[0]["cloud_coverage"]


def search(args: Namespace):
    """
    Search a single instance and print the result to the terminal
    arguments provided through json file or cmdline arguments:
        - api: GPORTAL or JASMES, default: GPORTAL
        - level_product: L1B, L2R, or L2P
        - date: string date
        - latitude
        - longitude
        - resolution: str(250m or 1km) or int(250 or 1000)
        - path_number: optional
        - scene_number: optional
    """
    # selecting which API
    if args.api == SGLIAPIs.GPORTAL:
        pl = GPortalLvlProd(args.level_product)
        api = GportalApi(pl)
        # send search request
        result = api.search(args.date, args.latitude, args.longitude,
                        args.resolution, args.path_number, args.scene_number)
    elif args.api == SGLIAPIs.JASMES:
        pl = JASMESProd(args.level_product)
        api = JasmesApi(pl)
        # send search request
        api.set_auth_details(args.cred)
        result = api.search(args.date, args.latitude, args.longitude)
    else: 
        print("API name is not recognized")
        exit(1)

    
    
    # print results
    print("returned results: ")
    result.print()

    # if download option is set set the download url and call the download function
    if args.download:
        if args.api == SGLIAPIs.GPORTAL:
            setattr(args, "download_url", result.properties.product.downloadUrl.geturl())
        elif args.api == SGLIAPIs.JASMES:
            setattr(args, "ftp_path", result.filePath)
        download(args)


def search_csv_gportal(args: Namespace):
    """
    Bulk search operation using csv file
    arguments provided through json file or cmdline arguments:
        - api: GPORTAL or JASMES, default: GPORTAL
        - level_product: L1B, L2R, or L2P
        - csv: path to csv file
        - no_repeat: boolean, if identifier exists will not search the corresponding row
    CSV file columns:
        - date
        - lat
        - lon
        - path_number: optional (will be used instead of lat and lon)
        - scene_number: optional (will be used instead of lat and lon)
        - resolution: optional (defaults to 250m)
        - identifier: optional (if no_repeat set and identifier provided the corresponding row will be skipped)

    Output columns:
        - identifier
        - file_status
        - resolution
        - path_number
        - scene_number
        - download_url
        - preview_url
        - cloud_coverage (%)
    """
    pl = GPortalLvlProd(args.level_product)
    api = GportalApi(pl)

    print("=============================")
    print("Searching CSV...")
    print("=============================")

    df = pd.read_csv(args.csv) # read csv
    pbar = tqdm(total=len(df), position=0, leave=True) # prepare progress bar

    for i in range(len(df)):
        row = df.iloc[i].fillna(0).to_dict() # convert current row to dict

        # read search parameters from current row
        date, lat, lon = get_value(row, "date"), get_value(row, "lat"), get_value(row, "lon")
        path_number, scene_number = get_value(row, "path_number"), get_value(row, "scene_number")
        resolution = get_value(row, "resolution")
        id = get_value(row, "identifier")

        # selecting resolution
        if resolution: resolution = GPortalResolution.from_int(int(resolution))
        else: resolution = GPortalResolution.H

        # progress if no repeat and id exists
        if id and args.no_repeat: 
            pbar.update(1)
            continue

        # send search request 
        result = api.search(date, lat, lon, resolution, path_number, scene_number, verbose=False)
        # if results returned add to the data
        if result != None:
            result.to_dataframe(df, i)

        pbar.update(1) # update progress bar

        # save to csv every 100 row
        if (i % 100 == 0): df.to_csv(args.csv, index=False)

    df.to_csv(args.csv, index=False) # save to csv
    pbar.close()

    # move to download option if download is set
    if args.download:
        download_csv_gportal(args)

def search_csv_grouped_gportal(args: Namespace):
    """
    Bulk search operation using csv file
    arguments provided through json file or cmdline arguments:
        - api: GPORTAL or JASMES, default: GPORTAL
        - level_product: L1B, L2R, or L2P
        - csv: path to csv file
        - no_repeat: boolean, if identifier exists will not search the corresponding row
    CSV file columns:
        - date
        - lat
        - lon
        - identifier: optional (if no_repeat set and identifier provided the corresponding row will be skipped)

    Output columns:
        - identifier
        - file_status
        - resolution
        - path_number
        - scene_number
        - download_url
        - preview_url
        - cloud_coverage (%)
    """
    pl = GPortalLvlProd(args.level_product)
    api = GportalApi(pl)

    print("=============================")
    print("Searching CSV (grouped)...")
    print("=============================")

    df = pd.read_csv(args.csv) # read csv
    grouped = df.groupby(["lat", "lon", "date"])
    pbar = tqdm(total=len(df), position=0, leave=True) # prepare progress bar

    for i, ((lat, lon, date), g) in enumerate(grouped):
    
        id = get_value(g.iloc[0].fillna(0).to_dict(), "identifier")
        resolution = GPortalResolution.H

        # progress if no repeat and id exists
        if id and args.no_repeat: 
            fill_group(df, g)
            pbar.update(len(g))
            continue

        # send search request 
        result = api.search(date, lat, lon, resolution, None, None, verbose=False)
        # if results returned add to the data
        if result != None:
            for j in range(len(g)):
                result.to_dataframe(df, g.index[j])

        pbar.update(len(g)) # update progress bar

        # save to csv every 100 row
        if (i % 100 == 0): df.to_csv(args.csv, index=False)

    df.to_csv(args.csv, index=False) # save to csv
    pbar.close()

    # move to download option if download is set
    if args.download:
        download_csv_gportal(args)
        

def search_csv_jasmes(args: Namespace):
    """
    Bulk search operation using csv file for JASMES API
    arguments provided through json file or cmdline arguments:
        - level_product: NWLR_380, NWLR_412, NWLR_443, NWLR_490, NWLR_530, NWLR_565, NWLR_670, PAR, TAUA_670, TAUA_865, FAI, CDOM, CHLA, TSM, SST, Cloud_probability
        - csv: path to csv file
        - no_repeat: boolean, if identifier exists will not search the corresponding row
    CSV file columns:
        - date
        - lat
        - lon
        - file_name: optional (if no_repeat set and filename provided the corresponding row will be skipped)

    Output columns:
        - file_name
        - file_path
        - file_size
        - box_id
    """
    pl = JASMESProd(args.level_product)
    api = JasmesApi(pl)
    api.set_auth_details(args.cred)
    print("=============================")
    print("Searching CSV...")
    print("=============================")

    df = pd.read_csv(args.csv) # read csv
    grouped = df.groupby(["lat", "lon", "date"])
    pbar = tqdm(total=len(df), position=0, leave=True) # prepare progress bar

    for i, ((lat, lon, date), g) in enumerate(grouped):
    
        fn = get_value(g.iloc[0].fillna(0).to_dict(), "file_name")

        # progress if no repeat and id exists
        if fn and args.no_repeat: 
            fill_group(df, g)
            pbar.update(len(g))
            continue

        # send search request 
        result = api.search(date, lat, lon, verbose=False)
        # if results returned add to the data
        if result != None:
            for j in range(len(g)):
                result.to_dataframe(df, g.index[j])

        pbar.update(len(g)) # update progress bar

        # save to csv every 100 row
        if (i % 100 == 0): df.to_csv(args.csv, index=False)

    df.to_csv(args.csv, index=False) # save to csv
    pbar.close()

    # move to download option if download is set
    if args.download:
        download_csv_jasmes(args)