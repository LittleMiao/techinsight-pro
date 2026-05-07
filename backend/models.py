"""
TechInsight Pro - 数据模型
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, Text, JSON, ForeignKey
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
    
    quote = relationship("StockQuote", back_populates="stock", uselist=False,
                         foreign_keys="StockQuote.symbol", primaryjoin="Stock.symbol == StockQuote.symbol")
    indicators = relationship("FinancialIndicator", back_populates="stock",
                              foreign_keys="FinancialIndicator.symbol", primaryjoin="Stock.symbol == FinancialIndicator.symbol")

class StockQuote(Base):
    """股票实时行情"""
    __tablename__ = "stock_quotes"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), ForeignKey("stocks.symbol"), unique=True, index=True, nullable=False)
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
    symbol = Column(String(20), ForeignKey("stocks.symbol"), index=True, nullable=False)
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

class HistoricalIndicator(Base):
    """历史财务指标（模拟）"""
    __tablename__ = "historical_indicators"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), ForeignKey("stocks.symbol"), index=True, nullable=False)
    report_date = Column(Date, index=True)
    
    pe_ttm = Column(Float)
    pb = Column(Float)
    ps_ttm = Column(Float)
    roe = Column(Float)
    roa = Column(Float)
    gross_margin = Column(Float)
    net_margin = Column(Float)
    operating_margin = Column(Float)
    revenue_growth_3y = Column(Float)
    profit_growth_3y = Column(Float)
    debt_to_equity = Column(Float)
    current_ratio = Column(Float)

class InformationSource(Base):
    """信息源"""
    __tablename__ = "information_sources"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), ForeignKey("stocks.symbol"), index=True, nullable=False)
    source_type = Column(String(30), index=True)  # report/research/news/analyst_opinion
    title = Column(String(500), nullable=False)
    source = Column(String(200))  # 来源：中信证券、东方财富等
    publish_time = Column(DateTime, nullable=False)
    summary = Column(Text)
    sentiment = Column(String(20))  # positive/negative/neutral
    url = Column(String(1000))
    created_at = Column(DateTime, default=func.now())
