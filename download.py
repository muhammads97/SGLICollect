"""
This module provide search functionality for a single instance or for a bulk download operation via csv file.
Author: Muhammad Salah
Email: msalah.29.10@gmail.com
"""

from argparse import Namespace

from api_types import SGLIAPIs
from gportal.gportal_api import GportalApi
import pandas as pd


def download(args: Namespace):
    """
    Download a single product into a specified download directory
    arguments provided through json file or cmdline arguments:
        - api: GPORTAL or JASMES, default: GPORTAL
        - level_product: L1B, L2R, or L2P
        - download_url: url of the product
        - account: user account on GPORTAL
        - password: GPORTAL password
        - download_dir: directory to download the file
    """
    # selecting which API
    if args.api == SGLIAPIs.GPORTAL:
        api = GportalApi(args.level_product)
    else:
        print("to be implemented")
        exit(1)

    # for single file download the url must be provided directly on arguments
    if args.download_url == None: 
        print("download_url must be set!")
        exit(1)
    download_url = str(args.download_url)  

    # supply the API with the auth credentials  
    # this is only needed for download not search
    api.set_auth_details(args.account, args.password)
    # start the download process
    api.download(download_url, args.download_dir)



def download_csv(args: Namespace):
    """
    Bulk download operation using csv file
    arguments provided through json file or cmdline arguments:
        - api: GPORTAL or JASMES, default: GPORTAL
        - level_product: L1B, L2R, or L2P
        - csv: path to csv file
        - account: user account on GPORTAL
        - password: GPORTAL password
        - download_dir: directory to download the file
    CSV file columns:
        - download_url
    """
    # selecting which API
    if args.api == SGLIAPIs.GPORTAL:
        api = GportalApi(args.level_product)
    else:
        print("to be implemented")
        exit(1)
    
    # supply the API with the auth credentials  
    # this is only needed for download not search
    api.set_auth_details(args.account, args.password)

    df = pd.read_csv(args.csv) # read csv
    df =df.groupby("download_url") # only download uniqe urls

    for i, (url, _) in enumerate(df):
        print("==========>",i+1, "out of", len(df)) # progress indicator 
        # start the download of the i's url
        api.download(url, args.download_dir)
