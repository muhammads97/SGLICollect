from args import args
from download import download, download_csv
from extract import extract
from search import search, search_csv, search_csv_grouped
from utils import empty_temp

if __name__ == "__main__":
    if args.search:
        if args.csv:
            if args.group:
                search_csv_grouped(args)
            else:
                search_csv(args)
        else:
            search(args)
    elif args.download:
        if args.csv:
            download_csv(args)
        else:
            download(args)
    elif args.extract:
        if args.csv:
            print("wait")
        else:
            extract(args)

    empty_temp()
