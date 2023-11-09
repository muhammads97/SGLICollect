import numpy as np

def distance_sqr(lat:float, lat_mat:np.ndarray[float, float], lon:float, lon_mat:np.ndarray[float, float])->np.ndarray[float, float]:
    lat_diff = (lat_mat - lat)
    lon_diff = (lon_mat - lon)
    return lat_diff * lat_diff + lon_diff * lon_diff

def find_entry(lat_mat:np.ndarray[float, float], lon_mat:np.ndarray[float, float], lat:float, lon:float)-> tuple[int, int, float]:
    dist = distance_sqr(lat, lat_mat, lon, lon_mat)
    row, col = np.where(dist == np.min(dist))
    return row[0], col[0], dist[row, col]