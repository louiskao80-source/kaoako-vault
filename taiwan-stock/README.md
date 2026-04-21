# TWSE 台灣股票資料

## 📁 資料夾結構

```
taiwan-stock/
├── README.md                    # 本說明文件
├── data/                        # 原始數據
│   ├── raw/                     # 原始日線數據
│   │   ├── twse_2330_20260421.json  # 台積電
│   │   ├── twse_1216_20260421.json  # 聯發科
│   │   ├── twse_2303_20260421.json  # 台達電
│   │   └── twse_9925_20260421.json  # 鴻海
│   └── processed/               # 處理後數據
│       ├── twse_2330_20260421_processed.json
│       ├── twse_1216_20260421_processed.json
│       ├── twse_2303_20260421_processed.json
│       └── twse_9925_20260421_processed.json
├── reports/                     # 分析報告
│   ├── twse_report_2330_20260421.md  # 台積電
│   ├── twse_report_1216_20260421.md  # 聯發科
│   ├── twse_report_2303_20260421.md  # 台達電
│   ├── twse_report_9925_20260421.md  # 鴻海
│   └── twse_report_2330_20260420.md  # 台積電 (舊)
├── notes/                       # 觀察筆記
│   ├── twse_2330.md  # 台積電
│   ├── twse_1216.md  # 聯發科
│   ├── twse_2303.md  # 台達電
│   └── twse_9925.md  # 鴻海
└── scripts/                     # 分析腳本
    └── twse-analyzer.py         # 主分析腳本
```

## 📊 追蹤個股

| 代碼 | 名稱 | 產業 |
|------|------|------|
| 2330 | 台積電 (TSMC) | 半導體 |
| 1216 | 聯發科 (MediaTek) | 半導體 |
| 2303 | 台達電 (Delta) | 電源管理 |
| 9925 | 鴻海 (Foxconn) | 電子代工 |

## 📅 自動化

- **Cron Job ID**: `5a57857add7a`
- **執行時間**: 每日 09:00
- **腳本路徑**: `scripts/twse-analyzer.py`

## 📖 相關文件

- [../memory-summary.md](../../memory-summary.md) - 記憶摘要
- [../context/02-stock-analysis.md](../../context/02-stock-analysis.md) - 股票分析框架
