from .gportal_resolution import GPortalResolution


class GPortalMeta:
    datasetId: str
    totalQualityCode: str
    cloudCoverPercentage: int
    operatorComment: str
    compressFlag: int
    physicalQuantity: str
    resolution: GPortalResolution
    browseImageSize: int
    parameterVersion: int
    algorithmVersion: int
    numberPixels: int
    numberLines: int
    numberBands: int
    numberMissingData: int
    sceneNumber: int
    startPathNumber: int
    endPathNumber: int
    startArgumentLat: float
    endArgumentLat: float
    mapProjection: str
    mapDirection: str
    orbitDirection: str
    tileNo: str
    channels: list[list[str]]
    bandWidth: list[list[str]]
    downlinkSegmentNumber: str
    sensorOffPeriod: str
    sceneCenterTime: str
    startSubsatellitePosition: tuple[float]
    endSubsatellitePosition: tuple[float]
    ProcessTimeUnit: str
    tileHNo: str
    tileVNo: str
    topicCategory: str
    organizationName: str
    pseq: str
    hasProduct: bool

    def __init__(self, response) -> None:
        self.datasetId = str(response["datasetId"])
        self.totalQualityCode = str(response["totalQualityCode"])
        self.cloudCoverPercentage = int(response["cloudCoverPercentage"])
        self.operatorComment = str(response["operatorComment"])
        self.compressFlag = int(response["compressFlag"])
        self.physicalQuantity = str(response["physicalQuantity"])
        self.resolution = GPortalResolution(response["Resolution"])
        self.browseImageSize = int(response["browseImageSize"])
        self.parameterVersion = int(response["parameterVersion"])
        self.algorithmVersion = int(response["algorithmVersion"])
        self.numberPixels = int(response["numberPixels"])
        self.numberLines = int(response["numberLines"])
        self.numberBands = int(response["numberBands"])
        self.numberMissingData = int(response["numberMissingData"])
        self.sceneNumber = int(response["sceneNumber"])
        self.startPathNumber = int(response["startPathNumber"])
        self.endPathNumber = int(response["endPathNumber"])
        self.startArgumentLat = float(response["startArgumentLat"])
        self.endArgumentLat = float(response["endArgumentLat"])
        self.mapProjection = str(response["mapProjection"])
        self.mapDirection = str(response["mapDirection"])
        self.orbitDirection = str(response["orbitDirection"])
        self.tileNo = str(response["tileNo"])
        self.channels = [part.split(" ")
                         for part in response["channels"].split(", ")]
        self.bandWidth = [part.split(" ")
                          for part in response["bandWidth"].split(", ")]
        self.downlinkSegmentNumber = str(response["downlinkSegmentNumber"])
        self.sensorOffPeriod = str(response["sensorOffPeriod"])
        self.sceneCenterTime = str(response["sceneCenterTime"])
        self.startSubsatellitePosition = tuple(
            [float(coord) for coord in response["startSubsatellitePosition"].split(" ")])
        self.endSubsatellitePosition = tuple(
            [float(coord) for coord in response["endSubsatellitePosition"].split(" ")])
        self.ProcessTimeUnit = str(response["ProcessTimeUnit"])
        self.tileHNo = str(response["tileHNo"])
        self.tileVNo = str(response["tileVNo"])
        self.topicCategory = str(response["topicCategory"])
        self.organizationName = str(response["organizationName"])
        self.pseq = str(response["pseq"])
        self.hasProduct = bool(response["hasProduct"])

    def to_json(self) -> dict:
        return {
            "datasetId": self.datasetId,
            "totalQualityCode": self.totalQualityCode,
            "cloudCoverPercentage": self.cloudCoverPercentage,
            "operatorComment": self.operatorComment,
            "compressFlag": self.compressFlag,
            "physicalQuantity": self.physicalQuantity,
            "resolution": self.resolution.value,
            "browseImageSize": self.browseImageSize,
            "parameterVersion": self.parameterVersion,
            "algorithmVersion": self.algorithmVersion,
            "numberPixels": self.numberPixels,
            "numberLines": self.numberLines,
            "numberBands": self.numberBands,
            "numberMissingData": self.numberMissingData,
            "sceneNumber": self.sceneNumber,
            "startPathNumber": self.startPathNumber,
            "endPathNumber": self.endPathNumber,
            "startArgumentLat": self.startArgumentLat,
            "endArgumentLat": self.endArgumentLat,
            "mapProjection": self.mapProjection,
            "mapDirection": self.mapDirection,
            "orbitDirection": self.orbitDirection,
            "tileNo": self.tileNo,
            "channels": self.channels,
            "bandWidth": self.bandWidth,
            "downlinkSegmentNumber": self.downlinkSegmentNumber,
            "sensorOffPeriod": self.sensorOffPeriod,
            "sceneCenterTime": self.sceneCenterTime,
            "startSubsatellitePosition": self.startSubsatellitePosition,
            "endSubsatellitePosition": self.endSubsatellitePosition,
            "ProcessTimeUnit": self.ProcessTimeUnit,
            "tileHNo": self.tileHNo,
            "tileVNo": self.tileVNo,
            "topicCategory": self.topicCategory,
            "organizationName": self.organizationName,
            "pseq": self.pseq,
            "hasProduct": self.hasProduct
        }
