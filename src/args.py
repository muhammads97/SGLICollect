#
# Copyright (c) 2023 Muhammad Salah msalah.29.10@gmail.com
# Licensed under AGPL-3.0-or-later.
# Refer to COPYING.txt for the AGPL license.
# All rights reserved.
# This project is developed as part of my research in the Remote Sensing Laboratory
# in Kyoto University of Advanced Science towards my Master's Degree course.
# The research was mainly supervised by Professor Salem Ibrahim Salem.
#

import argparse
from pathlib import Path
import json
from src.api_types import SGLIAPIs
from sys import exit
from io import open
import os
import tempfile

__version__ = "1.2.0"
dirs = __file__.split("/")
dir_index = -1
for i, d in enumerate(dirs):
    if d == "SGLICollect":
        dir_index = i


TEMP_FOLDER = Path(os.path.join(tempfile.gettempdir(), "SGLICollect"))
TEMP_FOLDER.mkdir(exist_ok=True)

parser = argparse.ArgumentParser(
    description="Welcome to SGLICollect!\n"
    "This API is developed for searching and downloading SGLI Images.\n"
    "This API is developed by Muhammad Salah (msalah.29.10@gmail.com)\n",
    formatter_class=argparse.RawTextHelpFormatter,
)
parser.add_argument(
    "--version",
    action="version",
    version="%(prog)s {version}".format(version=__version__),
)
parser.add_argument(
    "-s", "--search", action="store_true", help="Search GPortal for products"
)
parser.add_argument(
    "-d", "--download", action="store_true", help="Download the products"
)
parser.add_argument(
    "-e",
    "--extract",
    action="store_true",
    help="extract the pixel matching the lat, and long from the product",
)

parser.add_argument(
    "-p",
    "--product",
    nargs="?",
    help="'L1B' for level 1, 'L2R' for level 2 NWLR (Rrs), 'L2P' for level 2 IWLR (Chla, etc), or 'ALL' for JASMES",
    type=str,
)
parser.add_argument(
    "--api",
    nargs="?",
    type=SGLIAPIs,
    default=SGLIAPIs.GPORTAL,
    help="API: GPORTAL or JASMES",
)
parser.add_argument(
    "-c", "--config-file", type=Path, help="provide the arguments in a json file"
)
parser.add_argument(
    "--csv",
    nargs="?",
    type=Path,
    help="a path to a json file containing the search results",
)
parser.add_argument(
    "--no-repeat", action="store_true", help="don't repeat if identifier exists"
)
parser.add_argument(
    "--cred",
    type=Path,
    help='a path to json file containing account and password\nexample: \n{\n\t"account": "<YOUR_USERNAME>", \n\t"password": "<YOUR_PASSOWRD>"\n}',
)
parser.add_argument(
    "--download-dir",
    type=Path,
    default=TEMP_FOLDER,
    help="directory path of the download location",
)
parser.add_argument(
    "--product-dir", type=Path, help="directory containing products to extract"
)
args, _ = parser.parse_known_args()

def is_valid_GPortalLvlProd(prod: str):
    return prod == "L1B" or prod == "L2R" or prod == "L2P"

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

if not args.search and not args.download and not args.extract:
    print("No option provided!")
    parser.print_help()
    exit(1)

if args.api == SGLIAPIs.GPORTAL:
    if not is_valid_GPortalLvlProd(args.product):
        print("Invalid Product value for GPortal")
        exit(1)

if not args.csv:
    print("Data must be provided using csv")
    exit(1)

if args.download:
    args.download_dir.mkdir(exist_ok=True, parents=True) # create the download directory if it doesn't exist
    
if args.cred == None:
    print("credentials must be provided via a json file")
    exit(1)
