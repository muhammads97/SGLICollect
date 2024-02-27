#
# Copyright (c) 2024 Muhammad Salah msalah.29.10@gmail.com
# Licensed under AGPL-3.0-or-later.
# Refer to COPYING.txt for the AGPL license.
# All rights reserved.
# This project is developed as part of my research in the Remote Sensing Laboratory
# in Kyoto University of Advanced Science towards my Master's Degree course.
# The research was mainly supervised by Professor Salem Ibrahim Salem.
#

import json
from pathlib import Path
from src.jasmes.jasmes_api import JASMESProd, JasmesApi
from src.jasmes.jasmes_types.jasmes_collection import JASMESCollection
from argparse import Namespace

class JasmesCollector(JasmesApi):
    def __init__(self):
        super().__init__(JASMESProd.NWLR_380)         

    def search(self, date: str, latitude: float, longitude: float, resolution=None, verbose: bool = True):
            # NWLR
            super().set_prod(JASMESProd.NWLR_380)
            res = super().search(date, latitude, longitude, resolution, verbose)
            if res == None:
                 return None
            ftp_path_NWLR_380 = res.filePath
            ftp_path_NWLR_412 = ftp_path_NWLR_380.replace("NWLR_380", "NWLR_412")
            ftp_path_NWLR_443 = ftp_path_NWLR_380.replace("NWLR_380", "NWLR_443")
            ftp_path_NWLR_490 = ftp_path_NWLR_380.replace("NWLR_380", "NWLR_490")
            ftp_path_NWLR_530 = ftp_path_NWLR_380.replace("NWLR_380", "NWLR_530")
            ftp_path_NWLR_565 = ftp_path_NWLR_380.replace("NWLR_380", "NWLR_565")
            ftp_path_NWLR_670 = ftp_path_NWLR_380.replace("NWLR_380", "NWLR_670")
            # CDOM, Chla, TSM
            super().set_prod(JASMESProd.CDOM)
            res = super().search(date, latitude, longitude, resolution, verbose)
            if res == None:
                 return None
            ftp_path_CDOM = res.filePath
            ftp_path_CHLA = ftp_path_CDOM.replace("CDOM", "CHLA")
            ftp_path_TSM = ftp_path_CDOM.replace("CDOM", "TSM")
            # SST
            super().set_prod(JASMESProd.SST)
            res = super().search(date, latitude, longitude, resolution, verbose)
            if res == None:
                 return None
            ftp_path_SST = res.filePath
            
            return JASMESCollection(
                ftp_path_NWLR_380,
                ftp_path_NWLR_412,
                ftp_path_NWLR_443,
                ftp_path_NWLR_490,
                ftp_path_NWLR_530,
                ftp_path_NWLR_565,
                ftp_path_NWLR_670,
                ftp_path_CDOM,
                ftp_path_CHLA,
                ftp_path_TSM,
                ftp_path_SST,
                )
    def download(self, ftp_paths: dict, output_dir: Path) -> Path:
        paths = {}
        for k in ftp_paths.keys():
            path = super().download(ftp_paths[k], output_dir)
            paths[k] = str(path)
        return json.dumps(paths)