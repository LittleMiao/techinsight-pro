"""
TechInsight Pro - 股票深度研究平台后端API
包含博主风格蒸馏模块
"""
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date

from database import engine, Base, get_db
from models import *
from schemas import *
from analyst_service import AnalystService, SimulationService, StockService, ReferenceService
from init_data import init_database

# 创建表
Base.metadata.create_all(bind=engine)

# 初始化数据
init_database()

app = FastAPI(
    title="TechInsight Pro API",
    description="科技板块股票深度研究平台 - 含博主风格蒸馏模块",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== 博主框架管理API ====================

@app.get("/api/v1/analysts", response_model=AnalystListResponse)
def get_analysts(
    is_active: bool = True,
    db: Session = Depends(get_db)
):
    """获取博主列表"""
    data = AnalystService.get_analysts(db, is_active)
    return AnalystListResponse(data=data)


@app.get("/api/v1/analysts/{analyst_id}", response_model=AnalystDetailResponse)
def get_analyst(analyst_id: str, db: Session = Depends(get_db)):
    """获取博主详情"""
    data = AnalystService.get_analyst(db, analyst_id)
    if not data:
        raise HTTPException(status_code=404, detail="博主不存在")
    return AnalystDetailResponse(data=data)


@app.post("/api/v1/analysts", response_model=AnalystDetailResponse)
def create_analyst(
    analyst_data: AnalystFrameworkCreate,
    db: Session = Depends(get_db)
):
    """创建博主框架"""
    analyst = AnalystService.create_analyst(db, analyst_data)
    data = AnalystService.get_analyst(db, analyst.analyst_id)
    return AnalystDetailResponse(data=data)


@app.get("/api/v1/analysts/{analyst_id}/judgments")
def get_analyst_judgments(
    analyst_id: str,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取博主历史判断"""
    data = AnalystService.get_judgments(db, analyst_id, limit)
    return {"code": 200, "data": data}


# ==================== 模拟分析API ====================

@app.post("/api/v1/analysts/{analyst_id}/simulate", response_model=SimulatedAnalysisAPIResponse)
def simulate_analysis(
    analyst_id: str,
    request: SimulatedAnalysisRequest,
    db: Session = Depends(get_db)
):
    """执行模拟分析"""
    data = SimulationService.simulate_analysis(db, analyst_id, request.symbol)
    if not data:
        raise HTTPException(status_code=404, detail="博主或股票不存在")
    return SimulatedAnalysisAPIResponse(data=data)


@app.get("/api/v1/stocks/{symbol}/analyst-views")
def get_stock_analyst_views(
    symbol: str,
    db: Session = Depends(get_db)
):
    """获取所有博主对某股票的模拟观点"""
    analysts = db.query(AnalystFramework).filter(
        AnalystFramework.is_active == True
    ).limit(5).all()

    views = []
    for analyst in analysts:
        # 获取最新的模拟分析
        latest = db.query(SimulatedAnalysis).filter(
            SimulatedAnalysis.analyst_id == analyst.analyst_id,
            SimulatedAnalysis.symbol == symbol
        ).order_by(SimulatedAnalysis.analysis_date.desc()).first()

        if latest:
            views.append({
                "analyst_name": analyst.analyst_name,
                "analyst_id": analyst.analyst_id,
                "judgment": latest.simulated_judgment,
                "confidence": latest.confidence_score,
                "similarity": latest.style_similarity,
                "date": latest.analysis_date
            })

    return {"code": 200, "data": {"symbol": symbol, "views": views}}


# ==================== 股票相关API ====================

@app.get("/api/v1/stocks", response_model=StockListResponse)
def get_stocks(
    sector: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取股票列表"""
    data = StockService.get_stocks(db, sector, page, page_size)
    return StockListResponse(data=data)


@app.get("/api/v1/stocks/{symbol}", response_model=StockDetailResponse)
def get_stock_detail(symbol: str, db: Session = Depends(get_db)):
    """获取股票详情"""
    data = StockService.get_stock_detail(db, symbol)
    if not data:
        raise HTTPException(status_code=404, detail="股票不存在")
    return StockDetailResponse(data=data)


# ==================== 参考数据API ====================

@app.get("/api/v1/stocks/{symbol}/sector-comparison")
def get_sector_comparison(symbol: str, db: Session = Depends(get_db)):
    """获取股票行业板块对比数据"""
    data = ReferenceService.get_sector_comparison(db, symbol)
    if not data:
        raise HTTPException(status_code=404, detail="股票不存在")
    return {"code": 200, "data": data}


@app.get("/api/v1/stocks/{symbol}/peers")
def get_peers(symbol: str, db: Session = Depends(get_db)):
    """获取同细分行业同行对比"""
    data = ReferenceService.get_peers(db, symbol)
    if not data:
        raise HTTPException(status_code=404, detail="股票不存在")
    return {"code": 200, "data": data}


@app.get("/api/v1/stocks/{symbol}/history-trend")
def get_history_trend(symbol: str, db: Session = Depends(get_db)):
    """获取历史指标趋势"""
    data = ReferenceService.get_history_trend(db, symbol)
    if not data:
        raise HTTPException(status_code=404, detail="股票不存在")
    return {"code": 200, "data": data}


@app.get("/api/v1/stocks/{symbol}/sources")
def get_sources(symbol: str, source_type: Optional[str] = None, page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    """获取信息源列表"""
    data = ReferenceService.get_sources(db, symbol, source_type, page, page_size)
    return {"code": 200, "data": data}


# ==================== 健康检查 ====================

@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "ok", "service": "TechInsight Pro API"}


@app.get("/")
def root():
    """根路径"""
    return {
        "name": "TechInsight Pro API",
        "version": "1.0.0",
        "features": ["股票分析", "博主风格蒸馏", "模拟分析"],
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
