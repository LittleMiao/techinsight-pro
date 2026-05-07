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

            # === 半导体 - 存储芯片 (6只) ===
            {"symbol": "603986.SH", "name": "兆易创新", "market": "sh", "sector": "semiconductor", "sub_sector": "存储芯片", "total_shares": 667000000, "is_hot": True},
            {"symbol": "688525.SH", "name": "佰维存储", "market": "sh", "sector": "semiconductor", "sub_sector": "存储芯片", "total_shares": 430000000},
            {"symbol": "301308.SZ", "name": "江波龙", "market": "sz", "sector": "semiconductor", "sub_sector": "存储模组", "total_shares": 413000000},
            {"symbol": "688766.SH", "name": "普冉股份", "market": "sh", "sector": "semiconductor", "sub_sector": "NOR Flash", "total_shares": 76000000},
            {"symbol": "688110.SH", "name": "东芯股份", "market": "sh", "sector": "semiconductor", "sub_sector": "存储芯片", "total_shares": 442000000},
            {"symbol": "688416.SH", "name": "恒烁股份", "market": "sh", "sector": "semiconductor", "sub_sector": "NOR Flash", "total_shares": 83000000},

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

        # 5. 创建历史财务指标数据（每只股票8个季度）
        total_hist = 0
        quarters = [
            date(2024, 3, 31), date(2024, 6, 30), date(2024, 9, 30), date(2024, 12, 31),
            date(2025, 3, 31), date(2025, 6, 30), date(2025, 9, 30), date(2025, 12, 31)
        ]
        hist_fields = [
            "pe_ttm", "pb", "ps_ttm", "roe", "roa",
            "gross_margin", "net_margin", "operating_margin",
            "revenue_growth_3y", "profit_growth_3y",
            "debt_to_equity", "current_ratio"
        ]

        for stock in stocks_data:
            current = db.query(FinancialIndicator).filter(
                FinancialIndicator.symbol == stock["symbol"]
            ).first()
            if not current:
                continue

            for i, q_date in enumerate(quarters):
                # 越早的季度偏离越大，越接近当前值的季度偏离越小
                factor = 0.7 + 0.3 * (i / (len(quarters) - 1))  # 0.7 -> 1.0
                noise = random.uniform(0.85, 1.15)
                multiplier = factor * noise

                hist_data = {
                    "symbol": stock["symbol"],
                    "report_date": q_date,
                }
                for field in hist_fields:
                    current_val = getattr(current, field, None)
                    if current_val is not None:
                        hist_data[field] = round(current_val * multiplier, 2)
                    else:
                        hist_data[field] = None

                db.add(HistoricalIndicator(**hist_data))
                total_hist += 1

        db.commit()
        print(f"创建了 {total_hist} 条历史财务指标数据")

        # 6. 创建信息源数据（每只股票6-10条）
        total_sources = 0

        # 行业相关的新闻/研报关键词模板
        sector_keywords = {
            "semiconductor": {
                "news_titles": [
                    "{name}获得大额芯片订单，产能利用率持续攀升",
                    "{name}发布新一代{sub_sector}产品，技术指标达到国际领先水平",
                    "半导体国产替代加速，{name}有望受益于政策红利",
                ],
                "research_summaries": [
                    "半导体行业景气度持续回升，{name}作为{sub_sector}龙头有望充分受益。公司技术实力突出，客户拓展顺利，维持增持评级。",
                    "看好{name}在{sub_sector}领域的长期竞争力，随着下游需求回暖和国产替代推进，业绩有望持续超预期。",
                    '{name}核心产品竞争力强，{sub_sector}赛道空间广阔，给予「买入」评级，目标价看涨30%。',
                ],
                "report_summaries": [
                    "报告期内，公司实现营业收入稳健增长，{sub_sector}业务保持良好发展势头。研发投入持续加大，新产品进展顺利，市场竞争力进一步提升。",
                    "公司{sub_sector}业务收入同比增长显著，毛利率保持稳定。在建产能稳步推进，为未来增长奠定基础。",
                ],
            },
            "ai": {
                "news_titles": [
                    "{name}发布大模型新产品，AI应用落地加速",
                    "{name}与多家头部企业达成AI战略合作协议",
                    "AI政策持续加码，{name}核心业务迎来发展机遇",
                ],
                "research_summaries": [
                    "AI产业趋势明确，{name}在{sub_sector}领域具备核心技术优势。随着大模型商业化加速，公司业绩有望进入快速增长期。",
                    "{name}AI产品矩阵持续丰富，{sub_sector}赛道渗透率快速提升，给予「增持」评级。",
                    "看好{name}在AI{sub_sector}领域的先发优势和技术壁垒，下游需求旺盛，维持「买入」评级。",
                ],
                "report_summaries": [
                    "报告期内，公司AI{sub_sector}业务收入实现高速增长，研发投入占比进一步提升。大模型相关产品已进入商业化阶段，客户反馈良好。",
                    "公司持续深耕AI{sub_sector}领域，核心技术能力不断增强。报告期内新签订单大幅增长，市场份额稳步提升。",
                ],
            },
            "new_energy": {
                "news_titles": [
                    "{name}中标海外大型项目，国际化布局取得新突破",
                    "新能源补贴政策落地，{name}产业链地位进一步巩固",
                    "{name}发布新一代产品，能量密度/转换效率创行业新高",
                ],
                "research_summaries": [
                    "新能源行业景气度回升，{name}作为{sub_sector}龙头具备显著成本优势。海外市场拓展顺利，维持「增持」评级。",
                    "看好{name}在{sub_sector}领域的龙头地位，产能扩张有序，盈利能力持续改善，给予「买入」评级。",
                    "{name}{sub_sector}业务量价齐升，行业竞争格局优化带来盈利弹性，维持「增持」评级。",
                ],
                "report_summaries": [
                    "报告期内，公司{sub_sector}业务保持快速增长，产能利用率维持高位。海外收入占比持续提升，全球化战略稳步推进。",
                    "公司{sub_sector}产品出货量同比增长，市场份额进一步扩大。成本控制能力突出，盈利水平行业领先。",
                ],
            },
            "cloud_computing": {
                "news_titles": [
                    "{name}发布新一代云原生产品，客户数量突破新高",
                    "数字经济政策持续利好，{name}SaaS业务加速增长",
                    "{name}中标多个政企大单，行业解决方案能力获认可",
                ],
                "research_summaries": [
                    "企业数字化转型加速，{name}在{sub_sector}领域具备深厚积累。SaaS化转型成效显著，ARR保持高速增长，维持「增持」评级。",
                    "看好{name}在{sub_sector}赛道的长期成长性，客户续费率和客单价持续提升，给予「买入」评级。",
                    "{name}{sub_sector}产品竞争力突出，AI赋能带来新的增长曲线，维持「增持」评级。",
                ],
                "report_summaries": [
                    "报告期内，公司{sub_sector}业务收入稳健增长，订阅收入占比持续提升。研发投入加大，AI功能集成进展顺利。",
                    "公司{sub_sector}产品线持续丰富，大客户拓展成效显著。云化转型推动毛利率稳步改善。",
                ],
            },
        }

        analyst_sources_map = {
            "semiconductor": ["半导体老王", "AI投研圈"],
            "ai": ["AI投研圈", "半导体老王"],
            "new_energy": ["新能源观察", "AI投研圈"],
            "cloud_computing": ["AI投研圈", "新能源观察"],
        }

        research_brokers = ["中信证券", "华泰证券", "国泰君安", "招商证券", "海通证券"]
        news_sources = ["东方财富", "同花顺", "证券时报", "上海证券报"]

        now = datetime.now()

        for stock in stocks_data:
            sector = stock["sector"]
            sub_sector = stock["sub_sector"]
            name = stock["name"]
            kw = sector_keywords.get(sector, sector_keywords["semiconductor"])

            # --- 公司公告/报告 (2条) ---
            report_titles = [
                f"{name}2024年年度报告",
                f"{name}2024年第三季度报告",
            ]
            report_dates = [
                datetime(2025, 3, 28) + timedelta(days=random.randint(0, 10)),
                datetime(2024, 10, 25) + timedelta(days=random.randint(0, 10)),
            ]
            for ri, r_title in enumerate(report_titles):
                summary = random.choice(kw["report_summaries"]).format(
                    name=name, sub_sector=sub_sector
                )
                db.add(InformationSource(
                    symbol=stock["symbol"],
                    source_type="report",
                    title=r_title,
                    source=name,
                    publish_time=report_dates[ri],
                    summary=summary,
                    sentiment="neutral",
                ))
                total_sources += 1

            # --- 券商研报 (2-3条) ---
            num_research = random.randint(2, 3)
            for _ in range(num_research):
                broker = random.choice(research_brokers)
                r_title = f"{name}深度报告：{sub_sector}行业景气度回升，维持增持评级"
                days_ago = random.randint(30, 180)
                pub_time = now - timedelta(days=days_ago)
                summary = random.choice(kw["research_summaries"]).format(
                    name=name, sub_sector=sub_sector
                )
                db.add(InformationSource(
                    symbol=stock["symbol"],
                    source_type="research",
                    title=r_title,
                    source=broker,
                    publish_time=pub_time,
                    summary=summary,
                    sentiment="positive",
                ))
                total_sources += 1

            # --- 新闻资讯 (2-3条) ---
            num_news = random.randint(2, 3)
            news_titles_shuffled = random.sample(kw["news_titles"], min(num_news, len(kw["news_titles"])))
            for ni, n_title_tpl in enumerate(news_titles_shuffled):
                n_title = n_title_tpl.format(name=name, sub_sector=sub_sector)
                days_ago = random.randint(1, 180)
                pub_time = now - timedelta(days=days_ago)
                sentiment = random.choice(["positive", "neutral"])
                db.add(InformationSource(
                    symbol=stock["symbol"],
                    source_type="news",
                    title=n_title,
                    source=random.choice(news_sources),
                    publish_time=pub_time,
                    summary=n_title,
                    sentiment=sentiment,
                ))
                total_sources += 1

            # --- 博主观点 (1-2条) ---
            num_analyst = random.randint(1, 2)
            available_analysts = analyst_sources_map.get(sector, ["AI投研圈"])
            chosen_analysts = random.sample(available_analysts, min(num_analyst, len(available_analysts)))
            for analyst in chosen_analysts:
                a_title = f"关于{name}的近期看法"
                days_ago = random.randint(1, 90)
                pub_time = now - timedelta(days=days_ago)
                sentiment = random.choice(["positive", "neutral"])
                db.add(InformationSource(
                    symbol=stock["symbol"],
                    source_type="analyst_opinion",
                    title=a_title,
                    source=analyst,
                    publish_time=pub_time,
                    summary=f"{analyst}：{name}近期基本面稳健，{sub_sector}赛道长期逻辑不变，建议持续关注。",
                    sentiment=sentiment,
                ))
                total_sources += 1

        db.commit()
        print(f"创建了 {total_sources} 条信息源数据")

        print("数据库初始化完成！")
        print("- 51只科技板块股票")
        print("- 完整财务指标（27个字段）")
        print("- 3个博主框架")
        print(f"- {total_hist} 条历史财务指标（8个季度）")
        print(f"- {total_sources} 条信息源")

    except Exception as e:
        print(f"初始化失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
