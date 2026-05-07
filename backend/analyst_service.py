"""
博主风格蒸馏服务层
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from models import AnalystFramework, AnalystJudgment, SimulatedAnalysis, Stock, FinancialIndicator, StockQuote, HistoricalIndicator, InformationSource
from schemas import *
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import random


class AnalystService:
    """博主框架管理服务"""

    @staticmethod
    def get_analysts(db: Session, is_active: bool = True):
        """获取博主列表"""
        query = db.query(AnalystFramework)
        if is_active:
            query = query.filter(AnalystFramework.is_active == True)

        analysts = query.order_by(desc(AnalystFramework.hit_rate)).all()

        return {
            "total": len(analysts),
            "list": [
                {
                    "id": a.id,
                    "analyst_name": a.analyst_name,
                    "analyst_id": a.analyst_id,
                    "platform": a.platform,
                    "avatar_url": a.avatar_url,
                    "focus_sectors": a.focus_sectors,
                    "total_judgments": a.total_judgments,
                    "hit_rate": a.hit_rate,
                    "style_tags": a.style_tags,
                    "is_active": a.is_active
                }
                for a in analysts
            ]
        }

    @staticmethod
    def get_analyst(db: Session, analyst_id: str):
        """获取博主详情"""
        analyst = db.query(AnalystFramework).filter(
            AnalystFramework.analyst_id == analyst_id
        ).first()

        if not analyst:
            return None

        return {
            "id": analyst.id,
            "analyst_name": analyst.analyst_name,
            "analyst_id": analyst.analyst_id,
            "platform": analyst.platform,
            "profile_url": analyst.profile_url,
            "avatar_url": analyst.avatar_url,
            "focus_sectors": analyst.focus_sectors,
            "selection_criteria": analyst.selection_criteria,
            "decision_process": analyst.decision_process,
            "key_metrics": analyst.key_metrics,
            "risk_rules": analyst.risk_rules,
            "avoid_patterns": analyst.avoid_patterns,
            "style_summary": analyst.style_summary,
            "total_judgments": analyst.total_judgments,
            "correct_judgments": analyst.correct_judgments,
            "hit_rate": analyst.hit_rate,
            "avg_hold_period": analyst.avg_hold_period,
            "style_tags": analyst.style_tags,
            "is_active": analyst.is_active,
            "created_at": analyst.created_at
        }

    @staticmethod
    def create_analyst(db: Session, analyst_data: AnalystFrameworkCreate):
        """创建博主框架"""
        analyst = AnalystFramework(
            analyst_name=analyst_data.analyst_name,
            analyst_id=analyst_data.analyst_id,
            platform=analyst_data.platform,
            profile_url=analyst_data.profile_url,
            focus_sectors=analyst_data.focus_sectors,
            style_tags=analyst_data.style_tags,
            selection_criteria=analyst_data.selection_criteria,
            decision_process=analyst_data.decision_process,
            key_metrics=analyst_data.key_metrics,
            risk_rules=analyst_data.risk_rules,
            avoid_patterns=analyst_data.avoid_patterns,
            style_summary=analyst_data.style_summary
        )
        db.add(analyst)
        db.commit()
        db.refresh(analyst)
        return analyst

    @staticmethod
    def get_judgments(db: Session, analyst_id: str, limit: int = 20):
        """获取博主历史判断"""
        judgments = db.query(AnalystJudgment).filter(
            AnalystJudgment.analyst_id == analyst_id
        ).order_by(desc(AnalystJudgment.judgment_date)).limit(limit).all()

        return {
            "total": len(judgments),
            "list": [
                {
                    "id": j.id,
                    "symbol": j.symbol,
                    "judgment_date": j.judgment_date,
                    "judgment_type": j.judgment_type,
                    "target_price": j.target_price,
                    "time_horizon": j.time_horizon,
                    "core_logic": j.core_logic,
                    "key_factors": j.key_factors,
                    "is_correct": j.is_correct,
                    "return_rate": j.return_rate
                }
                for j in judgments
            ]
        }


class SimulationService:
    """模拟分析服务"""

    @staticmethod
    def simulate_analysis(db: Session, analyst_id: str, symbol: str):
        """执行模拟分析"""
        # 获取博主框架
        analyst = db.query(AnalystFramework).filter(
            AnalystFramework.analyst_id == analyst_id
        ).first()

        if not analyst:
            return None

        # 获取股票数据
        stock = db.query(Stock).filter(Stock.symbol == symbol).first()
        if not stock:
            return None

        quote = stock.quote
        indicator = db.query(FinancialIndicator).filter(
            FinancialIndicator.symbol == symbol
        ).order_by(desc(FinancialIndicator.report_date)).first()

        # 模拟分析步骤
        steps = SimulationService._generate_analysis_steps(
            analyst, stock, quote, indicator
        )

        # 计算综合判断
        passed_steps = sum(1 for s in steps if s["result"] == "通过")
        total_steps = len(steps)
        confidence = (passed_steps / total_steps) * 100 if total_steps > 0 else 50

        # 判断方向
        if confidence >= 70:
            judgment = "buy"
        elif confidence >= 40:
            judgment = "hold"
        else:
            judgment = "sell"

        # 生成关键发现和风险提示
        key_findings = SimulationService._generate_key_findings(steps, stock)
        risk_warnings = SimulationService._generate_risk_warnings(analyst, indicator)

        # 生成完整报告
        report = SimulationService._generate_report(
            analyst, stock, steps, judgment, confidence, key_findings, risk_warnings
        )

        # 保存模拟结果
        simulation = SimulatedAnalysis(
            analyst_id=analyst_id,
            symbol=symbol,
            analysis_date=datetime.now(),
            simulated_judgment=judgment,
            confidence_score=round(confidence, 1),
            style_similarity="高" if confidence > 60 else "中",
            analysis_steps=steps,
            key_findings=key_findings,
            risk_warnings=risk_warnings,
            full_report=report
        )
        db.add(simulation)
        db.commit()

        return {
            "analyst_name": analyst.analyst_name,
            "analyst_id": analyst.analyst_id,
            "symbol": symbol,
            "analysis_date": simulation.analysis_date,
            "simulated_judgment": judgment,
            "confidence_score": round(confidence, 1),
            "style_similarity": simulation.style_similarity,
            "steps": steps,
            "key_findings": key_findings,
            "risk_warnings": risk_warnings,
            "divergence_from_consensus": "市场主流观点偏谨慎，但按该博主框架，当前具备配置价值" if judgment == "buy" else None,
            "report": report
        }

    @staticmethod
    def _generate_analysis_steps(analyst, stock, quote, indicator):
        """生成分析步骤"""
        # 使用博主的决策流程，如果没有则使用默认流程
        process = analyst.decision_process or [
            {"step": "Step 1: 行业景气度评估", "focus": "行业周期位置"},
            {"step": "Step 2: 竞争格局分析", "focus": "市场地位"},
            {"step": "Step 3: 财务数据验证", "focus": "核心财务指标"},
            {"step": "Step 4: 估值合理性", "focus": "估值水平"},
            {"step": "Step 5: 风险评估", "focus": "主要风险点"}
        ]

        steps = []
        for i, proc in enumerate(process):
            step_name = proc.get("step", f"Step {i+1}")
            focus = proc.get("focus", "")

            # 根据步骤类型生成分析结果
            result, detail = SimulationService._analyze_step(
                step_name, focus, stock, quote, indicator
            )

            steps.append({
                "step": step_name,
                "result": result,
                "detail": detail
            })

        return steps

    @staticmethod
    def _analyze_step(step_name, focus, stock, quote, indicator):
        """分析单个步骤"""
        results = ["通过", "不通过", "待观察"]

        if "行业" in step_name or "景气" in step_name:
            # 模拟行业分析
            result = random.choice(["通过", "通过", "待观察"])
            detail = f"{stock.sub_sector}行业当前处于{'底部回升' if result == '通过' else '调整'}阶段"
            if stock.sector == "semiconductor":
                detail = "半导体库存周期处于底部回升阶段，产能利用率持续改善"
            elif stock.sector == "ai":
                detail = "AI行业景气度持续高企，算力需求旺盛"
            elif stock.sector == "new_energy":
                detail = "新能源行业竞争加剧，但龙头优势明显"
            return result, detail

        elif "竞争" in step_name or "格局" in step_name:
            result = "通过"
            detail = f"{stock.name}在{stock.sub_sector}领域具备领先优势"
            return result, detail

        elif "财务" in step_name:
            if indicator:
                if indicator.revenue_growth_3y and indicator.revenue_growth_3y > 15:
                    result = "通过"
                    detail = f"营收3年复合增长率{indicator.revenue_growth_3y:.1f}%，成长性良好"
                elif indicator.revenue_growth_3y and indicator.revenue_growth_3y > 0:
                    result = "待观察"
                    detail = f"营收增长{indicator.revenue_growth_3y:.1f}%，需关注后续改善"
                else:
                    result = "不通过"
                    detail = "营收增长承压，需警惕"
                return result, detail
            return "待观察", "财务数据待验证"

        elif "估值" in step_name:
            if indicator and indicator.pe_ttm:
                if indicator.pe_ttm < 30:
                    result = "通过"
                    detail = f"当前PE {indicator.pe_ttm:.1f}x，估值合理"
                elif indicator.pe_ttm < 50:
                    result = "待观察"
                    detail = f"当前PE {indicator.pe_ttm:.1f}x，估值中等"
                else:
                    result = "不通过"
                    detail = f"当前PE {indicator.pe_ttm:.1f}x，估值偏高"
                return result, detail
            return "待观察", "估值数据待确认"

        elif "风险" in step_name:
            result = random.choice(["通过", "待观察"])
            detail = "主要风险已充分定价" if result == "通过" else "存在不确定性风险需关注"
            return result, detail

        return random.choice(results), "分析中..."

    @staticmethod
    def _generate_key_findings(steps, stock):
        """生成关键发现"""
        findings = []
        for step in steps:
            if step["result"] == "通过":
                findings.append(step["detail"])
        return findings[:3] if findings else ["整体分析结果待进一步验证"]

    @staticmethod
    def _generate_risk_warnings(analyst, indicator):
        """生成风险提示"""
        warnings = []

        # 使用博主的风险规则
        if analyst.avoid_patterns:
            warnings.extend(analyst.avoid_patterns[:2])

        # 基于财务数据的风险提示
        if indicator:
            if hasattr(indicator, 'debt_to_equity') and indicator.debt_to_equity and indicator.debt_to_equity > 0.6:
                warnings.append("负债率偏高，需关注财务风险")
            if hasattr(indicator, 'revenue_growth_3y') and indicator.revenue_growth_3y and indicator.revenue_growth_3y < 10:
                warnings.append("营收增速放缓，成长性存疑")

        return warnings if warnings else ["暂无明显风险信号"]

    @staticmethod
    def _generate_report(analyst, stock, steps, judgment, confidence, findings, risks):
        """生成完整分析报告"""
        judgment_text = {"buy": "看多", "hold": "中性", "sell": "看空"}

        report = f"""【{analyst.analyst_name}风格模拟分析报告】

