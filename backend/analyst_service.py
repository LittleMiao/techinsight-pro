"""
博主风格蒸馏服务层
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from models import AnalystFramework, AnalystJudgment, SimulatedAnalysis, Stock, FinancialIndicator, StockQuote
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
            if hasattr(indicator, 'debt_ratio') and indicator.debt_ratio and indicator.debt_ratio > 60:
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
            result["debt_ratio"] = getattr(indicator, 'debt_ratio', None)  # 资产负债率
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
