"""
TechInsight Pro - 数据模型
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Stock(Base):
    """股票基础信息"""
    __tablename__ = "stocks"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    name_en = Column(String(200))
    market = Column(String(10))
    sector = Column(String(50))
    sub_sector = Column(String(100))
    industry_chain = Column(JSON)
    company_profile = Column(Text)
    website = Column(String(200))
    founded_date = Column(Date)
    listing_date = Column(Date)
    total_shares = Column(Float)
    float_shares = Column(Float)
    is_active = Column(Boolean, default=True)
    is_hot = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    quote = relationship("StockQuote", back_populates="stock", uselist=False)
    indicators = relationship("FinancialIndicator", back_populates="stock")

class StockQuote(Base):
    """股票实时行情"""
    __tablename__ = "stock_quotes"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), unique=True, index=True, nullable=False)
    current_price = Column(Float)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    prev_close = Column(Float)
    change_amount = Column(Float)
    change_percent = Column(Float)
    volume = Column(Float)
    turnover = Column(Float)
    update_time = Column(DateTime, default=func.now())
    
    stock = relationship("Stock", back_populates="quote")

class FinancialIndicator(Base):
    """财务指标"""
    __tablename__ = "financial_indicators"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), index=True, nullable=False)
    report_date = Column(Date)
    
    # 估值指标
    pe_ttm = Column(Float)
    pb = Column(Float)
    ps_ttm = Column(Float)
    ev_ebitda = Column(Float)
    pcf = Column(Float)
    
    # 盈利能力
    roe = Column(Float)
    roa = Column(Float)
    gross_margin = Column(Float)
    net_margin = Column(Float)
    operating_margin = Column(Float)
    
    # 成长性
    revenue_growth_3y = Column(Float)
    profit_growth_3y = Column(Float)
    revenue_growth_5y = Column(Float)
    profit_growth_5y = Column(Float)
    
    # 财务健康
    current_ratio = Column(Float)
    quick_ratio = Column(Float)
    debt_to_equity = Column(Float)
    interest_coverage = Column(Float)
    
    stock = relationship("Stock", back_populates="indicators")

class AnalystFramework(Base):
    """博主分析框架"""
    __tablename__ = "analyst_frameworks"
    
    id = Column(Integer, primary_key=True, index=True)
    analyst_name = Column(String(100), nullable=False)
    analyst_id = Column(String(50), unique=True, nullable=False)
    platform = Column(String(50))
    profile_url = Column(String(500))
    avatar_url = Column(String(500))
    focus_sectors = Column(JSON)
    style_tags = Column(JSON)
    selection_criteria = Column(JSON)
    decision_process = Column(JSON)
    key_metrics = Column(JSON)
    risk_rules = Column(JSON)
    avoid_patterns = Column(JSON)
    style_summary = Column(Text)
    total_judgments = Column(Integer, default=0)
    correct_judgments = Column(Integer, default=0)
    hit_rate = Column(Float)
    avg_hold_period = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class AnalystJudgment(Base):
    """博主历史判断"""
    __tablename__ = "analyst_judgments"
    
    id = Column(Integer, primary_key=True, index=True)
    analyst_id = Column(String(50), index=True, nullable=False)
    symbol = Column(String(20), index=True, nullable=False)
    judgment_date = Column(DateTime, nullable=False)
    judgment_type = Column(String(20))
    target_price = Column(Float)
    time_horizon = Column(String(20))
    core_logic = Column(Text)
    key_factors = Column(JSON)
    is_correct = Column(Boolean)
    return_rate = Column(Float)

class SimulatedAnalysis(Base):
    """模拟分析结果"""
    __tablename__ = "simulated_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    analyst_id = Column(String(50), index=True, nullable=False)
    symbol = Column(String(20), index=True, nullable=False)
    analysis_date = Column(DateTime, nullable=False)
    simulated_judgment = Column(String(20))
    confidence_score = Column(Float)
    style_similarity = Column(String(20))
    analysis_steps = Column(JSON)
    key_findings = Column(JSON)
    risk_warnings = Column(JSON)
    full_report = Column(Text)
    divergence_from_consensus = Column(Text)
