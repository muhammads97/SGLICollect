from argparse import Namespace
from api_types import *
from gportal import GportalApi
import pandas as pd
import numpy as np
from tqdm import tqdm

from gportal.gportal_types.gportal_resolution import GPortalResolution

def get_value(d: dict, key: str):
    if key in d and d[key]:
        return d[key]

def search(args: Namespace):
    if args.api == SGLIAPIs.GPORTAL:
        api = GportalApi(args.level_product)
    else:
        print("to be implemented")
        exit(1)
    result = api.search(args.date, args.date, args.latitude, args.longitude,
                        args.resolution, args.path_number, args.scene_number)
    print("returned results: ")
    result.print()

def search_csv(args: Namespace):
    if args.api == SGLIAPIs.GPORTAL:
        api = GportalApi(args.level_product)
    else:
        print("to be implemented")
        exit(1)

    df = pd.read_csv(args.csv)
    pbar = tqdm(total=len(df), position=0, leave=True)
    for i in range(len(df)):
        row = df.iloc[i].fillna(0).to_dict()

        date, lat, lon = get_value(row, "date"), get_value(row, "lat"), get_value(row, "lon")
        path_number, scene_number = get_value(row, "path_number"), get_value(row, "scene_number")
        resolution = get_value(row, "resolution")
        id = get_value(row, "identifier")

        if resolution: resolution = GPortalResolution.from_int(int(resolution))
        else: resolution = GPortalResolution.H

        if id and args.no_repeat: 
            pbar.update(1)
            continue

        result = api.search(date, date, lat, lon, resolution, path_number, scene_number, show_loading=False)

        if result != None:
            result.to_dataframe(df, i)

        pbar.update(1)

        if (i % 100 == 0): df.to_csv(args.csv, index=False)

    df.to_csv(args.csv, index=False)
    pbar.close()
        

