# 台灣股市分析工具使用說明

## 📋 功能介紹

台灣股市分析工具提供以下功能：
1. **個股資訊查詢** - 獲取即時股價、成交量
2. **技術分析** - RSI、MACD、移動平均線
3. **趨勢分析** - 自動判斷上升/下降/震盪
4. **支撐壓力** - 自動計算關鍵價位
5. **操作建議** - 根據技術指標提供建議

## 🚀 快速開始

### 1. 安裝依賴
```bash
pip install pandas numpy requests
```

### 2. 申請 TWSE API Key
1. 訪問 https://www.twse.com.tw/
2. 申請 API 開發者帳號
3. 獲取 API Key 和 App ID

### 3. 修改程式碼
```python
# 在 twse-analyzer.py 中修改
self.api_key = "YOUR_API_KEY"  # 填入你的 API Key
self.app_id = "YOUR_APP_ID"     # 填入你的 App ID
```

### 4. 執行分析
```bash
python twse-analyzer.py
```

## 📊 使用範例

### 查詢台積電
```bash
python twse-analyzer.py
```

### 查詢特定個股
編輯程式碼，修改 `symbol` 變數：
```python
symbol = "2454"  # 聯發科
symbol = "2881"  # 富邦金
symbol = "2317"  # 鴻海
```

## 📁 輸出檔案

分析報告會自動儲存為：
```
twse_report_2330_20260420.md
```

## 🎯 分析指標說明

### RSI (相對強弱指標)
- **> 70**: 超買 (考慮賣出)
- **< 30**: 超賣 (考慮買入)
- **30-70**: 正常區間

### 移動平均線
- **5 日**: 短線趨勢
- **10 日**: 短中期趨勢
- **20 日**: 中期趨勢
- **60 日**: 長期趨勢

### 趨勢判斷
- **強上升**: 股價 > MA20 * 1.02
- **上升**: 股價 > MA20
- **下降**: 股價 < MA20 * 0.98
- **震盪**: 其他情況

## ⚠️ 注意事項

1. **數據延遲**: API 數據可能有延遲
2. **風險管理**: 設定停損點 (建議 -5% 至 -10%)
3. **分散投資**: 不要全倉單一產業
4. **長期思維**: 避免短線投機

## 🛠️ 進階使用

### 自訂分析週期
```python
# 修改日期範圍
end_date = datetime.now().strftime('%Y%m%d')
start_date = (datetime.now() - pd.Timedelta(days=60)).strftime('%Y%m%d')
```

### 批量分析多個個股
```python
symbols = ["2330", "2454", "2881", "2317"]
for symbol in symbols:
    # 執行分析
    pass
```

## 📚 相關文件

- **分析框架**: `../context/02-stock-analysis.md`
- **知識庫**: `/home/hermes/.hermes/kaoako-vault/`

---

**版本**: 2.0  
**最後更新**: 2026/04/20
