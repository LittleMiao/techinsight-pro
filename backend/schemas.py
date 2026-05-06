from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date

# ==================== 博主相关 ====================

class AnalystFrameworkBase(BaseModel):
    analyst_name: str
    analyst_id: str
    platform: Optional[str] = None
    profile_url: Optional[str] = None
    focus_sectors: Optional[List[str]] = None
    style_tags: Optional[List[str]] = None

class AnalystFrameworkCreate(AnalystFrameworkBase):
    selection_criteria: Optional[List[Dict]] = None
    decision_process: Optional[List[Dict]] = None
    key_metrics: Optional[List[Dict]] = None
    risk_rules: Optional[List[Dict]] = None
    avoid_patterns: Optional[List[str]] = None
    style_summary: Optional[str] = None

class AnalystFrameworkResponse(AnalystFrameworkBase):
    id: int
    avatar_url: Optional[str] = None
    selection_criteria: Optional[List[Dict]] = None
    decision_process: Optional[List[Dict]] = None
    key_metrics: Optional[List[Dict]] = None
    risk_rules: Optional[List[Dict]] = None
    avoid_patterns: Optional[List[str]] = None
    style_summary: Optional[str] = None
    total_judgments: int = 0
    correct_judgments: int = 0
    hit_rate: Optional[float] = None
    avg_hold_period: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    
    class Config:
        from_attributes = True

class AnalystListResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Dict[str, Any]

class AnalystDetailResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: AnalystFrameworkResponse

# ==================== 模拟分析相关 ====================

class AnalysisStep(BaseModel):
    step: str
    result: str
    detail: str

class SimulatedAnalysisRequest(BaseModel):
    symbol: str
    include_details: bool = True

class SimulatedAnalysisResponse(BaseModel):
    analyst_name: str
    analyst_id: str
    symbol: str
    analysis_date: datetime
    simulated_judgment: str
    confidence_score: float
    style_similarity: str
    steps: List[AnalysisStep]
    key_findings: List[str]
    risk_warnings: List[str]
    divergence_from_consensus: Optional[str] = None
    report: str

class SimulatedAnalysisAPIResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: SimulatedAnalysisResponse

# ==================== 股票相关 ====================

class StockBase(BaseModel):
    symbol: str
    name: str
    market: str
    sector: str

class StockResponse(StockBase):
    id: int
    sub_sector: Optional[str] = None
    market_cap: Optional[float] = None
    price: Optional[float] = None
    change_percent: Optional[float] = None
    pe_ttm: Optional[float] = None
    pb: Optional[float] = None
    is_hot: bool = False
    
    class Config:
        from_attributes = True

class StockListResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Dict[str, Any]

class StockDetailResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Dict[str, Any]

# ==================== 通用响应 ====================

class ResponseBase(BaseModel):
    code: int = 200
    message: str = "success"
    timestamp: datetime = Field(default_factory=datetime.now)
