# app/models/raw_data.py
from pydantic import BaseModel, Field
from typing import Optional

class RawDataType1(BaseModel):
    ID: str
    STATUS: str
    STATUS_DATA: str

class RawDataType2(BaseModel):
    ID: str
    RESULT_ID: str
    RESULT_DESCRIPTION: str
    CAPTURE_TIME: str
    STATUS: str

class RawDataType3(BaseModel):
    ID: str
    DATA_DETECCAO: str = Field(..., alias="DATA.DETECCAO")  
    PONTO: str
    LOC_ID: int
    LOC: str
    POS_ID: int
    POS: str
    TYPE_ID: int
    TYPE_TEXT: str
    VIEW_ID: Optional[float]
    COLUNA: str
    LINHA: Optional[int]

class RawDataType4(BaseModel):
    ID: str
    MODELL: str
    FARBAU: str
    FARBIN: str
    ZIEL_LAND: str
    PR: str
