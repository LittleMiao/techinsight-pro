# TechInsight Pro - 第一阶段功能扩展设计

## 概述

为股票详情页增加参考性内容，帮助用户做出更明智的投资判断。第一阶段聚焦于可基于现有数据快速实现的高价值功能。

## 功能清单

### 1. 行业对比（指标旁内联显示）

**描述**：在每个财务指标数值下方，显示行业均值和行业龙头信息。

**展示格式**：
```
PE-TTM: 32.15
行业均值: 45.2  龙头: 晶晨股份 18.3
```

**规则**：
- 行业均值 = 同 sector 所有股票该指标的算术平均值
- 行业龙头 = 该指标最优值（PE/PB等越低越好，ROE/毛利率等越高越好）
- 颜色标识：当前值优于均值显示绿色，劣于均值显示红色
- 涉及指标：PE-TTM、PB、PS-TTM、ROE、毛利率、净利率、营收增速、资产负债率

### 2. 同业对比表（独立卡片）

**描述**：新增"同业对比"卡片，展示同一 sub_sector 的公司核心指标并排对比。

**展示维度**：
- PE-TTM、ROE、毛利率、营收增速(3年)、资产负债率

**规则**：
- 选取同 sub_sector 的所有公司（最多显示8家）
- 当前股票行高亮
- 每列最优值加粗+绿色标注
- 按市值降序排列

### 3. 历史趋势（模拟数据）

**描述**：在每个指标旁显示"vs 3年均值"的偏离度。

**展示格式**：
```
PE-TTM: 32.15
vs 3年均值: -12% ↓（低于均值，绿色）
```

**规则**：
- 从模拟历史数据生成3年均值（当前值 × 随机波动系数）
- 偏离度 = (当前值 - 3年均值) / 3年均值 × 100%
- 正偏离显示红色（偏贵），负偏离显示绿色（偏便宜）

### 4. 信息源面板（可展开抽屉）

**描述**：页面右侧增加"信息源"按钮，点击展开侧边面板。

**分类Tab**：
- 财报：定期报告、业绩预告
- 研报：券商研究报告摘要
- 新闻：行业新闻、公司公告
- 博主观点：模拟博主的历史判断和观点

**每条信息包含**：
- 标题
- 来源（如：中信证券、东方财富、雪球）
- 时间戳
- 摘要（2-3句话）
- 相关性标签（如：利好、利空、中性）

**数据来源**：第一阶段使用模拟数据，预留真实API接口。

## 后端API设计

### 新增接口

1. `GET /api/v1/stocks/{symbol}/sector-comparison`
   - 返回：当前股票各指标 vs 行业均值 vs 行业龙头
   - 响应格式：
     ```json
     {
       "code": 200,
       "data": {
         "sector": "semiconductor",
         "metrics": {
           "pe_ttm": { "current": 32.15, "sector_avg": 45.2, "sector_best": { "name": "晶晨股份", "value": 18.3 } },
           "roe": { "current": 14.12, "sector_avg": 12.5, "sector_best": { "name": "澜起科技", "value": 22.1 } }
         }
       }
     }
     ```

2. `GET /api/v1/stocks/{symbol}/peers`
   - 返回：同 sub_sector 公司的核心指标对比表
   - 响应格式：
     ```json
     {
       "code": 200,
       "data": {
         "sub_sector": "存储芯片",
         "peers": [
           { "symbol": "603986.SH", "name": "兆易创新", "pe_ttm": 35.2, "roe": 15.1, ... },
           ...
         ]
       }
     }
     ```

3. `GET /api/v1/stocks/{symbol}/sources?type=report&page=1`
   - 返回：信息源列表（分页，按类型筛选）
   - 响应格式：
     ```json
     {
       "code": 200,
       "data": {
         "total": 25,
         "list": [
           { "id": 1, "type": "report", "title": "...", "source": "中信证券", "time": "2026-05-06", "summary": "...", "sentiment": "positive" }
         ]
       }
     }
     ```

4. `GET /api/v1/stocks/{symbol}/history-trend`
   - 返回：各指标 vs 3年均值的偏离度
   - 响应格式：
     ```json
     {
       "code": 200,
       "data": {
         "metrics": {
           "pe_ttm": { "current": 32.15, "avg_3y": 36.5, "deviation_pct": -12.0 },
           "roe": { "current": 14.12, "avg_3y": 12.8, "deviation_pct": 10.3 }
         }
       }
     }
     ```

## 数据模型变更

### 新增表

1. `information_sources` - 信息源表
   - id, symbol, type(report/news/analyst_opinion), title, source, publish_time, summary, sentiment, url, created_at

2. `historical_indicators` - 历史指标表（模拟）
   - id, symbol, report_date, pe_ttm, pb, roe, gross_margin, revenue_growth_3y, debt_to_equity, ...

### init_data.py 变更

- 为每只股票生成2-3年的历史指标数据（每季度一条）
- 为每只股票生成5-10条模拟信息源（财报/研报/新闻/博主观点混合）

## 前端组件设计

### 新增组件

1. `SectorComparison.vue` - 行业对比信息（内联在指标卡片中）
2. `PeerComparison.vue` - 同业对比表卡片
3. `SourcePanel.vue` - 信息源侧边抽屉
4. `HistoryTrend.vue` - 历史趋势标签（内联在指标卡片中）

### StockDetail.vue 改动

- 指标卡片中的每个指标增加行业对比和历史趋势子行
- 新增同业对比卡片区域
- 新增信息源浮动按钮和侧边抽屉

## 实施顺序

1. 后端：数据模型 + init_data 扩展
2. 后端：4个新API实现
3. 前端：行业对比内联展示
4. 前端：同业对比表卡片
5. 前端：历史趋势标签
6. 前端：信息源侧边抽屉
7. 联调测试 + 提交推送
