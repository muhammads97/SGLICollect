from ftplib import FTP

import pandas as pd

OUTPUT_COLUMNS = [
    "file_name",
    "ftp_path",
    "file_size",
    "box_id"
]

class JASMESResponse:
    coordinates:list[list[float]]
    fileName: str
    filePath: str
    fileSize: int
    boxId: int

    def __init__(self, fileName:str, coordinates:list[list[float]], fileSize:int, filePath:str):
        """
        Object to represent the response from JASMES FTP server

        | fileName      str file name on the server
        | coordinates   list of pairs of floating point numbers representing the coordinates in lat and lon of the product
        | fileSize      size of the file in bytes
        | filePath      path of the file on the server
        """
        self.fileName = fileName
        self.coordinates = coordinates
        self.boxId = int(fileName.split(".")[0][-2:-1])
        self.fileSize = fileSize
        self.filePath = filePath

    def print(self):
        """
        prints the product to screen
        """
        print(
            "File Name: %s"%self.fileName,
            "File Size: %s"%self.fileSize,
            "Path: %s"%self.filePath,
            "Box ID: %s"%self.boxId,
            sep="\n"
        )

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
                "file_name"    : self.fileName,
                "ftp_path"   : self.filePath,
                "file_size"    : self.fileSize,
                "box_id"   : self.boxId,
            }], columns=OUTPUT_COLUMNS)
            df = pd.concat([df, j], axis=0, ignore_index=True)
        else:
            index = df.index[index]
            df.loc[index, "file_name"] = self.fileName
            df.loc[index, "ftp_path"]=self.filePath
            df.loc[index, "file_size"]=self.fileSize
            df.loc[index, "box_id"]=self.boxId
        return df
