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

    def construct_polygon_coordinates(self, lon: float, lat: float):
        lon1 = str(lon - 0.5)
        lon2 = str(lon + 0.5)
        lat1 = str(lat - 0.5)
        lat2 = str(lat + 0.5)
        polygon = "POLYGON((%s %s, %s %s, %s %s, %s %s, %s %s))" % (
            lon2, lat2, lon1, lat2, lon1, lat1, lon2, lat1, lon2, lat2)
        return polygon

    def animate(self, msg="loading"):
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if self.done:
                break
            sys.stdout.write('\r' + msg + ' ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\r\n')

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
            body["coordinates"] = self.construct_polygon_coordinates(longitude, latitude),
        if show_loading:
            t = threading.Thread(target=self.animate, args=["Talking to GPortal"])
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
        

    def auth(self, account: str, password: str):
        body = {
            "account": account,
            "password": password,
            "fuel_csrf_token": self.token
        }
        auth_url = "https://gportal.jaxa.jp/gpr/auth/authenticate.json"
        res = requests.post(auth_url, body, headers=self.headers)
        return res
