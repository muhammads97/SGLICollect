from pathlib import Path
import h5py
import numpy as np

class Extractor:
    __h5: h5py.File = None
    def __init__(self, path: Path):
        print("reading file: %s" % path)
        f = h5py.File(path, 'r')
        self.__h5 = f

    def close(self):
        self.__h5.close()

    def bilin_2d(self, data: np.ndarray, interval: int, lon_mode:bool=False):
        data = data.copy()

        if lon_mode is True:
            max_diff = np.nanmax(np.abs(data[:, :-1] - data[:, 1:]))
            if max_diff > 180.:
                data[data < 0] = 360. + data[data < 0]

        data = np.concatenate((data, data[-1].reshape(1, -1)), axis=0)
        data = np.concatenate((data, data[:, -1].reshape(-1, 1)), axis=1)

        ratio_horizontal = np.tile(np.linspace(0, (interval - 1) / interval, interval, dtype=np.float32),
                                    (data.shape[0] * interval, data.shape[1] - 1))
        ratio_vertical = np.tile(
                            np.linspace(0, 
                                        (interval - 1) / interval, 
                                        interval, 
                                        dtype=np.float32
                                        ).reshape(-1, 1),
                            (data.shape[0] - 1, (data.shape[1] - 1) * interval)
                            )
        repeat_data = np.repeat(data, interval, axis=0)
        repeat_data = np.repeat(repeat_data, interval, axis=1)

        horizontal_interp = (1. - ratio_horizontal) * \
            repeat_data[:, :-interval] + \
            ratio_horizontal * repeat_data[:, interval:]
        ret = (1. - ratio_vertical) * \
            horizontal_interp[:-interval, :] + \
            ratio_vertical * horizontal_interp[interval:, :]

        if lon_mode is True:
            ret[ret > 180.] = ret[ret > 180.] - 360.

        return ret
    
    def get_lat_lon(self) -> tuple[list[float], list[float]]:
        lat = self.__h5['Geometry_data/Latitude']
        lon = self.__h5['Geometry_data/Longitude']
        resampling_interval = lat.attrs['Resampling_interval'][0]
        if resampling_interval > 1:
            lat = self.bilin_2d(lat[:], resampling_interval, False)
            lon = self.bilin_2d(lon[:], resampling_interval, True)
        (size_lin, size_pxl) = lat.shape

        img_attrs = self.__h5['Image_data'].attrs
        img_n_pix = img_attrs['Number_of_pixels'][0]
        img_n_lin = img_attrs['Number_of_lines'][0]
        if (img_n_lin <= size_lin) and (img_n_pix <= size_pxl):
            lat = lat[:img_n_lin, :img_n_pix]
            lon = lon[:img_n_lin, :img_n_pix]
        return lat, lon
    
    def get_pixel(self, lat:float, lon:float)-> dict:
        pass

    