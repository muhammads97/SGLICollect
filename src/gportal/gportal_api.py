#
# Copyright (c) 2023 Muhammad Salah msalah.29.10@gmail.com
# Licensed under AGPL-3.0-or-later.
# Refer to COPYING.txt for the AGPL license.
# All rights reserved.
# This project is developed as part of my research in the Remote Sensing Laboratory
# in Kyoto University of Advanced Science towards my Master's Degree course.
# The research was mainly supervised by Professor Salem Ibrahim Salem.
#

import requests
import json
import numpy as np
from enum import Enum

from src.gportal.gportal_response import GPortalResponse, GPortalSearchResult
from src.gportal.gportal_types import GPortalResolution
from src.args import TEMP_FOLDER
import sys
import time
import itertools
import threading
from tqdm import tqdm
import asyncio
import os
import concurrent.futures
import functools
from pathlib import Path
from io import open

DATASETS = {
    "L1B": "10001003",
    "L2R": "10002000",
    "L2P": "10002001"
}


class GPortalLvlProd(Enum):
    L1B = "L1B"
    L2R = "L2R"
    L2P = "L2P"


class GportalApi:
    def __init__(self, type: GPortalLvlProd):
        """
        API to talk to GPortal 

        :type GPortalLvlProd L1B, L2R, or L2P
        """
        self.token = "7726524198fa59edb5564f6d939d5b168f1ed1d3288434f000028e2d1d982695f88f11a240a224e75516bca03d3aa9ec38d8dbf918b329733c0329003e9ec10f"
        self.baseurl = "https://gportal.jaxa.jp/gpr/search/catalog_records.json"
        self.headers = {
            "Cookie": "fuel_csrf_token=%s" % self.token
        }
        self.dataset = DATASETS[type.value] # select product
        self.done = False # used for the loading function

    def set_auth_details(self, cred:Path):
        """
        sets the account and password for using for download functionality.
        
        | cred: path to json file containing account and password
        |       Example:
        |       {
        |           "account": "<YOUR_USERNAME>",
        |           "password": "<YOUR_PASSWORD>"
        |       }
        """
        f = open(cred, 'r')
        j = json.load(f)
        f.close()
        self.account = j["account"]
        self.password = j["password"]

    def search(self, date: str, latitude: float, longitude: float, resolution: GPortalResolution, verbose: bool = True)->GPortalResponse:
        """
        Searchs GPortal for a single product with a specific searc criteria.

        | date   : string formated date YYYY/MM/DD
        | latitude    : None or float
        | longitude   : None or float
        | resolution  : GPortalResolution (250m or 1km)
        | verbose     : boolean 
        """
        # construct initial request body
        body = {
            "dataset[0][id]": self.dataset,
            "obsdate[0][from]": date,
            "obsdate[0][to]": date,
            "mapProjection": "EQ",
            "count": "1000",
            "coordinates": self.__construct_polygon_coordinates(longitude, latitude),
            "dataset[0][Resolution][op]": "=",
            "dataset[0][Resolution][value][]": resolution.value,
            "fuel_csrf_token": self.token
        }
        if verbose:
            # show the loading message in a separate thread and wait until search is done
            t = threading.Thread(target=self.__show_loading_msg, args=["Talking to GPortal"])
            t.start()
        
        try: # send the request and wait for the response from GPortal
            res = requests.post(self.baseurl, data=body, headers=self.headers)
        except requests.exceptions.ConnectionError: # if connection error return None
            print(
                "Connection aborted by GPortal, please try again with more specific search criteria.")
            self.done = True
            return None
        
        # stop the loading message thread
        self.done = True 
        time.sleep(0.2)

        if not res.ok:
            return None

        # parse the results
        try:
            results = json.loads(res.content)
            results = GPortalSearchResult(results)
        except:
            return None
        # filter the results to get a single product the best matchs the search criteria
        return results.filter_results(longitude, latitude)

    def download(self, url: str, output_dir: Path, max_workers=20)->Path:
        """
        Downloads a single product from GPortal.

        | url        : string url of the product to download
        | output_dir : Path of the output directory to download the product
        | max_workers: number of threads to download in parallel

        Must call set_auth_details before calling this function.
        """

        # authenticate GPortal using account and password
        self.__auth()

        # setting up the thread pool
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        loop = asyncio.new_event_loop()
        run = functools.partial(loop.run_in_executor, executor)
        asyncio.set_event_loop(loop)

        # run the download in multithreading
        try:
            loop.run_until_complete(
                self.__download(run, url, output_dir, chunk_size=10000000)
            )
        finally:
            loop.close()

        file_name = url.split("/")[-1]
        output_file = Path(os.path.join(output_dir, file_name))
        return output_file


    def __construct_polygon_coordinates(self, lon: float, lat: float):
        """constructs a polygon of size 1x1 around the latitude and longitude"""
        lon1 = str(lon - 0.5)
        lon2 = str(lon + 0.5)
        lat1 = str(lat - 0.5)
        lat2 = str(lat + 0.5)
        polygon = "POLYGON((%s %s, %s %s, %s %s, %s %s, %s %s))" % (
            lon2, lat2, lon1, lat2, lon1, lat1, lon2, lat1, lon2, lat2)
        return polygon

    def __show_loading_msg(self, msg:str="loading"):
        """shows a loading message for the search functionality"""

        for c in itertools.cycle(['|', '/', '-', '\\']):
            if self.done:
                break
            sys.stdout.write('\r' + msg + ' ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\r\n')
        
    def __auth(self):
        """
        authenticates the user on GPortal
        
        account and password must be provided via set_auth_details
        """
        auth_url = "https://gportal.jaxa.jp/gpr/auth/authenticate.json"
        body = {
        "account": self.account,
        "password": self.password,
        "fuel_csrf_token": self.token
        } 
        headers = {
            "Cookie": "fuel_csrf_token=%s" % self.token
        }

        res = requests.post(auth_url, body, headers = headers)
        if res.ok:
            # set the cookie
            cookie = res.headers["Set-Cookie"].split("secure, ")[-1]
            self.headers["Cookie"] = cookie
        elif res.status_code == 406:
            print("authentication failed!") 
    
    async def __get_size(self, url:str):
        """
        returns the size of the file to be downloaded
        """
        response = requests.head(url, headers=self.headers, stream=True)
        size = int(response.headers['Content-Length'])
        return size

    def __download_range(self, url:str, start:int, end:int, output_path:Path):
        """downloads a sequence of bytes from start to end."""
        headers = {'Range': f'bytes={start}-{end}'}
        headers.update(self.headers)
        response = requests.get(url, headers=headers, stream=True)

        with open(output_path, 'wb') as f:
            for part in response.iter_content(1024):
                f.write(part)
        self.pbar.update(1)

    async def __download(self, run, url, output_dir:Path, chunk_size=2000000):
        """download the file by dividing it into chucks of 1mb and calling a thread for each chunck"""
        file_name = url.split("/")[-1]
        print("downloading file:", file_name, "into:", output_dir.absolute())
        try:
            file_size = await self.__get_size(url)
        except:
            print("failed to get size")
            return
        output_file = Path(os.path.join(output_dir, file_name))

        # don't download if file already exists
        if output_file.exists():
            stats = os.stat(output_file)
            if stats.st_size == file_size:
                # print("file already exists!")
                return

        chunks = [(i*chunk_size, (i+1)*chunk_size-1) for i in range(file_size//chunk_size)]
        if file_size%chunk_size > 0: chunks.append((chunks[-1][1]+1, chunks[-1][1]+file_size%chunk_size+1))

        self.pbar = tqdm(total=len(chunks))
        tasks = [
            run(
                self.__download_range,
                url,
                start,
                end,
                os.path.join(TEMP_FOLDER, f'tmp_product.part{i}'),
            )
            for i, (start, end) in enumerate(chunks)
        ]
        await asyncio.wait(tasks)

        # collect the downloaded chuncks in one file
        with open(output_file, 'wb') as o:
            for i in range(len(chunks)):
                chunk_path = os.path.join(TEMP_FOLDER, f'tmp_product.part{i}')

                with open(chunk_path, 'rb') as s:
                    o.write(s.read())

                os.remove(chunk_path)

    