"""
初始化数据库数据 - 包含博主框架示例
"""
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import *
from datetime import datetime, date, timedelta
import random

def init_database():
    """初始化数据库"""
    db = SessionLocal()
    try:
        # 检查是否已有数据
        if db.query(Stock).first():
            print("数据库已有数据，跳过初始化")
            return
        
        print("开始初始化数据库...")
        
        # 1. 创建股票基础数据
        stocks_data = [
            {"symbol": "688981.SH", "name": "中芯国际", "market": "sh", "sector": "semiconductor", "sub_sector": "晶圆代工", "total_shares": 7900000000, "is_hot": True},
            {"symbol": "002371.SZ", "name": "北方华创", "market": "sz", "sector": "semiconductor", "sub_sector": "半导体设备", "total_shares": 530000000, "is_hot": True},
            {"symbol": "603501.SH", "name": "韦尔股份", "market": "sh", "sector": "semiconductor", "sub_sector": "芯片设计", "total_shares": 1200000000},
            {"symbol": "688256.SH", "name": "寒武纪", "market": "sh", "sector": "ai", "sub_sector": "AI芯片", "total_shares": 416000000, "is_hot": True},
            {"symbol": "002230.SZ", "name": "科大讯飞", "market": "sz", "sector": "ai", "sub_sector": "语音识别", "total_shares": 2300000000},
            {"symbol": "300750.SZ", "name": "宁德时代", "market": "sz", "sector": "new_energy", "sub_sector": "动力电池", "total_shares": 4400000000, "is_hot": True},
            {"symbol": "002594.SZ", "name": "比亚迪", "market": "sz", "sector": "new_energy", "sub_sector": "新能源汽车", "total_shares": 2900000000, "is_hot": True},
            {"symbol": "601012.SH", "name": "隆基绿能", "market": "sh", "sector": "new_energy", "sub_sector": "光伏", "total_shares": 7500000000},
            {"symbol": "688111.SH", "name": "金山办公", "market": "sh", "sector": "cloud_computing", "sub_sector": "办公软件", "total_shares": 461000000},
            {"symbol": "300454.SZ", "name": "深信服", "market": "sz", "sector": "cloud_computing", "sub_sector": "网络安全", "total_shares": 419000000},
        ]
        
        for data in stocks_data:
            stock = Stock(**data)
            db.add(stock)
        db.commit()
        print("创建了股票数据")
        
        # 2. 创建实时行情
        base_prices = {
            "688981.SH": 58.20, "002371.SZ": 245.0, "603501.SH": 85.50,
            "688256.SH": 185.40, "002230.SZ": 42.80, "300750.SZ": 185.60,
            "002594.SZ": 268.50, "601012.SH": 18.20, "688111.SH": 285.30,
            "300454.SZ": 58.90
        }
        
        for symbol, base_price in base_prices.items():
            change = random.uniform(-5, 5)
            quote = StockQuote(
                symbol=symbol,
                current_price=round(base_price + change, 2),
                open_price=round(base_price + random.uniform(-2, 2), 2),
                high_price=round(base_price + random.uniform(0, 8), 2),
                low_price=round(base_price - random.uniform(0, 8), 2),
                prev_close=base_price,
                change_amount=round(change, 2),
                change_percent=round(change / base_price * 100, 2),
                volume=random.randint(1000000, 50000000),
                turnover=random.randint(100000000, 5000000000),
                update_time=datetime.now()
            )
            db.add(quote)
        db.commit()
        print("创建了行情数据")
        
        # 3. 创建财务指标
        for symbol in base_prices.keys():
            indicator = FinancialIndicator(
                symbol=symbol,
                report_date=date(2024, 12, 31),
                pe_ttm=round(random.uniform(20, 80), 2),
                pb=round(random.uniform(2, 8), 2),
                roe=round(random.uniform(5, 20), 2),
                gross_margin=round(random.uniform(25, 45), 2),
                revenue_growth_3y=round(random.uniform(10, 35), 2),
                debt_to_equity=round(random.uniform(0.3, 0.7), 2)
            )
            db.add(indicator)
        db.commit()
        print("创建了财务指标")
        
        # 4. 创建示例博主框架
        analysts_data = [
            {
                "analyst_name": "半导体老王",
                "analyst_id": "semiconductor_wang",
                "platform": "雪球",
                "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=wang",
                "focus_sectors": ["semiconductor"],
                "style_tags": ["价值投资", "长线持有", "产业研究"],
                "selection_criteria": [
                    {"criteria": "库存周期处于底部区域", "weight": 30},
                    {"criteria": "国产替代逻辑清晰", "weight": 25},
                    {"criteria": "毛利率 > 30%", "weight": 20},
                    {"criteria": "研发投入占比 > 10%", "weight": 15},
                    {"criteria": "管理层持股稳定", "weight": 10}
                ],
                "decision_process": [
                    {"step": "Step 1: 行业景气度评估", "focus": "库存周期位置"},
                    {"step": "Step 2: 国产替代空间分析", "focus": "市场份额提升潜力"},
                    {"step": "Step 3: 财务数据验证", "focus": "毛利率、研发投入"},
                    {"step": "Step 4: 估值合理性", "focus": "PE分位数"},
                    {"step": "Step 5: 风险评估", "focus": "美国出口管制影响"}
                ],
                "key_metrics": [
                    {"metric": "库存周期位置", "weight": 30},
                    {"metric": "国产替代率", "weight": 25},
                    {"metric": "毛利率变化", "weight": 20},
                    {"metric": "PE估值分位", "weight": 15},
                    {"metric": "研发投入占比", "weight": 10}
                ],
                "risk_rules": [
                    {"rule": "止损线 -20%", "action": "无条件止损"},
                    {"rule": "单只最大仓位 20%", "action": "分散风险"}
                ],
                "avoid_patterns": [
                    "连续2季度营收下滑",
                    "大股东持续减持",
                    "商誉占净资产 > 30%"
                ],
                "style_summary": "专注于半导体产业链深度研究，重视库存周期和国产替代逻辑，偏好左侧布局行业龙头。",
                "total_judgments": 45,
                "correct_judgments": 31,
                "hit_rate": 68.9,
                "avg_hold_period": "6-12个月"
            },
            {
                "analyst_name": "AI投研圈",
                "analyst_id": "ai_research_circle",
                "platform": "微信公众号",
                "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=ai",
                "focus_sectors": ["ai", "cloud_computing"],
                "style_tags": ["成长投资", "技术驱动", "赛道投资"],
                "selection_criteria": [
                    {"criteria": "技术壁垒高", "weight": 30},
                    {"criteria": "营收增速 > 30%", "weight": 25},
                    {"criteria": "下游需求旺盛", "weight": 25},
                    {"criteria": "团队技术背景强", "weight": 20}
                ],
                "decision_process": [
                    {"step": "Step 1: 技术壁垒评估", "focus": "核心技术护城河"},
                    {"step": "Step 2: 下游需求分析", "focus": "应用场景和客户"},
                    {"step": "Step 3: 成长性验证", "focus": "营收增速、订单能见度"},
                    {"step": "Step 4: 竞争格局", "focus": "市场份额和对手"},
                    {"step": "Step 5: 估值容忍度", "focus": "成长性溢价"}
                ],
                "key_metrics": [
                    {"metric": "营收增速", "weight": 30},
                    {"metric": "技术壁垒", "weight": 25},
                    {"metric": "客户质量", "weight": 20},
                    {"metric": "市场份额", "weight": 15},
                    {"metric": "团队背景", "weight": 10}
                ],
                "risk_rules": [
                    {"rule": "增速放缓立即减仓", "action": "趋势破坏"},
                    {"rule": "技术路线被颠覆", "action": "清仓止损"}
                ],
                "avoid_patterns": [
                    "技术路线不清晰",
                    "过度依赖单一客户",
                    "管理层频繁变动"
                ],
                "style_summary": "专注AI和云计算赛道，重视技术壁垒和成长性，愿意给予高估值溢价，偏好右侧趋势投资。",
                "total_judgments": 38,
                "correct_judgments": 27,
                "hit_rate": 71.1,
                "avg_hold_period": "3-6个月"
            },
            {
                "analyst_name": "新能源观察",
                "analyst_id": "new_energy_observer",
                "platform": "微博",
                "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=energy",
                "focus_sectors": ["new_energy"],
                "style_tags": ["产业跟踪", "周期投资", "龙头偏好"],
                "selection_criteria": [
                    {"criteria": "行业龙头地位", "weight": 30},
                    {"criteria": "成本优势明显", "weight": 25},
                    {"criteria": "产能扩张有序", "weight": 20},
                    {"criteria": "海外市场拓展", "weight": 15},
                    {"criteria": "政策支持力度", "weight": 10}
                ],
                "decision_process": [
                    {"step": "Step 1: 产业链位置分析", "focus": "上下游议价能力"},
                    {"step": "Step 2: 成本竞争力", "focus": "毛利率和成本曲线"},
                    {"step": "Step 3: 产能和订单", "focus": "产能利用率和订单能见度"},
                    {"step": "Step 4: 竞争格局", "focus": "市占率变化趋势"},
                    {"step": "Step 5: 政策和海外", "focus": "政策支持和出海进度"}
                ],
                "key_metrics": [
                    {"metric": "市占率", "weight": 30},
                    {"metric": "毛利率", "weight": 25},
                    {"metric": "产能利用率", "weight": 20},
                    {"metric": "海外收入占比", "weight": 15},
                    {"metric": "政策支持", "weight": 10}
                ],
                "risk_rules": [
                    {"rule": "价格战启动减仓", "action": "竞争恶化"},
                    {"rule": "产能过剩预警", "action": "降低仓位"}
                ],
                "avoid_patterns": [
                    "二线厂商无成本优势",
                    "过度依赖补贴",
                    "技术路线落后"
                ],
                "style_summary": "深耕新能源产业链，重视龙头地位和成本优势，关注产能周期和竞争格局变化，偏好左侧布局。",
                "total_judgments": 52,
                "correct_judgments": 34,
                "hit_rate": 65.4,
                "avg_hold_period": "6-12个月"
            }
        ]
        
        for data in analysts_data:
            analyst = AnalystFramework(**data)
            db.add(analyst)
        db.commit()
        print("创建了博主框架数据")
        
        print("数据库初始化完成！")
        
    except Exception as e:
        print(f"初始化失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
