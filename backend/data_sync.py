"""
AKShare 数据同步模块 - 接入全量科技板块股票数据
"""
import akshare as ak
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Stock, StockQuote, FinancialIndicator
from datetime import datetime, date
import time

# 科技板块相关概念/行业映射
TECH_SECTORS = {
    "半导体": "semiconductor",
    "芯片": "semiconductor",
    "集成电路": "semiconductor",
    "人工智能": "ai",
    "AI": "ai",
    "新能源": "new_energy",
    "光伏": "new_energy",
    "锂电池": "new_energy",
    "储能": "new_energy",
    "云计算": "cloud_computing",
    "大数据": "cloud_computing",
    "软件": "cloud_computing",
    "5G": "communication",
    "通信": "communication",
    "消费电子": "consumer_electronics"
}

def classify_sector(industry_name, concept_names=""):
    """根据行业/概念分类到科技板块"""
    text = (industry_name or "") + " " + (concept_names or "")
    text = text.lower()
    
    for cn_key, en_value in TECH_SECTORS.items():
        if cn_key in text:
            return en_value
    return "other"

def sync_stock_list(db: Session):
    """同步A股股票列表"""
    print("正在获取A股股票列表...")
    
    try:
        # 获取所有A股
        stock_df = ak.stock_zh_a_spot_em()
        print(f"获取到 {len(stock_df)} 只股票")
        
        # 获取行业信息
        try:
            industry_df = ak.stock_sector_spot()
            industry_map = {}
            for _, row in industry_df.iterrows():
                code = row.get('代码', '')
                industry = row.get('行业', '')
                if code:
                    industry_map[code] = industry
        except:
            industry_map = {}
        
        count = 0
        for _, row in stock_df.iterrows():
            symbol = row.get('代码', '')
            name = row.get('名称', '')
            
            if not symbol or not name:
                continue
            
            # 判断市场
            if symbol.startswith('6'):
                market = 'sh'
                full_symbol = f"{symbol}.SH"
            elif symbol.startswith('0') or symbol.startswith('3'):
                market = 'sz'
                full_symbol = f"{symbol}.SZ"
            elif symbol.startswith('8') or symbol.startswith('4'):
                market = 'bj'
                full_symbol = f"{symbol}.BJ"
            else:
                continue
            
            # 获取行业并分类
            industry = industry_map.get(symbol, '')
            sector = classify_sector(industry)
            
            # 只保留科技板块
            if sector == "other":
                continue
            
            # 检查是否已存在
            existing = db.query(Stock).filter(Stock.symbol == full_symbol).first()
            if existing:
                # 更新行情
                update_quote(db, existing, row)
            else:
                # 创建新股票
                stock = Stock(
                    symbol=full_symbol,
                    name=name,
                    market=market,
                    sector=sector,
                    sub_sector=industry,
                    total_shares=int(row.get('总市值', 0) / row.get('最新价', 1)) if row.get('最新价', 0) > 0 else None,
                    is_active=True
                )
                db.add(stock)
                
                # 创建行情
                create_quote(db, stock, row)
                count += 1
        
        db.commit()
        print(f"新增 {count} 只科技板块股票")
        return count
        
    except Exception as e:
        print(f"同步失败: {e}")
        db.rollback()
        return 0

