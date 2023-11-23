"""
Author: Muhammad Salah
Email: msalah.29.10@gmail.com
"""
from src import args
from src import download, download_csv, search, search_csv, extract, extract_csv, empty_temp

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
