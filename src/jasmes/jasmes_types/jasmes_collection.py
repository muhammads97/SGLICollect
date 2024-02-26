#
# Copyright (c) 2024 Muhammad Salah msalah.29.10@gmail.com
# Licensed under AGPL-3.0-or-later.
# Refer to COPYING.txt for the AGPL license.
# All rights reserved.
# This project is developed as part of my research in the Remote Sensing Laboratory
# in Kyoto University of Advanced Science towards my Master's Degree course.
# The research was mainly supervised by Professor Salem Ibrahim Salem.
#

import pandas as pd
import json
OUTPUT_COLUMNS = [
    "ftp_path_NWLR_380",
    "ftp_path_NWLR_412",
    "ftp_path_NWLR_443",
    "ftp_path_NWLR_490",
    "ftp_path_NWLR_530",
    "ftp_path_NWLR_565",
    "ftp_path_NWLR_670",
    "ftp_path_CDOM",
    "ftp_path_CHLA",
    "ftp_path_TSM",
    "ftp_path_SST",
]
class JASMESCollection:
    ftp_path_380: str
    ftp_path_412: str
    ftp_path_443: str
    ftp_path_490: str
    ftp_path_530: str
    ftp_path_565: str
    ftp_path_670: str
    ftp_path_CDOM: str
    ftp_path_CHLA: str
    ftp_path_TSM: str
    ftp_path_SST: str

    def __init__(self, 
                ftp_path_380: str,
                ftp_path_412: str,
                ftp_path_443: str,
                ftp_path_490: str,
                ftp_path_530: str,
                ftp_path_565: str,
                ftp_path_670: str,
                ftp_path_CDOM: str,
                ftp_path_CHLA: str,
                ftp_path_TSM: str,
                ftp_path_SST: str,
                 ):
        """
        Object to represent the response from JASMES FTP server

        | fileNames     list of str file names on the server
        | filePaths     list of str file paths on the server
        """
        self.ftp_path_380 = ftp_path_380
        self.ftp_path_412 = ftp_path_412
        self.ftp_path_443 = ftp_path_443
        self.ftp_path_490 = ftp_path_490
        self.ftp_path_530 = ftp_path_530
        self.ftp_path_565 = ftp_path_565
        self.ftp_path_670 = ftp_path_670
        self.ftp_path_CDOM = ftp_path_CDOM
        self.ftp_path_CHLA = ftp_path_CHLA
        self.ftp_path_TSM = ftp_path_TSM
        self.ftp_path_SST = ftp_path_SST

    def print(self):
        """
        prints the product to screen
        """
        print("Files found:")
        print(
            "ftp_path_NWLR_380: %s"%self.ftp_path_380,
            "ftp_path_NWLR_412: %s"%self.ftp_path_412,
            "ftp_path_NWLR_443: %s"%self.ftp_path_443,
            "ftp_path_NWLR_490: %s"%self.ftp_path_490,
            "ftp_path_NWLR_530: %s"%self.ftp_path_530,
            "ftp_path_NWLR_565: %s"%self.ftp_path_565,
            "ftp_path_NWLR_670: %s"%self.ftp_path_670,
            "ftp_path_CDOM: %s"%self.ftp_path_CDOM,
            "ftp_path_CHLA: %s"%self.ftp_path_CHLA,
            "ftp_path_TSM: %s"%self.ftp_path_TSM,
            "ftp_path_SST: %s"%self.ftp_path_SST,
            sep="\n"
        )

    def get_json(self):
        return json.dumps({
            "ftp_path_NWLR_380": self.ftp_path_380,
            "ftp_path_NWLR_412": self.ftp_path_412,
            "ftp_path_NWLR_443": self.ftp_path_443,
            "ftp_path_NWLR_490": self.ftp_path_490,
            "ftp_path_NWLR_530": self.ftp_path_530,
            "ftp_path_NWLR_565": self.ftp_path_565,
            "ftp_path_NWLR_670": self.ftp_path_670,
            "ftp_path_CDOM":self.ftp_path_CDOM,
            "ftp_path_CHLA":self.ftp_path_CHLA,
            "ftp_path_TSM":self.ftp_path_TSM,
            "ftp_path_SST":self.ftp_path_SST,
        })


    def to_dataframe(self, df:pd.DataFrame=None, index:int=None):
        """
        appends the response to a dataframe in index
        """
        if df is None:
            df = pd.DataFrame(columns=OUTPUT_COLUMNS)
        if index is None:
            index = 0
            for c in OUTPUT_COLUMNS:
                if c not in df.columns:
                    df[c] = []
        if(index == df.size):
            j = pd.DataFrame([{
                "ftp_path_NWLR_380": self.ftp_path_380,
                "ftp_path_NWLR_412": self.ftp_path_412,
                "ftp_path_NWLR_443": self.ftp_path_443,
                "ftp_path_NWLR_490": self.ftp_path_490,
                "ftp_path_NWLR_530": self.ftp_path_530,
                "ftp_path_NWLR_565": self.ftp_path_565,
                "ftp_path_NWLR_670": self.ftp_path_670,
                "ftp_path_CDOM": self.ftp_path_CDOM,
                "ftp_path_CHLA": self.ftp_path_CHLA,
                "ftp_path_TSM": self.ftp_path_TSM,
                "ftp_path_SST": self.ftp_path_SST,
            }], columns=OUTPUT_COLUMNS)
            df = pd.concat([df, j], axis=0, ignore_index=True)
        else:
            index = df.index[index]
            df.loc[index, "ftp_path_NWLR_380"] = self.ftp_path_380
            df.loc[index, "ftp_path_NWLR_412"] = self.ftp_path_412
            df.loc[index, "ftp_path_NWLR_443"] = self.ftp_path_443
            df.loc[index, "ftp_path_NWLR_490"] = self.ftp_path_490
            df.loc[index, "ftp_path_NWLR_530"] = self.ftp_path_530
            df.loc[index, "ftp_path_NWLR_565"] = self.ftp_path_565
            df.loc[index, "ftp_path_NWLR_670"] = self.ftp_path_670
            df.loc[index, "ftp_path_CDOM"] = self.ftp_path_CDOM
            df.loc[index, "ftp_path_CHLA"] = self.ftp_path_CHLA
            df.loc[index, "ftp_path_TSM"] = self.ftp_path_TSM
            df.loc[index, "ftp_path_SST"] = self.ftp_path_SST
        return df
