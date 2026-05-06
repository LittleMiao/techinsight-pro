from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Text, Boolean, ForeignKey, JSON, BigInteger
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Stock(Base):
    """股票基础信息表"""
    __tablename__ = "stocks"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    name_en = Column(String(100))
    market = Column(String(10), nullable=False)
    sector = Column(String(50), nullable=False)
    sub_sector = Column(String(100))
    industry_chain = Column(String(20))
    company_profile = Column(Text)
    website = Column(String(200))
    founded_date = Column(Date)
    listing_date = Column(Date)
    total_shares = Column(BigInteger)
    float_shares = Column(BigInteger)
    is_active = Column(Boolean, default=True)
    is_hot = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    prices = relationship("StockPrice", back_populates="stock")
    quote = relationship("StockQuote", back_populates="stock", uselist=False)
    financials = relationship("FinancialStatement", back_populates="stock")
    indicators = relationship("FinancialIndicator", back_populates="stock")
    sentiments = relationship("SentimentIndicator", back_populates="stock")
    ai_analyses = relationship("AIAnalysis", back_populates="stock")

class StockPrice(Base):
    """历史行情数据表"""
    __tablename__ = "stock_prices"
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(20), ForeignKey("stocks.symbol"), nullable=False)
    trade_date = Column(Date, nullable=False)
    period = Column(String(10), nullable=False)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(BigInteger)
    turnover = Column(Float)
    adj_close = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    
    stock = relationship("Stock", back_populates="prices")

class StockQuote(Base):
    """实时行情表"""
    __tablename__ = "stock_quotes"
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(20), ForeignKey("stocks.symbol"), unique=True, nullable=False)
    current_price = Column(Float)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    prev_close = Column(Float)
    change_amount = Column(Float)
    change_percent = Column(Float)
    volume = Column(BigInteger)
    turnover = Column(Float)
    bid_price = Column(Float)
    ask_price = Column(Float)
    bid_volume = Column(Integer)
    ask_volume = Column(Integer)
    update_time = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    stock = relationship("Stock", back_populates="quote")

class FinancialStatement(Base):
    """财务报表表"""
    __tablename__ = "financial_statements"
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(20), ForeignKey("stocks.symbol"), nullable=False)
    report_type = Column(String(20), nullable=False)
    report_period = Column(String(10), nullable=False)
    report_date = Column(Date, nullable=False)
    revenue = Column(Float)
    revenue_yoy = Column(Float)
    gross_profit = Column(Float)
    operating_profit = Column(Float)
    net_profit = Column(Float)
    net_profit_yoy = Column(Float)
    eps = Column(Float)
    rd_expense = Column(Float)
    total_assets = Column(Float)
    total_liabilities = Column(Float)
    shareholders_equity = Column(Float)
    operating_cash_flow = Column(Float)
    free_cash_flow = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    
    stock = relationship("Stock", back_populates="financials")

class FinancialIndicator(Base):
    """财务指标表"""
    __tablename__ = "financial_indicators"
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(20), ForeignKey("stocks.symbol"), nullable=False)
    report_date = Column(Date, nullable=False)
    pe_ttm = Column(Float)
    pb = Column(Float)
    ps_ttm = Column(Float)
    roe = Column(Float)
    roa = Column(Float)
    gross_margin = Column(Float)
    net_margin = Column(Float)
    revenue_growth_3y = Column(Float)
    profit_growth_3y = Column(Float)
    current_ratio = Column(Float)
    debt_to_equity = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    
    stock = relationship("Stock", back_populates="indicators")

class SentimentIndicator(Base):
    """情绪指标表"""
    __tablename__ = "sentiment_indicators"
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(20), ForeignKey("stocks.symbol"), nullable=False)
    calc_date = Column(Date, nullable=False)
    overall_score = Column(Float)
    overall_sentiment = Column(String(20))
    news_score = Column(Float)
    social_score = Column(Float)
    analyst_score = Column(Float)
    institutional_score = Column(Float)
    trend_direction = Column(String(20))
    created_at = Column(DateTime, default=datetime.now)
    
    stock = relationship("Stock", back_populates="sentiments")