股票: {stock.name} ({stock.symbol})
板块: {stock.sector} - {stock.sub_sector}

═══════════════════════════════════════

【分析过程】

"""
        for step in steps:
            icon = "通过" if step["result"] == "通过" else ("待观察" if step["result"] == "待观察" else "不通过")
            report += f"[{icon}] {step['step']}\n   {step['detail']}\n\n"

        report += f"""═══════════════════════════════════════

【综合判断】{judgment_text.get(judgment, '中性')}
【置信度】{confidence:.0f}%

【关键发现】
"""
        for f in findings:
            report += f"- {f}\n"

        report += f"""
【风险提示】
"""
        for r in risks:
            report += f"- {r}\n"

        report += f"""
═══════════════════════════════════════

免责声明：本报告基于{analyst.analyst_name}历史分析框架模拟生成，
仅供参考，不构成投资建议。投资有风险，入市需谨慎。

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return report


class StockService:
    """股票服务"""

    @staticmethod
    def get_stocks(db: Session, sector: Optional[str] = None, page: int = 1, page_size: int = 20):
        """获取股票列表"""
        query = db.query(Stock)

        if sector:
            query = query.filter(Stock.sector == sector)

        total = query.count()
        stocks = query.offset((page - 1) * page_size).limit(page_size).all()

        result = []
        for stock in stocks:
            stock_dict = {
                "id": stock.id,
                "symbol": stock.symbol,
                "name": stock.name,
                "market": stock.market,
                "sector": stock.sector,
                "sub_sector": stock.sub_sector,
                "market_cap": stock.total_shares * stock.quote.current_price if stock.quote and stock.total_shares else None,
                "price": stock.quote.current_price if stock.quote else None,
                "change_percent": stock.quote.change_percent if stock.quote else None,
                "is_hot": stock.is_hot
            }
            result.append(stock_dict)

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "list": result
        }

    @staticmethod
    def get_stock_detail(db: Session, symbol: str):
        """获取股票详情 - 返回全部27个字段"""
        stock = db.query(Stock).filter(Stock.symbol == symbol).first()
        if not stock:
            return None

        quote = stock.quote
        indicator = db.query(FinancialIndicator).filter(
            FinancialIndicator.symbol == symbol
        ).order_by(desc(FinancialIndicator.report_date)).first()

        # 基础信息
        result = {
            "id": stock.id,
            "symbol": stock.symbol,
            "name": stock.name,
            "market": stock.market,
            "sector": stock.sector,
            "sub_sector": stock.sub_sector,
            "total_shares": stock.total_shares,
            "is_hot": stock.is_hot,
            # 行情数据
            "price": quote.current_price if quote else None,
            "change_percent": quote.change_percent if quote else None,
            "change_amount": quote.change_amount if quote else None,
            "open_price": quote.open_price if quote else None,
            "high_price": quote.high_price if quote else None,
            "low_price": quote.low_price if quote else None,
            "prev_close": quote.prev_close if quote else None,
            "volume": quote.volume if quote else None,
            "turnover": quote.turnover if quote else None,
            "market_cap": stock.total_shares * quote.current_price if quote and stock.total_shares else None,
        }

        # 财务指标 - 27个字段
        if indicator:
            # 估值指标
            result["pe_ttm"] = indicator.pe_ttm  # 市盈率(TTM)
            result["pb"] = indicator.pb  # 市净率
            result["ps_ttm"] = getattr(indicator, 'ps_ttm', None)  # 市销率(TTM)
            result["ev_ebitda"] = getattr(indicator, 'ev_ebitda', None)  # EV/EBITDA
            result["pcf"] = getattr(indicator, 'pcf', None)  # 市现率

            # 盈利能力指标
            result["roe"] = indicator.roe  # 净资产收益率
            result["roa"] = getattr(indicator, 'roa', None)  # 总资产收益率
            result["gross_margin"] = indicator.gross_margin  # 毛利率
            result["net_margin"] = getattr(indicator, 'net_margin', None)  # 净利率
            result["operating_margin"] = getattr(indicator, 'operating_margin', None)  # 营业利润率

            # 成长性指标
            result["revenue_growth_3y"] = indicator.revenue_growth_3y  # 3年营收复合增长率
            result["profit_growth_3y"] = getattr(indicator, 'profit_growth_3y', None)  # 3年利润复合增长率
            result["revenue_growth_5y"] = getattr(indicator, 'revenue_growth_5y', None)  # 5年营收复合增长率
            result["profit_growth_5y"] = getattr(indicator, 'profit_growth_5y', None)  # 5年利润复合增长率

            # 偿债能力指标
            result["current_ratio"] = getattr(indicator, 'current_ratio', None)  # 流动比率
            result["quick_ratio"] = getattr(indicator, 'quick_ratio', None)  # 速动比率
            result["debt_ratio"] = round(indicator.debt_to_equity * 100, 2) if indicator and indicator.debt_to_equity else None  # 资产负债率(%)
            result["interest_coverage"] = getattr(indicator, 'interest_coverage', None)  # 利息保障倍数

            # 其他指标
            result["report_date"] = indicator.report_date
        else:
            # 如果没有财务数据，填充None
            result.update({
                "pe_ttm": None,
                "pb": None,
                "ps_ttm": None,
                "ev_ebitda": None,
                "pcf": None,
                "roe": None,
                "roa": None,
                "gross_margin": None,
                "net_margin": None,
                "operating_margin": None,
                "revenue_growth_3y": None,
                "profit_growth_3y": None,
                "revenue_growth_5y": None,
                "profit_growth_5y": None,
                "current_ratio": None,
                "quick_ratio": None,
                "debt_ratio": None,
                "interest_coverage": None,
                "report_date": None,
            })

        return result


