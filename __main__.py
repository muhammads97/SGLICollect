from api_types import SGLIAPIs
from args import args
from download import download, download_csv_gportal, download_csv_jasmes
from extract import extract, extract_csv
from search import search, search_csv_gportal, search_csv_grouped_gportal, search_csv_jasmes
from utils import empty_temp

if __name__ == "__main__":
    if args.api == SGLIAPIs.GPORTAL:
        if args.search:
            if args.csv:
                if args.group:
                    search_csv_grouped_gportal(args)
                else:
                    search_csv_gportal(args)
            else:
                search(args)
        elif args.download:
            if args.csv:
                download_csv_gportal(args)
            else:
                download(args)
        elif args.extract:
            if args.csv:
                extract_csv(args)
            else:
                extract(args)
    elif args.api == SGLIAPIs.JASMES:
        if args.search:
            if args.csv:
                search_csv_jasmes(args)
            else:
                search(args)
        elif args.download:
            if args.csv:
                download_csv_jasmes(args)
            else:
                download(args)
        elif args.extract:
            if args.csv:
                extract_csv(args)
            else:
                extract(args)

    empty_temp()
