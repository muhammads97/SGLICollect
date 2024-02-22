#
# Copyright (c) 2023 Muhammad Salah msalah.29.10@gmail.com
# Licensed under AGPL-3.0-or-later.
# Refer to COPYING.txt for the AGPL license.
# All rights reserved.
# This project is developed as part of my research in the Remote Sensing Laboratory
# in Kyoto University of Advanced Science towards my Master's Degree course.
# The research was mainly supervised by Professor Salem Ibrahim Salem.
#

from datetime import datetime
from enum import Enum
import json
import os
from pathlib import Path
from ftplib import FTP
from dateutil import parser
import numpy as np
from tqdm import tqdm

from src.jasmes.jasmes_types import JASMESResponse
from src.jasmes.jasmes_cooredinates import COORDINATES
from io import open

class JASMESProd(Enum):
    NWLR_380            = "NWLR_380"
    NWLR_412            = "NWLR_412"
    NWLR_443            = "NWLR_443"
    NWLR_490            = "NWLR_490"
    NWLR_530            = "NWLR_530"
    NWLR_565            = "NWLR_565"
    NWLR_670            = "NWLR_670"
    PAR                 = "PAR"
    TAUA_670            = "TAUA_670"
    TAUA_865            = "TAUA_865"
    FAI                 = "FAI"
    CDOM                = "CDOM"
    CHLA                = "CHLA"
    TSM                 = "TSM"
    SST                 = "SST"
    Cloud_probability   = "Cloud_probability"