class ReferenceService:
    """参考数据服务 - 行业对比、同行分析、历史趋势、信息源"""

    @staticmethod
    def get_sector_comparison(db: Session, symbol: str):
        """获取股票与行业板块的对比数据"""
        stock = db.query(Stock).filter(Stock.symbol == symbol).first()
        if not stock:
            return None

        # 获取当前股票的最新财务指标
        current_indicator = db.query(FinancialIndicator).filter(
            FinancialIndicator.symbol == symbol
        ).order_by(desc(FinancialIndicator.report_date)).first()

        if not current_indicator:
            return None

        # 查询同板块所有股票的最新财务指标
        sector_stocks = db.query(Stock).filter(Stock.sector == stock.sector).all()

        # 获取每只股票的最新财务指标
        sector_indicators = []
        for s in sector_stocks:
            ind = db.query(FinancialIndicator).filter(
                FinancialIndicator.symbol == s.symbol
            ).order_by(desc(FinancialIndicator.report_date)).first()
            if ind:
                sector_indicators.append((s, ind))

        if not sector_indicators:
            return None

        # 定义需要对比的指标
        # lower_is_better: pe_ttm, pb, ps_ttm, debt_to_equity
        # higher_is_better: roe, gross_margin, net_margin, operating_margin, revenue_growth_3y
        metrics_config = {
            "pe_ttm": {"label": "市盈率(TTM)", "lower_is_better": True},
            "pb": {"label": "市净率", "lower_is_better": True},
            "ps_ttm": {"label": "市销率(TTM)", "lower_is_better": True},
            "roe": {"label": "净资产收益率", "lower_is_better": False},
            "gross_margin": {"label": "毛利率", "lower_is_better": False},
            "net_margin": {"label": "净利率", "lower_is_better": False},
            "operating_margin": {"label": "营业利润率", "lower_is_better": False},
            "revenue_growth_3y": {"label": "营收3年复合增长率", "lower_is_better": False},
            "debt_to_equity": {"label": "资产负债率", "lower_is_better": True},
        }

        result = {}
        for metric_key, config in metrics_config.items():
            current_value = getattr(current_indicator, metric_key, None)

            # 收集同板块该指标的有效值
            values = []
            for s, ind in sector_indicators:
                val = getattr(ind, metric_key, None)
                if val is not None:
                    values.append((s.name, s.symbol, val))

            if not values:
                result[metric_key] = {
                    "label": config["label"],
                    "current": current_value,
                    "sector_avg": None,
                    "sector_best": None,
                }
                continue

            # 计算板块平均值
            sector_avg = sum(v[2] for v in values) / len(values)

            # 找出板块最优
            if config["lower_is_better"]:
                best = min(values, key=lambda x: x[2])
            else:
                best = max(values, key=lambda x: x[2])

            result[metric_key] = {
                "label": config["label"],
                "current": current_value,
                "sector_avg": round(sector_avg, 2),
                "sector_best": {
                    "name": best[0],
                    "symbol": best[1],
                    "value": best[2],
                },
            }

        return result

    @staticmethod
    def get_peers(db: Session, symbol: str):
        """获取同细分行业同行对比"""
        stock = db.query(Stock).filter(Stock.symbol == symbol).first()
        if not stock:
            return None

        # 查询同细分行业的股票
        peers = db.query(Stock).filter(Stock.sub_sector == stock.sub_sector).all()

        result = []
        for s in peers:
            # 获取最新财务指标
            ind = db.query(FinancialIndicator).filter(
                FinancialIndicator.symbol == s.symbol
            ).order_by(desc(FinancialIndicator.report_date)).first()

            # 计算市值
            market_cap = None
            if s.total_shares and s.quote and s.quote.current_price:
                market_cap = s.total_shares * s.quote.current_price

            result.append({
                "symbol": s.symbol,
                "name": s.name,
                "pe_ttm": ind.pe_ttm if ind else None,
                "roe": ind.roe if ind else None,
                "gross_margin": ind.gross_margin if ind else None,
                "revenue_growth_3y": ind.revenue_growth_3y if ind else None,
                "debt_to_equity": ind.debt_to_equity if ind else None,
                "market_cap": market_cap,
            })

        # 按市值降序排列，限制8个
        result.sort(key=lambda x: x["market_cap"] if x["market_cap"] is not None else 0, reverse=True)
        return result[:8]

    @staticmethod
    def get_history_trend(db: Session, symbol: str):
        """获取历史指标趋势 - 与3年均值对比"""
        # 获取当前财务指标
        current_indicator = db.query(FinancialIndicator).filter(
            FinancialIndicator.symbol == symbol
        ).order_by(desc(FinancialIndicator.report_date)).first()

        if not current_indicator:
            return None

        # 查询历史指标
        historical_records = db.query(HistoricalIndicator).filter(
            HistoricalIndicator.symbol == symbol
        ).all()

        if not historical_records:
            return None

        # 定义需要计算趋势的指标
        metrics = [
            "pe_ttm", "pb", "ps_ttm", "roe", "roa",
            "gross_margin", "net_margin", "operating_margin",
            "revenue_growth_3y", "profit_growth_3y",
            "debt_to_equity", "current_ratio",
        ]

        result = {}
        for metric in metrics:
            current_value = getattr(current_indicator, metric, None)

            # 收集历史有效值
            hist_values = []
            for h in historical_records:
                val = getattr(h, metric, None)
                if val is not None:
                    hist_values.append(val)

            if not hist_values:
                result[metric] = {
                    "current": current_value,
                    "avg_3y": None,
                    "deviation_pct": None,
                }
                continue

            avg_3y = sum(hist_values) / len(hist_values)

            # 计算偏离度
            if avg_3y != 0:
                deviation_pct = round((current_value - avg_3y) / abs(avg_3y) * 100, 2) if current_value is not None else None
            else:
                deviation_pct = None

            result[metric] = {
                "current": current_value,
                "avg_3y": round(avg_3y, 2),
                "deviation_pct": deviation_pct,
            }

        return result

    @staticmethod
    def get_sources(db: Session, symbol: str, source_type: Optional[str] = None, page: int = 1, page_size: int = 10):
        """获取信息源列表（分页）"""
        query = db.query(InformationSource).filter(InformationSource.symbol == symbol)

        if source_type:
            query = query.filter(InformationSource.source_type == source_type)

        total = query.count()
        sources = query.order_by(desc(InformationSource.publish_time)) \
            .offset((page - 1) * page_size) \
            .limit(page_size) \
            .all()

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "list": [
                {
                    "id": s.id,
                    "source_type": s.source_type,
                    "title": s.title,
                    "source": s.source,
                    "publish_time": s.publish_time,
                    "summary": s.summary,
                    "sentiment": s.sentiment,
                }
                for s in sources
            ],
        }