class AIAnalysis(Base):
    """AI分析结果表"""
    __tablename__ = "ai_analysis"
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(20), ForeignKey("stocks.symbol"), nullable=False)
    analysis_date = Column(Date, nullable=False)
    key_highlights = Column(JSON)
    key_risks = Column(JSON)
    short_term_rating = Column(String(20))
    short_term_target_low = Column(Float)
    short_term_target_high = Column(Float)
    short_term_factors = Column(JSON)
    medium_term_rating = Column(String(20))
    medium_term_target_low = Column(Float)
    medium_term_target_high = Column(Float)
    medium_term_factors = Column(JSON)
    long_term_rating = Column(String(20))
    long_term_target_low = Column(Float)
    long_term_target_high = Column(Float)
    long_term_factors = Column(JSON)
    full_analysis = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    
    stock = relationship("Stock", back_populates="ai_analyses")

class News(Base):
    """新闻表"""
    __tablename__ = "news"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    content = Column(Text)
    summary = Column(Text)
    source = Column(String(100))
    source_url = Column(String(500))
    publish_time = Column(DateTime, nullable=False)
    category = Column(String(50))
    sentiment = Column(String(20))
    sentiment_score = Column(Float)
    related_symbols = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)

class SupplyChain(Base):
    """供应链关系表"""
    __tablename__ = "supply_chain"
    
    id = Column(Integer, primary_key=True)
    company_symbol = Column(String(20), ForeignKey("stocks.symbol"), nullable=False)
    partner_symbol = Column(String(20), ForeignKey("stocks.symbol"), nullable=False)
    relationship_type = Column(String(20), nullable=False)
    relationship_desc = Column(String(100))
    revenue_ratio = Column(Float)
    supply_ratio = Column(Float)
    importance_level = Column(String(10))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)

# ==================== 博主风格蒸馏相关表 ====================

class AnalystFramework(Base):
    """博主分析框架表"""
    __tablename__ = "analyst_frameworks"
    
    id = Column(Integer, primary_key=True)
    analyst_name = Column(String(100), nullable=False)
    analyst_id = Column(String(50), unique=True, nullable=False)
    platform = Column(String(50))
    profile_url = Column(String(500))
    avatar_url = Column(String(500))
    focus_sectors = Column(JSON)
    
    # 蒸馏出的核心框架
    selection_criteria = Column(JSON)
    decision_process = Column(JSON)
    key_metrics = Column(JSON)
    risk_rules = Column(JSON)
    avoid_patterns = Column(JSON)
    style_summary = Column(Text)
    
    # 统计数据
    total_judgments = Column(Integer, default=0)
    correct_judgments = Column(Integer, default=0)
    hit_rate = Column(Float)
    avg_hold_period = Column(String(20))
    style_tags = Column(JSON)
    
    # 元数据
    data_start_date = Column(Date)
    data_end_date = Column(Date)
    last_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    
    judgments = relationship("AnalystJudgment", back_populates="analyst")
    simulations = relationship("SimulatedAnalysis", back_populates="analyst")

class AnalystJudgment(Base):
    """博主历史判断表"""
    __tablename__ = "analyst_judgments"
    
    id = Column(Integer, primary_key=True)
    analyst_id = Column(String(50), ForeignKey("analyst_frameworks.analyst_id"), nullable=False)
    symbol = Column(String(20), nullable=False)
    judgment_date = Column(Date, nullable=False)
    judgment_type = Column(String(20), nullable=False)
    target_price = Column(Float)
    time_horizon = Column(String(20))
    
    core_logic = Column(Text)
    key_factors = Column(JSON)
    risk_factors = Column(JSON)
    data_source_url = Column(String(500))
    data_source_title = Column(String(500))
    
    actual_price_at_judgment = Column(Float)
    actual_price_after_period = Column(Float)
    is_correct = Column(Boolean)
    return_rate = Column(Float)
    
    created_at = Column(DateTime, default=datetime.now)
    
    analyst = relationship("AnalystFramework", back_populates="judgments")

class SimulatedAnalysis(Base):
    """模拟分析结果表"""
    __tablename__ = "simulated_analyses"
    
    id = Column(Integer, primary_key=True)
    analyst_id = Column(String(50), ForeignKey("analyst_frameworks.analyst_id"), nullable=False)
    symbol = Column(String(20), nullable=False)
    analysis_date = Column(DateTime, nullable=False)
    
    simulated_judgment = Column(String(20))
    confidence_score = Column(Float)
    style_similarity = Column(String(20))
    
    analysis_steps = Column(JSON)
    key_findings = Column(JSON)
    risk_warnings = Column(JSON)
    divergence_from_consensus = Column(Text)
    
    full_report = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    
    analyst = relationship("AnalystFramework", back_populates="simulations")
