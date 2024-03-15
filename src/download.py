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
from src.jasmes.jasmes_collector import JasmesCollector
from src.api_types import SGLIAPIs
from src.gportal import GPortalLvlProd, GportalApi
from src.extract import extract

def download(args: Namespace):
    """
    Bulk download operation using csv file for GPORTAL
    arguments provided through json file or cmdline arguments:
        - product: GPortal Products or Jasmes Products
        - download_dir: directory to download the file
        - cred: path to json file containing account and password
        |       Example:
        |       {
        |           "account": "<YOUR_USERNAME>",
        |           "password": "<YOUR_PASSWORD>"
        |       }
    CSV file columns:
        - download_url/ftp_path
    """
    if args.api == SGLIAPIs.GPORTAL:
        pl = GPortalLvlProd(args.product)
        api = GportalApi(pl)
        group_key = "download_url"
    elif args.api == SGLIAPIs.JASMES:
        api = JasmesCollector()
        group_key = "ftp_path_NWLR_380"
    
    print("=============================")
    print("Downloading files...")
    print("=============================")
    # supply the API with the auth credentials  
    # this is only needed for download not search
    api.set_auth_details(args.cred)

    df = pd.read_csv(args.csv, low_memory=True) # read csv
    df =df.groupby(group_key) # only download uniqe urls

    for i, (url, g) in enumerate(df):
        print(f"> {i+1}/{len(df)}", end=": \n") # progress indicator 
        if args.api == SGLIAPIs.JASMES:
            row = g.iloc[0].to_dict()
            paths = {}
            for k in row.keys():
                if k.startswith("ftp_path"):
                    paths[k] = row[k]
            api.download(paths, args.download_dir)
        else:
            # start the download of the i's url
            api.download(url, args.download_dir)

    if args.extract:
        setattr(args, "product_dir", args.download_dir)
        extract(args)
