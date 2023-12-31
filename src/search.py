#
# Copyright (c) 2023 Muhammad Salah msalah.29.10@gmail.com
# Licensed under AGPL-3.0-or-later.
# Refer to COPYING.txt for the AGPL license.
# All rights reserved.
# This project is developed as part of my research in the Remote Sensing Laboratory
# in Kyoto University of Advanced Science towards my Master's Degree course.
# The research was mainly supervised by Professor Salem Ibrahim Salem.
#


from argparse import Namespace
import pandas as pd
import numpy as np
from tqdm import tqdm
from src import download, download_csv
from src.jasmes import JASMESProd
from src.api_types import SGLIAPIs
from src.gportal import GportalApi, GPortalLvlProd, GPortalResolution
from src.jasmes import JasmesApi
from sys import exit

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
        df.loc[df.index[g.index[j]], "download_url"] = g.iloc[0]["download_url"]
        df.loc[df.index[g.index[j]], "preview_url"] = g.iloc[0]["preview_url"]
        df.loc[df.index[g.index[j]], "cloud_coverage"] = g.iloc[0]["cloud_coverage"]


def search(args: Namespace):
    """
    Search a single instance and print the result to the terminal
    arguments provided through json file or cmdline arguments:
        - api: GPORTAL or JASMES, default: GPORTAL
        - product: GPortal Products or Jasmes Products
        - date: string date
        - latitude
        - longitude
        - resolution: str(250m or 1km) or int(250 or 1000)
    """
    # selecting which API
    if args.api == SGLIAPIs.GPORTAL:
        pl = GPortalLvlProd(args.product)
        api = GportalApi(pl)
        # send search request
        resolution = GPortalResolution.from_str(args.resolution)
        result = api.search(args.date, args.latitude, args.longitude, resolution)
        setattr(args, "download_url", result.properties.product.downloadUrl.geturl())
    elif args.api == SGLIAPIs.JASMES:
        pl = JASMESProd(args.product)
        api = JasmesApi(pl)
        # send search request
        api.set_auth_details(args.cred)
        result = api.search(args.date, args.latitude, args.longitude, None)
        setattr(args, "ftp_path", result.filePath)
    else: 
        print("API name is not recognized")
        exit(1)

    # print results
    print("returned results: ")
    result.print()

    # if download option is set, call the download function
    if args.download:
        download(args)

def search_csv(args: Namespace):
    """
    Bulk search operation using csv file
    arguments provided through json file or cmdline arguments:
        - api: GPORTAL or JASMES, default: GPORTAL
        - product: GPortal Products or Jasmes Products
        - csv: path to csv file
        - no_repeat: boolean, if identifier exists will not search the corresponding row
    CSV file columns:
        - date
        - lat
        - lon
        - identifier/file_name: optional (if no_repeat set and identifier/file_name provided the corresponding row will be skipped)

    Output columns for GPORTAL:
        - identifier
        - file_status
        - resolution
        - download_url
        - preview_url
        - cloud_coverage (%)
    Output columns for JASMES:
        - ftp_path
        - file_name
        - file_size
        - box_id
    """
    if args.api == SGLIAPIs.GPORTAL:
        pl = GPortalLvlProd(args.product)
        api = GportalApi(pl)
        id_key = "identifier"
    elif args.api == SGLIAPIs.JASMES:
        pl = JASMESProd(args.product)
        api = JasmesApi(pl)
        api.set_auth_details(args.cred)
        id_key = "file_name"

    print("=============================")
    print("Searching CSV ...")
    print("=============================")

    df = pd.read_csv(args.csv) # read csv
    grouped = df.groupby(["lat", "lon", "date"])
    pbar = tqdm(total=len(df), position=0, leave=True) # prepare progress bar

    for i, ((lat, lon, date), g) in enumerate(grouped):
    
        id = get_value(g.iloc[0].fillna(0).to_dict(), id_key)
        resolution = GPortalResolution.H

        # progress if no repeat and id exists
        if id and args.no_repeat: 
            fill_group(df, g)
            pbar.update(len(g))
            continue

        # send search request 
        result = api.search(date, lat, lon, resolution, verbose=False)
        # if results returned add to the data
        if result != None:
            for j in range(len(g)):
                result.to_dataframe(df, g.index[j])

        pbar.update(len(g)) # update progress bar

        # save to csv every 100 row
        if (i % 100 == 0): df.to_csv(args.csv, index=False)

    for c in df.columns:
        if c.startswith("Unnamed"):
            df.drop(columns=c, inplace=True)
    df.to_csv(args.csv, index=False) # save to csv
    pbar.close()

    # move to download option if download is set
    if args.download:
        download_csv(args)
        

