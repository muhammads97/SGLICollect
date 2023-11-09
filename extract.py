"""
Author: Muhammad Salah
Email: msalah.29.10@gmail.com
"""

from argparse import Namespace
import os

import pandas as pd
import numpy as np
from tqdm import tqdm

from api_types import SGLIAPIs
from extractors import GPortalL1BExtractor, GPortalL2PExtractor, GPortalL2RExtractor
from gportal import GPortalLvlProd


def extract(args:Namespace):
    """
    Extracts a pixel from a single product and prints the result to the terminal.

    arguments provided through json file or cmdline arguments:
        - api: GPORTAL or JASMES, default: GPORTAL
        - level_product: L1B, L2R, or L2P
        - product_path: Path to the product to extract from
        - latitude
        - longitude

    Output depends on the level and product:
        - L1B:
            - Rt11: Reflectance at band 11  
            - Rt10: Reflectance at band 10  
            - Rt09: Reflectance at band 09  
            - Rt08: Reflectance at band 08  
            - Rt07: Reflectance at band 07  
            - Rt06: Reflectance at band 06  
            - Rt05: Reflectance at band 05  
            - Rt04: Reflectance at band 04  
            - Rt03: Reflectance at band 03  
            - Rt02: Reflectance at band 02   
            - Rt01: Reflectance at band 01
            - Lt11: Radiance at band 11
            - Lt10: Radiance at band 10
            - Lt09: Radiance at band 09
            - Lt08: Radiance at band 08
            - Lt07: Radiance at band 07
            - Lt06: Radiance at band 06
            - Lt05: Radiance at band 05
            - Lt04: Radiance at band 04
            - Lt03: Radiance at band 03
            - Lt02: Radiance at band 02
            - Lt01: Radiance at band 01
            - land: percentage of land in the pixel
        - L2R:
            - Rrs_670: Remote sensing reflectance at wavelength 670 nm
            - Rrs_565: Remote sensing reflectance at wavelength 565 nm
            - Rrs_530: Remote sensing reflectance at wavelength 530 nm
            - Rrs_490: Remote sensing reflectance at wavelength 490 nm
            - Rrs_443: Remote sensing reflectance at wavelength 443 nm
            - Rrs_412: Remote sensing reflectance at wavelength 412 nm
            - Rrs_380: Remote sensing reflectance at wavelength 380 nm
        - L2P:
            - Chla      : Chlorophyll-a concentration using JAXA's Standard Chla Algorithm for GPortal (mg/m3)
            - aCDOM_412 : absorption of Colored Desolved Organic Matter at wavelength 412 nm (1/m)
            - TSM       : Total Suspended Matter (g/m3)
    """

    if args.product_path == None:
        print("product_path must be set")
        exit(1)
    # select the apropriate extractor
    # and provide the product path
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

    # get pixel information
    pixel = extractor.get_pixel(args.latitude, args.longitude)
    # print pixel information 
    print("===> pixel information:")
    for k in pixel.keys():
        print(f"{k}: {pixel[k]}")

def extract_csv(args:Namespace):
    """
    Bulk extract operation using csv file
    arguments provided through json file or cmdline arguments:
        - api: GPORTAL or JASMES, default: GPORTAL
        - level_product: L1B, L2R, or L2P
        - csv: path to csv file
    CSV file columns:
        - identifier: product identifier
        - lat       : latitude
        - lon       : longitude
    Output columns depends on the product and level:

    - L1B:
        - Rt11: Reflectance at band 11  
        - Rt10: Reflectance at band 10  
        - Rt09: Reflectance at band 09  
        - Rt08: Reflectance at band 08  
        - Rt07: Reflectance at band 07  
        - Rt06: Reflectance at band 06  
        - Rt05: Reflectance at band 05  
        - Rt04: Reflectance at band 04  
        - Rt03: Reflectance at band 03  
        - Rt02: Reflectance at band 02   
        - Rt01: Reflectance at band 01
        - Lt11: Radiance at band 11
        - Lt10: Radiance at band 10
        - Lt09: Radiance at band 09
        - Lt08: Radiance at band 08
        - Lt07: Radiance at band 07
        - Lt06: Radiance at band 06
        - Lt05: Radiance at band 05
        - Lt04: Radiance at band 04
        - Lt03: Radiance at band 03
        - Lt02: Radiance at band 02
        - Lt01: Radiance at band 01
        - land: percentage of land in the pixel
    - L2R:
        - Rrs_670: Remote sensing reflectance at wavelength 670 nm
        - Rrs_565: Remote sensing reflectance at wavelength 565 nm
        - Rrs_530: Remote sensing reflectance at wavelength 530 nm
        - Rrs_490: Remote sensing reflectance at wavelength 490 nm
        - Rrs_443: Remote sensing reflectance at wavelength 443 nm
        - Rrs_412: Remote sensing reflectance at wavelength 412 nm
        - Rrs_380: Remote sensing reflectance at wavelength 380 nm
    - L2P:
        - Chla      : Chlorophyll-a concentration using JAXA's Standard Chla Algorithm for GPortal (mg/m3)
        - aCDOM_412 : absorption of Colored Desolved Organic Matter at wavelength 412 nm (1/m)
        - TSM       : Total Suspended Matter (g/m3)

    """
    # select the apropriate extractor as a class 
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

    # product directory must be provided
    if args.product_dir == None:
        print("product_dir must be set")
        exit(1)

    print("=============================")
    print("Extracting pixels...")
    print("=============================")

    # reading the CSV file containing the product identifier and lat, lon pairs
    df = pd.read_csv(args.csv)

    # filter for records that contain an identifier
    filtered = df[df["identifier"].str.len() == 41]
    # filter for records that contain both lat and lon
    filtered = filtered[~np.isnan(filtered[["lat", "lon"]]).any(axis=1)]
    # define the progress bar
    pbar = tqdm(filtered["identifier"], position=0, leave=True)
    # group by identifier to open the product only once
    grouped = filtered.groupby("identifier")

    for i, (id, group) in enumerate(grouped):
        # make the product path by joining the product name and the product directory
        prod_path = os.path.join(args.product_dir, Extractor.make_file_name(id))
        try:
            # try to open the product (may fail if file is corrupt)
            extractor = Extractor(prod_path)
        except:
            # move to next product if failed to open the product
            pbar.update(len(group))
            print(f"file corrupted {prod_path}")
            continue
        # for each lat, lon pair in the group extract the corresponding pixel
        for r in range(len(group)):
            lat, lon = float(group.iloc[r]["lat"]), float(group.iloc[r]["lon"])
            # extract pixel values
            pixel = extractor.get_pixel(lat, lon)

            # add the pixel to the df
            for k in pixel.keys():
                df.loc[group.index[r], k] = pixel[k]
            
            # update the progress bar
            pbar.set_description(f"{i+1}/{len(grouped)}:{id}###{r+1}/{len(group)}")
            pbar.update()
        # after each product is processed save the data to the csv
        df.to_csv(args.csv)

    # finally, close the progress bar and save to the csv
    pbar.close()
    df.to_csv(args.csv)





    