def update_quote(db: Session, stock: Stock, row):
    """更新股票行情"""
    quote = db.query(StockQuote).filter(StockQuote.symbol == stock.symbol).first()
    
    price = float(row.get('最新价', 0) or 0)
    prev_close = float(row.get('昨收', 0) or 0)
    change = price - prev_close if prev_close > 0 else 0
    change_pct = (change / prev_close * 100) if prev_close > 0 else 0
    
    if quote:
        quote.current_price = price
        quote.prev_close = prev_close
        quote.change_amount = round(change, 2)
        quote.change_percent = round(change_pct, 2)
        quote.open_price = float(row.get('今开', 0) or 0)
        quote.high_price = float(row.get('最高', 0) or 0)
        quote.low_price = float(row.get('最低', 0) or 0)
        quote.volume = int(row.get('成交量', 0) or 0)
        quote.turnover = float(row.get('成交额', 0) or 0)
        quote.update_time = datetime.now()
    else:
        quote = StockQuote(
            symbol=stock.symbol,
            current_price=price,
            prev_close=prev_close,
            change_amount=round(change, 2),
            change_percent=round(change_pct, 2),
            open_price=float(row.get('今开', 0) or 0),
            high_price=float(row.get('最高', 0) or 0),
            low_price=float(row.get('最低', 0) or 0),
            volume=int(row.get('成交量', 0) or 0),
            turnover=float(row.get('成交额', 0) or 0),
            update_time=datetime.now()
        )
        db.add(quote)

def create_quote(db: Session, stock: Stock, row):
    """创建股票行情"""
    price = float(row.get('最新价', 0) or 0)
    prev_close = float(row.get('昨收', 0) or 0)
    change = price - prev_close if prev_close > 0 else 0
    change_pct = (change / prev_close * 100) if prev_close > 0 else 0
    
    quote = StockQuote(
        symbol=stock.symbol,
        current_price=price,
        prev_close=prev_close,
        change_amount=round(change, 2),
        change_percent=round(change_pct, 2),
        open_price=float(row.get('今开', 0) or 0),
        high_price=float(row.get('最高', 0) or 0),
        low_price=float(row.get('最低', 0) or 0),
        volume=int(row.get('成交量', 0) or 0),
        turnover=float(row.get('成交额', 0) or 0),
        update_time=datetime.now()
    )
    db.add(quote)

def sync_financial_data(db: Session, symbol: str = None):
    """同步财务数据"""
    print("正在同步财务数据...")
    
    try:
        # 获取财务指标
        if symbol:
            stocks = db.query(Stock).filter(Stock.symbol == symbol).all()
        else:
            stocks = db.query(Stock).limit(100).all()
        
        for stock in stocks:
            try:
                # 获取个股财务指标
                code = stock.symbol.split('.')[0]
                market = "sh" if stock.market == "sh" else "sz"
                
                # 获取主要指标
                df = ak.stock_financial_analysis_indicator(symbol=code)
                if df.empty:
                    continue
                
                latest = df.iloc[0]
                
                indicator = FinancialIndicator(
                    symbol=stock.symbol,
                    report_date=date.today(),
                    pe_ttm=float(latest.get('市盈率', 0) or 0),
                    pb=float(latest.get('市净率', 0) or 0),
                    roe=float(latest.get('净资产收益率', 0) or 0),
                    gross_margin=float(latest.get('毛利率', 0) or 0),
                    revenue_growth_3y=float(latest.get('营收增长率', 0) or 0),
                    debt_to_equity=float(latest.get('资产负债率', 0) or 0) / 100 if latest.get('资产负债率') else None
                )
                db.add(indicator)
                time.sleep(0.5)  # 避免请求过快
                
            except Exception as e:
                print(f"同步 {stock.symbol} 财务数据失败: {e}")
                continue
        
        db.commit()
        print("财务数据同步完成")
        
    except Exception as e:
        print(f"财务数据同步失败: {e}")
        db.rollback()

def run_full_sync():
    """执行全量同步"""
    db = SessionLocal()
    try:
        print("=" * 50)
        print("开始数据同步...")
        print("=" * 50)
        
        # 同步股票列表
        count = sync_stock_list(db)
        print(f"股票列表同步完成，新增 {count} 只股票")
        
        # 同步财务数据（只同步前50只，避免太慢）
        sync_financial_data(db)
        
        print("=" * 50)
        print("数据同步全部完成！")
        print("=" * 50)
        
    finally:
        db.close()

if __name__ == "__main__":
    run_full_sync()
