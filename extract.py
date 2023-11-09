"""
Author: Muhammad Salah
Email: msalah.29.10@gmail.com
"""

from argparse import Namespace
import os

import pandas as pd
from tqdm import tqdm

from api_types import SGLIAPIs
from extractors import GPortalL1BExtractor, GPortalL2PExtractor, GPortalL2RExtractor
from gportal import GPortalLvlProd


def extract(args:Namespace):
    # select the apropriate extractor
    if args.api == SGLIAPIs.GPORTAL:
        if args.level_product == GPortalLvlProd.L1B:
            extractor = GPortalL1BExtractor(args.product_path)
        elif args.level_product == GPortalLvlProd.L2R:
            extractor = GPortalL2RExtractor(args.product_path)
        elif args.level_product == GPortalLvlProd.L2P:
            extractor = GPortalL2PExtractor(args.product_path)
        else:
            print("level or product not supported yet")
            exit(1)
    else:
        print("to be implemented")
        exit(1)

    pixel = extractor.get_pixel(args.latitude, args.longitude)
    print("===> pixel information:")
    for k in pixel.keys():
        print(f"{k}: {pixel[k]}")

def extract_csv(args:Namespace):
    # select the apropriate extractor
    if args.api == SGLIAPIs.GPORTAL:
        if args.level_product == GPortalLvlProd.L1B:
            Extractor = GPortalL1BExtractor
        elif args.level_product == GPortalLvlProd.L2R:
            Extractor = GPortalL2RExtractor
        elif args.level_product == GPortalLvlProd.L2P:
            Extractor = GPortalL2PExtractor
        else:
            print("level or product not supported yet")
            exit(1)
    else:
        print("to be implemented")
        exit(1)

    if args.product_dir == None:
        print("product_dir must be set")
        exit(1)

    print("=============================")
    print("Extracting pixels...")
    print("=============================")

    df = pd.read_csv(args.csv)
    filtered = df[df["identifier"].str.len() == 41]
    pbar = tqdm(filtered["identifier"], position=0, leave=True)
    grouped = filtered.groupby("identifier")
    for i, (id, group) in enumerate(grouped):
        prod_path = os.path.join(args.product_dir, Extractor.make_file_name(id))
        try:
            extractor = Extractor(prod_path)
        except:
            print(f"file corrupted {prod_path}")
            continue
        for r in range(len(group)):
            lat, lon = float(group.iloc[r]["lat"]), float(group.iloc[r]["lon"])
            pixel = extractor.get_pixel(lat, lon)

            for k in pixel.keys():
                df.loc[group.index[r], k] = pixel[k]
            
            pbar.set_description(f"{i+1}/{len(grouped)}:{id}###{r+1}/{len(group)}")
            pbar.update()
        df.to_csv(args.csv)
    pbar.close()
    df.to_csv(args.csv)





    