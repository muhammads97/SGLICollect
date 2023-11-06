from args import args
from search import search, search_csv

if __name__ == "__main__":
    if args.search:
        if args.csv:
            search_csv(args)
        else:
            search(args)
    elif args.search_csv:
        print("wait")
    elif args.download:
        print("wait")
    elif args.download_csv:
        print("wait")
