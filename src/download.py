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

from src.api_types import SGLIAPIs
from src.gportal import GPortalLvlProd, GportalApi
from src.jasmes import JasmesApi, JASMESProd
from src.extract import extract, extract_csv
import pandas as pd
from sys import exit

def download(args: Namespace):
    """
    Download a single product into a specified download directory
    arguments provided through json file or cmdline arguments:
        - api: GPORTAL or JASMES, default: GPORTAL
        - - product: GPortal Products or Jasmes Products
        - download_url: url of the product
        - download_dir: directory to download the file
        - cred: path to json file containing account and password
        |       Example:
        |       {
        |           "account": "<YOUR_USERNAME>",
        |           "password": "<YOUR_PASSWORD>"
        |       }
        
    """
    # selecting which API
    if args.api == SGLIAPIs.GPORTAL:
        pl = GPortalLvlProd(args.product)
        api = GportalApi(pl)
        # for single file download the url must be provided directly on arguments
        if args.download_url == None: 
            print("download_url must be set!")
            exit(1)
        download_url = str(args.download_url)
        # supply the API with the auth credentials  
        # this is only needed for download not search
        api.set_auth_details(args.cred)
        # start the download process
        product_path = api.download(download_url, args.download_dir)
    elif args.api == SGLIAPIs.JASMES:
        pl = JASMESProd(args.product)
        api = JasmesApi(pl)
        # for single file download the url must be provided directly on arguments
        if args.ftp_path == None: 
            print("ftp_path must be set!")
            exit(1)
        ftp_path = str(args.ftp_path)
        # supply the API with the auth credentials  
        api.set_auth_details(args.cred)
        # start the download process
        product_path = api.download(ftp_path, args.download_dir)
    else:
        print("API name is not recognized")
        exit(1)

    if args.extract:
        setattr(args, "product_path", product_path)
        extract(args)




def download_csv(args: Namespace):
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
        pl = JASMESProd(args.product)
        api = JasmesApi(pl)
        group_key = "ftp_path"
    
    print("=============================")
    print("Downloading files...")
    print("=============================")
    # supply the API with the auth credentials  
    # this is only needed for download not search
    api.set_auth_details(args.cred)

    df = pd.read_csv(args.csv) # read csv
    df =df.groupby(group_key) # only download uniqe urls

    for i, (url, _) in enumerate(df):
        print(f"> {i+1}/{len(df)}", end=": ") # progress indicator 
        # start the download of the i's url
        api.download(url, args.download_dir)

    if args.extract:
        setattr(args, "product_dir", args.download_dir)
        extract_csv(args)
