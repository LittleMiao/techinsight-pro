from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class AnalystFrameworkCreate(BaseModel):
    analyst_name: str
    analyst_id: str
    platform: str
    profile_url: Optional[str] = None
    focus_sectors: List[str]
    style_tags: List[str]
    selection_criteria: List[Dict[str, Any]]
    decision_process: List[Dict[str, Any]]
    key_metrics: List[Dict[str, Any]]
    risk_rules: List[Dict[str, Any]]
    avoid_patterns: List[str]
    style_summary: str

class AnalystListResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Dict[str, Any]

class AnalystDetailResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Dict[str, Any]

class SimulatedAnalysisRequest(BaseModel):
    symbol: str

class SimulatedAnalysisAPIResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Dict[str, Any]

class StockListResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Dict[str, Any]

class StockDetailResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Dict[str, Any]
