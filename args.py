import argparse
import datetime
from pathlib import Path
import json
from api_types import *
from gportal import GPortalLvlProd, GPortalResolution
from pathlib import Path
import os

intro = open("./help/intro.txt")
parser = argparse.ArgumentParser(description=intro.read())
intro.close()
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
parser.add_argument("--use-orbit", action="store_true", help="use the satellite path number and scene number instead of lat and long")
parser.add_argument("--no-repeat", action="store_true", help="don't repeat if identifier exists")
args = parser.parse_args()

if args.config_file:
    f = open(args.config_file)
    config = json.load(f)
    f.close()
    setattr(args, config["operation"], True)
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

elif args.search_csv:
    print("search_csv")
elif args.download:
    print("download")
elif args.download_csv:
    print("download_csv")
else:
    print("No option provided!")
    parser.print_help()
    exit(1)
