"""
Author: Muhammad Salah
Email: msalah.29.10@gmail.com
"""
from .gportal_product import GPortalProduct
from .gportal_preview import GPortalPreview
from .gportal_meta import GPortalMeta


class GPortalProperties:
    identifier: str
    acquisitionType: str
    imageQualityDegradation: str
    imageQualityDegradationQuotationMode: str
    processingDate: str
    processingLevel: str
    productType: str
    status: str
    beginPosition: str
    endPosition: str
    platformShortName: str
    instrumentShortName: str
    sensorType: str
    operationalMode: str
    resolution: str
    orbitNumber: str
    lastOrbitNumber: str
    dayNight: str
    illuminationAzimuthAngle: str
    illuminationElevationAngle: str
    multiExtentOf: list[float]
    centerOf: tuple[float]
    product: GPortalProduct
    previews: list[GPortalPreview]
    meta: GPortalMeta

    def __init__(self, response) -> None:
        """
        parser for GPortal properties response
        
        :response dict the json dictionary of the response
        """
        self.identifier = str(response["identifier"])
        self.acquisitionType = str(response["acquisitionType"])
        self.imageQualityDegradation = str(response["imageQualityDegradation"])
        self.imageQualityDegradationQuotationMode = str(
            response["imageQualityDegradationQuotationMode"])
        self.processingDate = str(response["processingDate"])
        self.processingLevel = str(response["processingLevel"])
        self.productType = str(response["ProductType"])
        self.status = str(response["status"])
        self.beginPosition = str(response["beginPosition"])
        self.endPosition = str(response["endPosition"])
        self.platformShortName = str(response["platformShortName"])
        self.instrumentShortName = str(response["instrumentShortName"])
        self.sensorType = str(response["sensorType"])
        self.operationalMode = str(response["operationalMode"])
        self.resolution = str(response["resolution"])
        self.orbitNumber = str(response["orbitNumber"])
        self.lastOrbitNumber = str(response["lastOrbitNumber"])
        self.dayNight = str(response["DayNight"])
        self.illuminationAzimuthAngle = str(
            response["illuminationAzimuthAngle"])
        self.illuminationElevationAngle = str(
            response["illuminationElevationAngle"])
        self.multiExtentOf = [float(part)
                              for part in response["multiExtentOf"].split(" ")]
        self.centerOf = tuple([float(part)
                              for part in response["centerOf"].split(" ")])
        self.product = GPortalProduct(response["product"])
        self.previews = [GPortalPreview(prev) for prev in response["browse"]]
        self.meta = GPortalMeta(response["gpp"])

    def to_json(self) -> dict:
        return {
            "identifier": self.identifier,
            "acquisitionType": self.acquisitionType,
            "imageQualityDegradation": self.imageQualityDegradation,
            "imageQualityDegradationQuotationMode": self.imageQualityDegradationQuotationMode,
            "processingDate": self.processingDate,
            "processingLevel": self.processingLevel,
            "productType": self.productType,
            "status": self.status,
            "beginPosition": self.beginPosition,
            "endPosition": self.endPosition,
            "platformShortName": self.platformShortName,
            "instrumentShortName": self.instrumentShortName,
            "sensorType": self.sensorType,
            "operationalMode": self.operationalMode,
            "resolution": self.resolution,
            "orbitNumber": self.orbitNumber,
            "lastOrbitNumber": self.lastOrbitNumber,
            "dayNight": self.dayNight,
            "illuminationAzimuthAngle": self.illuminationAzimuthAngle,
            "illuminationElevationAngle": self.illuminationElevationAngle,
            "multiExtentOf": self.multiExtentOf,
            "centerOf": list(self.centerOf),
            "product": self.product.to_json(),
            "previews": [p.to_json() for p in self.previews],
            "meta": self.meta.to_json()
        }