class JasmesApi:
    __logged_in = False
    __ftp: FTP
    def __init__(self, type: JASMESProd):
        """
        API to talk to JASMES FTP server 

        :type JASMESProd
        """

        self.__prod = type
        self.__ftp = FTP("apollo.eorc.jaxa.jp")
    def set_auth_details(self, cred:Path):
        """
        sets the account and password for using for download functionality.
        
        | cred: path to json file containing account and password
        |       Example:
        |       {
        |           "account": "<YOUR_USERNAME>",
        |           "password": "<YOUR_PASSWORD>"
        |       }

        Note: account is anonymous and password is email used for registration on JASMES.
        """
        f = open(cred, 'r')
        j = json.load(f)
        f.close()
        self.account = j["account"]
        self.password = j["password"]

    def search(self, date: str, latitude: float, longitude: float, resolution=None, verbose: bool = True):
        """
        Searchs GPortal for a single product with a specific searc criteria.

        | date   : string formated date YYYY/MM/DD
        | latitude    : None or float
        | longitude   : None or float
        | verbose     : boolean 
        """
        parsed_date = parser.parse(date)
        if not self.__login():
            return None
        if not self.__go_to_product_directory():
            return None
        if not self.__go_to_date(parsed_date):
            return None
        box_id = self.__find_square(latitude, longitude)
        if box_id == -1:
            return None
        
        files = self.__ftp.nlst()
        file = None
        fileSize = 0
        for f in files:
            if f.endswith(f"{str(box_id).zfill(2)}.nc"):
                self.__ftp.voidcmd("TYPE I")
                size = self.__ftp.size(f)
                if size > fileSize:
                    file = f
                    fileSize = size
        if file == None:
            return None
        dir = os.path.join(self.__ftp.pwd(), file)
        return JASMESResponse(file, COORDINATES[box_id], fileSize, dir)
        
        
    def download(self, ftp_path: str, output_dir: Path)->Path:
        """
        Downloads a single product from JASMES using ftp.

        | ftp_path   : string path of the product to download on the ftp server
        | output_dir : Path of the output directory to download the product

        """
        if not self.__login():
            return None
        file_name = ftp_path.split("/")[-1]
        dir = "/".join(ftp_path.split("/")[:-1])
        self.__ftp.cwd(dir)
        self.__ftp.voidcmd("TYPE I")
        size = self.__ftp.size(file_name)
        nblocks = (size // 8192) + (size % 8192 != 0)
        self.__pbar = tqdm(total=nblocks, unit="block")
        self.__pbar.set_description(f"{file_name}")
        # don't download if file already exists
        output_file = Path(os.path.join(output_dir, file_name))
        if output_file.exists():
            stats = os.stat(output_file)
            if stats.st_size == size:
                self.__pbar.update(nblocks)
                self.__pbar.close()
                return output_file
            
        self.__output = open(output_file, "wb")
        
        
        self.__ftp.retrbinary("RETR %s"%file_name, self.__download_callback)
        self.__output.close()
        return output_file
        
    def close(self):
        self.__ftp.quit()

    def __download_callback(self, data:bytes)->object:
        self.__pbar.update(1)
        return self.__output.write(data)

    def __go_to_product_directory(self)->bool:
        if self.__prod == JASMESProd.NWLR_380:
            response = self.__ftp.cwd("/pub/SGLI_NRT/L2_Ocean_atmospheric_correction/NWLR_380")
        elif self.__prod == JASMESProd.NWLR_412:
            response = self.__ftp.cwd("/pub/SGLI_NRT/L2_Ocean_atmospheric_correction/NWLR_412")
        elif self.__prod == JASMESProd.NWLR_443:
            response = self.__ftp.cwd("/pub/SGLI_NRT/L2_Ocean_atmospheric_correction/NWLR_443")
        elif self.__prod == JASMESProd.NWLR_490:
            response = self.__ftp.cwd("/pub/SGLI_NRT/L2_Ocean_atmospheric_correction/NWLR_490")
        elif self.__prod == JASMESProd.NWLR_530:
            response = self.__ftp.cwd("/pub/SGLI_NRT/L2_Ocean_atmospheric_correction/NWLR_530")
        elif self.__prod == JASMESProd.NWLR_565:
            response = self.__ftp.cwd("/pub/SGLI_NRT/L2_Ocean_atmospheric_correction/NWLR_565")
        elif self.__prod == JASMESProd.NWLR_670:
            response = self.__ftp.cwd("/pub/SGLI_NRT/L2_Ocean_atmospheric_correction/NWLR_670")
        elif self.__prod == JASMESProd.PAR:
            response = self.__ftp.cwd("/pub/SGLI_NRT/L2_Ocean_atmospheric_correction/PAR")
        elif self.__prod == JASMESProd.TAUA_670:
            response = self.__ftp.cwd("/pub/SGLI_NRT/L2_Ocean_atmospheric_correction/TAUA_670")
        elif self.__prod == JASMESProd.TAUA_865:
            response = self.__ftp.cwd("/pub/SGLI_NRT/L2_Ocean_atmospheric_correction/TAUA_865")
        elif self.__prod == JASMESProd.FAI:
            response = self.__ftp.cwd("/pub/SGLI_NRT/L2_Ocean_atmospheric_correction/TAUA_865")
        elif self.__prod == JASMESProd.CHLA:
            response = self.__ftp.cwd("/pub/SGLI_NRT/L2_In-water_properties/CHLA")
        elif self.__prod == JASMESProd.CDOM:
            response = self.__ftp.cwd("/pub/SGLI_NRT/L2_In-water_properties/CDOM")
        elif self.__prod == JASMESProd.TSM:
            response = self.__ftp.cwd("/pub/SGLI_NRT/L2_In-water_properties/TSM")
        elif self.__prod == JASMESProd.SST:
            response = self.__ftp.cwd("/pub/SGLI_NRT/L2_Thermal_analysis/SST")
        elif self.__prod == JASMESProd.Cloud_probability:
            response = self.__ftp.cwd("/pub/SGLI_NRT/L2_Thermal_analysis/Cloud_probability")
        else:
            print("Product %s is not supported yet.."%self.__prod.value)
            exit(1)
        if not response.startswith("250"):
            print("cannot open product directory")
            return False
        else: return True
    def __find_square(self, lat:float, lon:float)->int:
        i = 1
        while(i <= 16):
            box = np.array(COORDINATES[i-1]).T
            max_lat = np.array(box[0]).max()
            min_lat = np.array(box[0]).min()
            max_lon = np.array(box[1]).max()
            min_lon = np.array(box[1]).min()
            if lat >= min_lat and lat <= max_lat and lon >= min_lon and lon <= max_lon:
                return i
            i += 1
        return -1

    def __go_to_date(self, date:datetime)->bool:
        year    = str(date.year).zfill(4)
        month   = str(date.month).zfill(2)
        day     = str(date.day).zfill(2)
        try:
            response = self.__ftp.cwd(f"{year}/{month}/{day}")
            if response.startswith("250"): return True
            else:
                print("cannot find date")
                return False
        except:
            return False
        
    def __login(self):
        if not self.__logged_in:
            response = self.__ftp.login(self.account, self.password)
            if not response.startswith("230"):
                print("login failed")
                return False
            else:
                return True
        else: return True
