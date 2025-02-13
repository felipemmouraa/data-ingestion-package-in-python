# app/models/transformed_data.py
from pydantic import BaseModel
from typing import Optional

class TransformedDataType1(BaseModel):
    id: str
    status: str
    status_data: str
    ingested_at: str  # timestamp of when data was ingested

class TransformedDataType2(BaseModel):
    id: str
    result_id: str
    result_description: str
    capture_time: str
    status: str
    ingested_at: str

class TransformedDataType3(BaseModel):
    id: str
    data_deteccao: str
    ponto: str
    loc_id: int
    loc: str
    pos_id: int
    pos: str
    type_id: int
    type_text: str
    view_id: Optional[float]
    coluna: str
    linha: Optional[int]
    ingested_at: str

class TransformedDataType4(BaseModel):
    id: str
    modell: str
    farbau: str
    farbin: str
    ziel_land: str
    pr: str
    ingested_at: str
