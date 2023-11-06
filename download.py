from argparse import Namespace

from api_types import SGLIAPIs
from gportal.gportal_api import GportalApi
import pandas as pd


def download(args: Namespace):
    # selecting which API
    if args.api == SGLIAPIs.GPORTAL:
        api = GportalApi(args.level_product)
    else:
        print("to be implemented")
        exit(1)

    if args.download_url == None: 
        print("download_url must be set!")
        exit(1)

    download_url = str(args.download_url)    
    api.set_auth_details(args.account, args.password)
    api.download(download_url, args.download_dir)

def download_csv(args: Namespace):
    # selecting which API
    if args.api == SGLIAPIs.GPORTAL:
        api = GportalApi(args.level_product)
    else:
        print("to be implemented")
        exit(1)
    
    api.set_auth_details(args.account, args.password)

    df = pd.read_csv(args.csv) # read csv
    df =df.groupby("download_url")

    for i, (url, _) in enumerate(df):
        print("==========>",i+1, "out of", len(df))
        api.download(url, args.download_dir)
