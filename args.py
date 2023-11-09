"""
This module provide arguments of this API
Author: Muhammad Salah
Email: msalah.29.10@gmail.com
"""
import argparse
from pathlib import Path
import json
from api_types import *
from gportal import GPortalLvlProd, GPortalResolution

parser = argparse.ArgumentParser(description="Welcome to SGLI-API!\n"
                                             "This API is developed for searching and downloading SGLI Images.\n" 
                                             "This API is developed by Muhammad Salah (msalah.29.10@gmail.com)\n",
                                formatter_class=argparse.RawTextHelpFormatter
                                )
parser.add_argument('-s', '--search', action="store_true", help='Search GPortal for products')
parser.add_argument('-d', '--download', action="store_true", help='Download the products')
parser.add_argument('-e', "--extract", action="store_true", help="extract the pixel matching the lat, and long from the product")

parser.add_argument("--date", nargs="?",
                    help="sample date format: yyyy/mm/dd", type=str)
parser.add_argument('-lp', "--level-product", nargs="?",
                    help="'L1B' for level 1, 'L2R' for level 2 NWLR (Rrs), or 'L2P' for level 2 IWLR (Chla, etc)",
                    type=GPortalLvlProd, default=GPortalLvlProd.L1B)
parser.add_argument('-lat', "--latitude", nargs="?",
                    help="Latitude", type=float)
parser.add_argument('-lon', "--longitude", nargs="?",
                    help="Longitude", type=float)
parser.add_argument('-pn', "--path-number", nargs="?",
                    type=int, help="Satellite path number from 0 to 485")
parser.add_argument('-sn', "--scene-number", nargs="?",
                    type=int, help="satellite scene number from 0 to 99")
parser.add_argument('-r', "--resolution", nargs="?", type=GPortalResolution,
                    default=GPortalResolution.H, help="resolution (250m or 1000m)")
parser.add_argument('--api', nargs="?", type=SGLIAPIs, default=SGLIAPIs.GPORTAL,
                    help="API: GPORTAL or JASMES (Not implemented yet)")
parser.add_argument('-c', "--config-file", type=Path,
                    help="provide the arguments in a json file")
parser.add_argument('--csv', nargs="?", type=Path,
                    help="a path to a json file containing the search results")
parser.add_argument("--no-repeat", action="store_true", help="don't repeat if identifier exists")
parser.add_argument("--cred", type=Path, help="a path to json file containing account and password\nexample: \n{\n\t\"account\": \"<YOUR_USERNAME>\", \n\t\"password\": \"<YOUR_PASSOWRD>\"\n}")
parser.add_argument("--download-dir", type=Path, default=Path("./temp"), help="directory path of the download location")
parser.add_argument("--download-url", type=str, help="url of product to download")
parser.add_argument("--product-path", type=Path, help="product path for extract option")
parser.add_argument("--product-dir", type=Path, help="directory containing products to extract")
parser.add_argument("--group", action="store_true", help="Only works with lat and lon searchs, it will group duplicated lat, lon, and date")
args = parser.parse_args()

if args.config_file:
    f = open(args.config_file)
    config = json.load(f)
    f.close()
    for o in config["operations"]:
        setattr(args, o, True)
    for k in config["args"].keys():
        if not isinstance(getattr(args, k), type(None)):
            setattr(args, k, type(getattr(args, k))(config["args"][k]))
        else:
            setattr(args, k, config["args"][k])

if args.api == SGLIAPIs.JASMES:
    print("JASMES API is still under construction.")
    exit(1)

if args.search:
    if not args.csv:
        if args.date == None:
            print("date must be provided")
            exit(1)
        if args.latitude == None or args.longitude == None:
            print("latitude and longitude must be provided")
            exit(1)
if args.download:
    if args.cred == None: 
        print("credentials must be provided via a json file")
        exit(1)
if args.extract:
    if not args.csv:
        if args.latitude == None or args.longitude == None:
            print("latitude and longitude must be provided")
            exit(1)   
if not args.search and not args.download and not args.extract:
    print("No option provided!")
    parser.print_help()
    exit(1)
