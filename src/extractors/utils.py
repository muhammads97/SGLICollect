#
# Copyright (c) 2023 Muhammad Salah msalah.29.10@gmail.com
# Licensed under AGPL-3.0-or-later.
# Refer to COPYING.txt for the AGPL license.
# All rights reserved.
# This project is developed as part of my research in the Remote Sensing Laboratory
# in Kyoto University of Advanced Science towards my Master's Degree course.
# The research was mainly supervised by Professor Salem Ibrahim Salem.
#

import numpy as np

def distance_sqr(lat:float, lat_mat:np.ndarray[float, float], lon:float, lon_mat:np.ndarray[float, float])->np.ndarray[float, float]:
    lat_diff = (lat_mat - lat)
    lon_diff = (lon_mat - lon)
    return lat_diff * lat_diff + lon_diff * lon_diff

def find_entry(lat_mat:np.ndarray[float, float], lon_mat:np.ndarray[float, float], lat:float, lon:float)-> tuple[int, int, float]:
    dist = distance_sqr(lat, lat_mat, lon, lon_mat)
    row, col = np.where(dist == np.min(dist))
    return row[0], col[0], dist[row, col]