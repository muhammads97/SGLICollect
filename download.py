"""
This module provide search functionality for a single instance or for a bulk download operation via csv file.
Author: Muhammad Salah
Email: msalah.29.10@gmail.com
"""

from argparse import Namespace

from api_types import SGLIAPIs
from extract import extract, extract_csv
from gportal import GPortalLvlProd, GportalApi
import pandas as pd

from jasmes import JasmesApi, JASMESProd


def download(args: Namespace):
    """
    Download a single product into a specified download directory
    arguments provided through json file or cmdline arguments:
        - api: GPORTAL or JASMES, default: GPORTAL
        - level_product: L1B, L2R, or L2P
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
        pl = GPortalLvlProd(args.level_product)
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
        pl = JASMESProd(args.level_product)
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




def download_csv_gportal(args: Namespace):
    """
    Bulk download operation using csv file for GPORTAL
    arguments provided through json file or cmdline arguments:
        - level_product: L1B, L2R, or L2P
        - download_url: url of the product
        - download_dir: directory to download the file
        - cred: path to json file containing account and password
        |       Example:
        |       {
        |           "account": "<YOUR_USERNAME>",
        |           "password": "<YOUR_PASSWORD>"
        |       }
    CSV file columns:
        - download_url
    """
    pl = GPortalLvlProd(args.level_product)
    api = GportalApi(pl)
    
    print("=============================")
    print("Downloading files...")
    print("=============================")
    # supply the API with the auth credentials  
    # this is only needed for download not search
    api.set_auth_details(args.cred)

    df = pd.read_csv(args.csv) # read csv
    df =df.groupby("download_url") # only download uniqe urls

    for i, (url, _) in enumerate(df):
        print(f"> {i+1}/{len(df)}", end=": ") # progress indicator 
        # start the download of the i's url
        api.download(url, args.download_dir)

    
    if args.extract:
        setattr(args, "product_dir", args.download_dir)
        extract_csv(args)

def download_csv_jasmes(args: Namespace):
    """
    Bulk download operation using csv file for JASMES
    arguments provided through json file or cmdline arguments:
        - level_product: NWLR_380, NWLR_412, NWLR_443, NWLR_490, NWLR_530, NWLR_565, NWLR_670, PAR, TAUA_670, TAUA_865, FAI, CDOM, CHLA, TSM, SST, Cloud_probability
        - csv: path to csv file
        - download_dir: directory to download the file
        - cred: path to json file containing account and password
        |       Example:
        |       {
        |           "account": "<YOUR_USERNAME>",
        |           "password": "<YOUR_PASSWORD>"
        |       }
    CSV file columns:
        - ftp_path
    """
    
    print("=============================")
    print("Downloading files...")
    print("=============================")
    pl = JASMESProd(args.level_product)
    api = JasmesApi(pl)
    # supply the API with the auth credentials  
    api.set_auth_details(args.cred)

    df = pd.read_csv(args.csv) # read csv
    df =df.groupby("ftp_path") # only download uniqe urls

    for i, (ftp_path, _) in enumerate(df):
        print(f"> {i+1}/{len(df)}", end=": ") # progress indicator 
        # start the download of the i's url
        api.download(ftp_path, args.download_dir)

    
    if args.extract:
        setattr(args, "product_dir", args.download_dir)
        extract_csv(args)

    
