# TechInsight Pro

科技板块股票深度研究平台，支持博主风格蒸馏分析。

## 功能特性

- 📊 股票行情与财务数据展示
- 🤖 博主风格蒸馏与模拟分析
- 🔍 智能股票搜索
- 📈 多维度分析视角

## 技术栈

- **后端**: FastAPI + SQLAlchemy + SQLite
- **前端**: Vue3 + Element Plus + ECharts
- **数据源**: AKShare (A股数据)

## 快速开始

### 启动后端
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 启动前端
```bash
cd frontend
npm install
npm run dev
```

### 访问
- 前端: http://localhost:3000
- API文档: http://localhost:8000/docs

## 博主风格蒸馏

支持将投资博主的分析框架蒸馏为可复用的分析视角，包括：
- 选股标准与权重
- 决策流程
- 风险控制规则
- 回避模式

## License

MIT
