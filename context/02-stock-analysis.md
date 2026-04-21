# 台灣股市分析框架 v2.0

## 📊 分析維度

### 1. 大盤指數 (TWSE)
| 代碼 | 名稱 | 說明 |
|------|------|------|
| 0000 | 加權指數 | 台灣股市總體表現 |
| 0051 | 金融指數 | 金融業表現 |
| 0052 | 上證指數 | 工業類股 |
| 0053 | 生技指數 | 生技醫藥 |
| 0054 | 半導體指數 | 半導體產業 |

### 2. 重要指標
- **外資動向**: 淨買超/賣超 (張數、金額)
- **投信動向**: 淨買超/賣超 (張數、金額)
- **個股動能**: 成交量、漲跌幅、換手率
- **技術指標**: 
  - MACD (移動平均收斂發散)
  - RSI (相對強弱指標)
  - 均線 (5 日、10 日、20 日、60 日)
  - 支撐/壓力位

### 3. 重點產業
| 產業 | 代表個股 | 代碼 |
|------|---------|------|
| 半導體 | 台積電 | 2330 |
| | 聯發科 | 2454 |
| | 聯電 | 2303 |
| 電子 | 鴻海 | 2317 |
| | 廣達 | 2382 |
| | 仁寶 | 2324 |
| 金融 | 富邦金 | 2881 |
| | 台新金 | 2890 |
| | 中信金 | 2891 |
| 生技 | 生技類股 | - |

## 🎯 分析流程

### 步驟 1: 數據收集
```python
# 需要 API 或網頁爬蟲
- 大盤指數走勢
- 外資/投信動向
- 個股基本面 (PE、EPS、營收)
- 技術指標
```

### 步驟 2: 技術分析
- **趨勢判斷**: 上升/下降/震盪
- **支撐壓力**: 關鍵價位
- **成交量**: 量價關係
- **指標信號**: 買入/賣出/觀望

### 步驟 3: 基本面分析
- **產業趨勢**: 半導體週期、景氣循環
- **公司財報**: 營收成長、獲利能力
- **估值合理性**: PE、PEG、PB
- **風險因素**: 地緣政治、匯率、利率

### 步驟 4: 投資策略
- **短線**: 技術面操作 (1-4 週)
- **中線**: 產業趨勢 (1-6 個月)
- **長線**: 基本面配置 (6 個月以上)

## 📈 分析模板

### 每日分析報告模板
```markdown
## 日期：YYYY/MM/DD
### 大盤走勢
- 加權指數：XXXX 點 (+/-XX%)
- 成交量：XXXX 億股
- 漲跌家數：漲 XXX / 跌 XXX

### 外資動向
- 淨買超/賣超：XXX 張，XXX 億元

### 投信動向
- 淨買超/賣超：XXX 張，XXX 億元

### 重點個股
| 代碼 | 名稱 | 收盤 | 漲跌 | 成交量 |
|------|------|------|------|--------|
| 2330 | 台積電 | XXX | +XX% | XXX 張 |
| 2454 | 聯發科 | XXX | +XX% | XXX 張 |

### 技術分析
- 趨勢：上升/下降/震盪
- 支撐：XXX 點
- 壓力：XXX 點
- RSI: XX (超買/超賣/正常)

### 分析結論
- 操作建議：買入/賣出/觀望
- 目標價：XXX 點
- 停損點：XXX 點

### 風險提示
- XXX
- XXX
```

## 🛠️ 分析工具

### Python 分析庫
```python
# 核心庫
import pandas as pd
import numpy as np

# 技術分析
import ta  # Technical Analysis
import talib  # Technical Analysis Library

# 數據可視化
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# 網路請求
import requests
```

### 分析函數
```python
def calculate_technical_indicators(prices):
    """計算技術指標"""
    rsi = calculate_rsi(prices, period=14)
    macd = calculate_macd(prices)
    ma = calculate_moving_average(prices)
    return rsi, macd, ma

def analyze_trend(prices, period=20):
    """分析趨勢"""
    ma = calculate_moving_average(prices, period)
    if prices[-1] > ma[-1]:
        return "上升趨勢"
    elif prices[-1] < ma[-1]:
        return "下降趨勢"
    else:
        return "震盪"

def calculate_support_resistance(prices, window=20):
    """計算支撐壓力位"""
    high = np.percentile(prices[-window:], 80)
    low = np.percentile(prices[-window:], 20)
    return low, high
```

## 📋 數據來源

### 免費來源
- 台灣證券交易所 (https://www.twse.com.tw/)
- CMOL (https://www.cmol.tw/)
- Yahoo Finance (部分數據)

### 付費來源
- 台灣證券交易所 API (需要申請)
- 專業金融數據服務

## ⚠️ 注意事項

1. **數據延遲**: 部分數據有延遲
2. **風險管理**: 設定停損點 (建議 -5% 至 -10%)
3. **分散投資**: 不要全倉單一產業
4. **長期思維**: 避免短線投機
5. **財報風險**: 注意財報季波動

## 📝 使用建議

### 短線交易者
- 重視技術指標
- 設定嚴格停損
- 關注外資動向

### 長線投資者
- 重視基本面
- 分散投資
- 定期檢視組合

### 保守型投資者
- 低波動個股
- 高股息類股
- 定期定額

---

**版本**: 2.0  
**最後更新**: 2026/04/20  
**維護者**: Kaoako Vault
