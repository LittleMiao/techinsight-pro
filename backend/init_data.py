"""
初始化数据库数据 - 51只科技板块股票 + 完整财务指标 + 3个博主框架
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

        # 1. 创建51只科技板块股票基础数据
        stocks_data = [
            # === 半导体 - 晶圆代工 (3只) ===
            {"symbol": "688981.SH", "name": "中芯国际", "market": "sh", "sector": "semiconductor", "sub_sector": "晶圆代工", "total_shares": 7900000000, "is_hot": True},
            {"symbol": "688396.SH", "name": "华润微", "market": "sh", "sector": "semiconductor", "sub_sector": "晶圆代工", "total_shares": 1320000000},
            {"symbol": "688727.SH", "name": "广立微", "market": "sh", "sector": "semiconductor", "sub_sector": "晶圆代工", "total_shares": 200000000},

            # === 半导体 - 设备 (7只) ===
            {"symbol": "002371.SZ", "name": "北方华创", "market": "sz", "sector": "semiconductor", "sub_sector": "半导体设备", "total_shares": 530000000, "is_hot": True},
            {"symbol": "688012.SH", "name": "中微公司", "market": "sh", "sector": "semiconductor", "sub_sector": "刻蚀设备", "total_shares": 618000000},
            {"symbol": "688082.SH", "name": "盛美上海", "market": "sh", "sector": "semiconductor", "sub_sector": "清洗设备", "total_shares": 433000000},
            {"symbol": "300316.SZ", "name": "晶盛机电", "market": "sz", "sector": "semiconductor", "sub_sector": "硅片设备", "total_shares": 1300000000},
            {"symbol": "688037.SH", "name": "芯源微", "market": "sh", "sector": "semiconductor", "sub_sector": "涂胶显影设备", "total_shares": 136000000},
            {"symbol": "688200.SH", "name": "华峰测控", "market": "sh", "sector": "semiconductor", "sub_sector": "测试设备", "total_shares": 97000000},
            {"symbol": "688521.SH", "name": "芯海科技", "market": "sh", "sector": "semiconductor", "sub_sector": "芯片测试", "total_shares": 142000000},

            # === 半导体 - 材料 (5只) ===
            {"symbol": "688126.SH", "name": "沪硅产业", "market": "sh", "sector": "semiconductor", "sub_sector": "硅片材料", "total_shares": 2730000000},
            {"symbol": "300655.SZ", "name": "晶瑞电材", "market": "sz", "sector": "semiconductor", "sub_sector": "电子化学品", "total_shares": 580000000},
            {"symbol": "688019.SH", "name": "安集科技", "market": "sh", "sector": "semiconductor", "sub_sector": "抛光材料", "total_shares": 99000000},
            {"symbol": "688234.SH", "name": "天岳先进", "market": "sh", "sector": "semiconductor", "sub_sector": "碳化硅材料", "total_shares": 440000000},
            {"symbol": "688581.SH", "name": "富乐德", "market": "sh", "sector": "semiconductor", "sub_sector": "陶瓷材料", "total_shares": 350000000},

            # === 半导体 - 芯片设计 (9只) ===
            {"symbol": "603501.SH", "name": "韦尔股份", "market": "sh", "sector": "semiconductor", "sub_sector": "芯片设计", "total_shares": 1200000000},
            {"symbol": "688008.SH", "name": "澜起科技", "market": "sh", "sector": "semiconductor", "sub_sector": "内存接口芯片", "total_shares": 1140000000},
            {"symbol": "300782.SZ", "name": "卓胜微", "market": "sz", "sector": "semiconductor", "sub_sector": "射频芯片", "total_shares": 534000000},
            {"symbol": "688099.SH", "name": "晶晨股份", "market": "sh", "sector": "semiconductor", "sub_sector": "SoC芯片", "total_shares": 416000000},
            {"symbol": "603893.SH", "name": "瑞芯微", "market": "sh", "sector": "semiconductor", "sub_sector": "SoC芯片", "total_shares": 418000000},
            {"symbol": "688536.SH", "name": "思瑞浦", "market": "sh", "sector": "semiconductor", "sub_sector": "信号链芯片", "total_shares": 132000000},
            {"symbol": "300661.SZ", "name": "圣邦股份", "market": "sz", "sector": "semiconductor", "sub_sector": "模拟芯片", "total_shares": 471000000},
            {"symbol": "688220.SH", "name": "翱捷科技", "market": "sh", "sector": "semiconductor", "sub_sector": "基带芯片", "total_shares": 418000000},
            {"symbol": "688368.SH", "name": "晶丰明源", "market": "sh", "sector": "semiconductor", "sub_sector": "电源管理芯片", "total_shares": 103000000},

            # === 半导体 - 封测 (2只) ===
            {"symbol": "600584.SH", "name": "长电科技", "market": "sh", "sector": "semiconductor", "sub_sector": "封装测试", "total_shares": 1780000000},
            {"symbol": "002156.SZ", "name": "通富微电", "market": "sz", "sector": "semiconductor", "sub_sector": "封装测试", "total_shares": 1510000000},

            # === AI - AI芯片 (3只) ===
            {"symbol": "688256.SH", "name": "寒武纪", "market": "sh", "sector": "ai", "sub_sector": "AI芯片", "total_shares": 416000000, "is_hot": True},
            {"symbol": "688787.SH", "name": "海天瑞声", "market": "sh", "sector": "ai", "sub_sector": "AI数据服务", "total_shares": 60000000},
            {"symbol": "688498.SH", "name": "源杰科技", "market": "sh", "sector": "ai", "sub_sector": "光芯片", "total_shares": 60000000},

            # === AI - 应用 (4只) ===
            {"symbol": "002230.SZ", "name": "科大讯飞", "market": "sz", "sector": "ai", "sub_sector": "语音识别", "total_shares": 2300000000, "is_hot": True},
            {"symbol": "688327.SH", "name": "云从科技", "market": "sh", "sector": "ai", "sub_sector": "计算机视觉", "total_shares": 740000000},
            {"symbol": "688207.SH", "name": "格灵深瞳", "market": "sh", "sector": "ai", "sub_sector": "计算机视觉", "total_shares": 260000000},
            {"symbol": "688039.SH", "name": "当虹科技", "market": "sh", "sector": "ai", "sub_sector": "视频AI", "total_shares": 80000000},

            # === 新能源 - 动力电池 (4只) ===
            {"symbol": "300750.SZ", "name": "宁德时代", "market": "sz", "sector": "new_energy", "sub_sector": "动力电池", "total_shares": 4400000000, "is_hot": True},
            {"symbol": "002074.SZ", "name": "国轩高科", "market": "sz", "sector": "new_energy", "sub_sector": "动力电池", "total_shares": 1780000000},
            {"symbol": "688567.SH", "name": "孚能科技", "market": "sh", "sector": "new_energy", "sub_sector": "动力电池", "total_shares": 1200000000},
            {"symbol": "301157.SZ", "name": "华塑科技", "market": "sz", "sector": "new_energy", "sub_sector": "电池管理", "total_shares": 60000000},

            # === 新能源 - 整车 (4只) ===
            {"symbol": "002594.SZ", "name": "比亚迪", "market": "sz", "sector": "new_energy", "sub_sector": "新能源汽车", "total_shares": 2900000000, "is_hot": True},
            {"symbol": "601127.SH", "name": "赛力斯", "market": "sh", "sector": "new_energy", "sub_sector": "新能源汽车", "total_shares": 1500000000},
            {"symbol": "000625.SZ", "name": "长安汽车", "market": "sz", "sector": "new_energy", "sub_sector": "新能源汽车", "total_shares": 9910000000},
            {"symbol": "600733.SH", "name": "北汽蓝谷", "market": "sh", "sector": "new_energy", "sub_sector": "新能源汽车", "total_shares": 5570000000},

            # === 新能源 - 光伏 (7只) ===
            {"symbol": "601012.SH", "name": "隆基绿能", "market": "sh", "sector": "new_energy", "sub_sector": "光伏", "total_shares": 7500000000},
            {"symbol": "600438.SH", "name": "通威股份", "market": "sh", "sector": "new_energy", "sub_sector": "光伏", "total_shares": 4500000000},
            {"symbol": "688599.SH", "name": "天合光能", "market": "sh", "sector": "new_energy", "sub_sector": "光伏组件", "total_shares": 2180000000},
            {"symbol": "688223.SH", "name": "晶科能源", "market": "sh", "sector": "new_energy", "sub_sector": "光伏组件", "total_shares": 10000000000},
            {"symbol": "002459.SZ", "name": "晶澳科技", "market": "sz", "sector": "new_energy", "sub_sector": "光伏组件", "total_shares": 3300000000},
            {"symbol": "300274.SZ", "name": "阳光电源", "market": "sz", "sector": "new_energy", "sub_sector": "逆变器", "total_shares": 1480000000},
            {"symbol": "688390.SH", "name": "固德威", "market": "sh", "sector": "new_energy", "sub_sector": "逆变器", "total_shares": 173000000},

            # === 新能源 - 储能 (3只) ===
            {"symbol": "300014.SZ", "name": "亿纬锂能", "market": "sz", "sector": "new_energy", "sub_sector": "储能电池", "total_shares": 2040000000},
            {"symbol": "002812.SZ", "name": "恩捷股份", "market": "sz", "sector": "new_energy", "sub_sector": "锂电池隔膜", "total_shares": 977000000},
            {"symbol": "300073.SZ", "name": "当升科技", "market": "sz", "sector": "new_energy", "sub_sector": "锂电池正极", "total_shares": 507000000},

            # === 云计算 - 软件服务 (6只) ===
            {"symbol": "688111.SH", "name": "金山办公", "market": "sh", "sector": "cloud_computing", "sub_sector": "办公软件", "total_shares": 461000000, "is_hot": True},
            {"symbol": "600570.SH", "name": "恒生电子", "market": "sh", "sector": "cloud_computing", "sub_sector": "金融软件", "total_shares": 1900000000},
            {"symbol": "300454.SZ", "name": "深信服", "market": "sz", "sector": "cloud_computing", "sub_sector": "网络安全", "total_shares": 419000000},
            {"symbol": "688561.SH", "name": "奇安信", "market": "sh", "sector": "cloud_computing", "sub_sector": "网络安全", "total_shares": 685000000},
            {"symbol": "300496.SZ", "name": "中科创达", "market": "sz", "sector": "cloud_computing", "sub_sector": "智能操作系统", "total_shares": 459000000},
            {"symbol": "688188.SH", "name": "柏楚电子", "market": "sh", "sector": "cloud_computing", "sub_sector": "工业软件", "total_shares": 146000000},

            # === 云计算 - SaaS (4只) ===
            {"symbol": "300682.SZ", "name": "朗新科技", "market": "sz", "sector": "cloud_computing", "sub_sector": "能源SaaS", "total_shares": 1070000000},
            {"symbol": "688369.SH", "name": "致远互联", "market": "sh", "sector": "cloud_computing", "sub_sector": "协同办公", "total_shares": 115000000},
            {"symbol": "688228.SH", "name": "开普云", "market": "sh", "sector": "cloud_computing", "sub_sector": "政务SaaS", "total_shares": 67000000},
            {"symbol": "300229.SZ", "name": "拓尔思", "market": "sz", "sector": "cloud_computing", "sub_sector": "NLP SaaS", "total_shares": 715000000},
        ]

        for data in stocks_data:
            stock = Stock(**data)
            db.add(stock)
        db.commit()
        print(f"创建了 {len(stocks_data)} 只股票数据")

        # 2. 创建实时行情数据
        for stock in stocks_data:
            base_price = random.uniform(10, 500)
            change = random.uniform(-8, 8)
            quote = StockQuote(
                symbol=stock["symbol"],
                current_price=round(base_price + change, 2),
                open_price=round(base_price + random.uniform(-2, 2), 2),
                high_price=round(base_price + random.uniform(0, 10), 2),
                low_price=round(base_price - random.uniform(0, 10), 2),
                prev_close=base_price,
                change_amount=round(change, 2),
                change_percent=round(change / base_price * 100, 2),
                volume=random.randint(1000000, 100000000),
                turnover=random.randint(100000000, 10000000000),
                update_time=datetime.now()
            )
            db.add(quote)
        db.commit()
        print("创建了行情数据")

        # 3. 创建完整财务指标数据（27个字段）
        for stock in stocks_data:
            # 根据不同行业设置合理的财务指标范围
            sector = stock["sector"]

            if sector == "semiconductor":
                pe_ttm = round(random.uniform(30, 80), 2)
                pb = round(random.uniform(3, 8), 2)
                gross_margin = round(random.uniform(35, 60), 2)
                roe = round(random.uniform(8, 20), 2)
                revenue_growth = round(random.uniform(10, 35), 2)
            elif sector == "ai":
                pe_ttm = round(random.uniform(50, 120), 2)
                pb = round(random.uniform(4, 12), 2)
                gross_margin = round(random.uniform(50, 80), 2)
                roe = round(random.uniform(5, 15), 2)
                revenue_growth = round(random.uniform(20, 50), 2)
            elif sector == "new_energy":
                pe_ttm = round(random.uniform(15, 40), 2)
                pb = round(random.uniform(2, 6), 2)
                gross_margin = round(random.uniform(15, 30), 2)
                roe = round(random.uniform(10, 25), 2)
                revenue_growth = round(random.uniform(15, 40), 2)
            else:  # cloud_computing
                pe_ttm = round(random.uniform(40, 90), 2)
                pb = round(random.uniform(5, 15), 2)
                gross_margin = round(random.uniform(60, 85), 2)
                roe = round(random.uniform(8, 18), 2)
                revenue_growth = round(random.uniform(15, 35), 2)

            indicator = FinancialIndicator(
                symbol=stock["symbol"],
                report_date=date(2024, 12, 31),
                # 估值指标 (5个)
                pe_ttm=pe_ttm,
                pb=pb,
                ps_ttm=round(random.uniform(2, 20), 2),
                ev_ebitda=round(random.uniform(10, 40), 2),
                pcf=round(random.uniform(5, 30), 2),
                # 盈利能力指标 (5个)
                roe=roe,
                roa=round(roe * random.uniform(0.4, 0.8), 2),
                gross_margin=gross_margin,
                net_margin=round(gross_margin * random.uniform(0.3, 0.6), 2),
                operating_margin=round(gross_margin * random.uniform(0.4, 0.7), 2),
                # 成长性指标 (4个)
                revenue_growth_3y=revenue_growth,
                profit_growth_3y=round(revenue_growth * random.uniform(0.8, 1.2), 2),
                revenue_growth_5y=round(revenue_growth * random.uniform(0.9, 1.1), 2),
                profit_growth_5y=round(revenue_growth * random.uniform(0.7, 1.3), 2),
                # 偿债能力指标 (4个)
                current_ratio=round(random.uniform(1.0, 3.0), 2),
                quick_ratio=round(random.uniform(0.6, 2.5), 2),
                debt_to_equity=round(random.uniform(0.3, 0.65), 2),
                interest_coverage=round(random.uniform(3, 20), 2),
            )
            db.add(indicator)
        db.commit()
        print("创建了完整财务指标数据（27个字段）")

        # 4. 创建3个博主框架
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
        print("创建了3个博主框架数据")

        print("数据库初始化完成！")
        print("- 51只科技板块股票")
        print("- 完整财务指标（27个字段）")
        print("- 3个博主框架")

    except Exception as e:
        print(f"初始化失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
