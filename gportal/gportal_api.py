import requests
import json
import numpy as np
from enum import Enum
from .gportal_response import GPortalSearchResult
from .gportal_types import GPortalResolution
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
import glob

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
        self.token = "7726524198fa59edb5564f6d939d5b168f1ed1d3288434f000028e2d1d982695f88f11a240a224e75516bca03d3aa9ec38d8dbf918b329733c0329003e9ec10f"
        self.baseurl = "https://gportal.jaxa.jp/gpr/search/catalog_records.json"
        self.headers = {
            "Cookie": "fuel_csrf_token=%s" % self.token
        }
        self.dataset = DATASETS[type.value]
        self.done = False

    def set_auth_details(self, account:str, password: str):
        self.account = account
        self.password = password

    def search(self, from_date: str, to_date: str, latitude: float, longitude: float, resolution: GPortalResolution, path_number: int = None, scene_number: int = None, show_loading: bool = True):
        body = {
            "dataset[0][id]": self.dataset,
            "obsdate[0][from]": from_date,
            "obsdate[0][to]": to_date,
            "mapProjection": "EQ",
            "count": "1000",
            "dataset[0][Resolution][op]": "=",
            "dataset[0][Resolution][value][]": resolution.value,
            "fuel_csrf_token": self.token
        }
        if path_number:
            body["dataset[0][OrbitNumber][op]"] = "="
            body["dataset[0][OrbitNumber][value]"] = str(path_number).zfill(3)
        if scene_number:
            body["dataset[0][sceneNumber][op]"] = "="
            body["dataset[0][sceneNumber][value]"] = str(scene_number).zfill(2)
        if latitude != None and longitude != None:
            body["coordinates"] = self.__construct_polygon_coordinates(longitude, latitude),
        if show_loading:
            t = threading.Thread(target=self.__animate, args=["Talking to GPortal"])
            t.start()
        try:
            res = requests.post(self.baseurl, data=body, headers=self.headers)
        except requests.exceptions.ConnectionError:
            print(
                "Connection aborted by GPortal, please try again with more specific search criteria.")
            self.done = True
            exit(1)
        self.done = True
        time.sleep(0.2)
        results = json.loads(res.content)
        results = GPortalSearchResult(results)
        return results.filter_results(longitude, latitude)

    def download(self, url: str, output_dir: Path, max_workers=20):
        self.__auth()
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        loop = asyncio.new_event_loop()
        run = functools.partial(loop.run_in_executor, executor)

        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(
                self.__download(run, url, output_dir)
            )
        finally:
            loop.close()

    def __construct_polygon_coordinates(self, lon: float, lat: float):
        lon1 = str(lon - 0.5)
        lon2 = str(lon + 0.5)
        lat1 = str(lat - 0.5)
        lat2 = str(lat + 0.5)
        polygon = "POLYGON((%s %s, %s %s, %s %s, %s %s, %s %s))" % (
            lon2, lat2, lon1, lat2, lon1, lat1, lon2, lat1, lon2, lat2)
        return polygon

    def __animate(self, msg:str="loading"):
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if self.done:
                break
            sys.stdout.write('\r' + msg + ' ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\r\n')
        
    def __auth(self):
        auth_url = "https://gportal.jaxa.jp/gpr/auth/authenticate.json"
        body = {
        "account": self.account,
        "password": self.password,
        "fuel_csrf_token": self.token
        } 

        res = requests.post(auth_url, body, headers = self.headers)
        if res.ok:
            cookie = res.headers["Set-Cookie"].split("secure, ")[-1]
            self.headers["Cookie"] = cookie
        else:
            print("auth failed!") 
    
    async def __get_size(self, url:str):
        response = requests.head(url, headers=self.headers)
        size = int(response.headers['Content-Length'])
        return size

    def __download_range(self, url:str, start:int, end:int, output_path:Path):
        headers = {'Range': f'bytes={start}-{end}'}
        headers.update(self.headers)
        response = requests.get(url, headers=headers)

        with open(output_path, 'wb') as f:
            for part in response.iter_content(1024):
                f.write(part)
        self.pbar.update(1)

    async def __download(self, run, url, output_dir:Path, chunk_size=1000000):
        file_size = await self.__get_size(url)
        chunks = range(0, file_size, chunk_size)
        self.pbar = tqdm(total=len(chunks))
        tasks = [
            run(
                self.__download_range,
                url,
                start,
                start + chunk_size - 1,
                f'./temp/tmp_product.part{i}',
            )
            for i, start in enumerate(chunks)
        ]
        await asyncio.wait(tasks)

        file_name = url.split("/")[-1]
        with open(os.path.join(output_dir, file_name), 'wb') as o:
            for i in range(len(chunks)):
                chunk_path = f'./temp/tmp_product.part{i}'

                with open(chunk_path, 'rb') as s:
                    o.write(s.read())

                os.remove(chunk_path)

    