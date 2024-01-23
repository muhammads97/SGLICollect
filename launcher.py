#
# Copyright (c) 2023 Muhammad Salah msalah.29.10@gmail.com
# Licensed under AGPL-3.0-or-later.
# Refer to COPYING.txt for the AGPL license.
# All rights reserved.
# This project is developed as part of my research in the Remote Sensing Laboratory
# in Kyoto University of Advanced Science towards my Master's Degree course.
# The research was mainly supervised by Professor Salem Ibrahim Salem.
#

from src.args import args
from src.download import download, download_csv
from src.search import search, search_csv
from src.extract import extract, extract_csv
from src.utils import empty_temp

if __name__ == "__main__":
    if args.search:
        if args.csv: search_csv(args)
        else:        search(args)
    elif args.download:
        if args.csv: download_csv(args)
        else:        download(args)
    elif args.extract:
        if args.csv: extract_csv(args)
        else:        extract(args)
    empty_temp()
