#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
台灣股市分析工具 v4.0 (公開 API 版)
功能：
1. 從 TWSE 公開 API 獲取真實股價
2. 技術分析 (RSI、MACD、趨勢)
3. 生成分析報告並儲存到 Vault
"""

import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# Vault 路徑
VAULT_ROOT = Path.home() / ".hermes" / "kaoako-vault"
DATA_RAW = VAULT_ROOT / "data" / "raw"
DATA_PROCESSED = VAULT_ROOT / "data" / "processed"
REPORTS_DIR = VAULT_ROOT / "reports"

class TWSEAnalyzer:
    """台灣股市分析器 (公開 API 版)"""
    
    def __init__(self):
        """初始化分析器 - 使用公開 API"""
        self.base_url = "https://openapi.twse.com.tw/v1"
        
    def get_stock_day_data(self, symbol: str, start_date: str = None, end_date: str = None):
        """從 TWSE 公開 API 獲取個股日線資料"""
        url = f"{self.base_url}/exchangeReport/STOCK_DAY_ALL"
        params = {"symbol": symbol, "repType": "L"}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        
        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if data and isinstance(data, list):
                    # 過濾出指定個股的數據
                    filtered_data = [item for item in data if item.get('Code') == symbol]
                    if filtered_data:
                        return filtered_data
        except Exception as e:
            print(f"查詢失敗：{e}")
        return None
    
    def get_market_index(self):
        """獲取市場指數"""
        url = f"{self.base_url}/exchangeReport/MI_INDEX"
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if data and isinstance(data, list):
                    # 查找加權指數 (發行量加權股價指數)
                    for item in data:
                        if item.get('指數') == '發行量加權股價指數':
                            return float(item.get('收盤指數', 0))
                    # 如果找不到，返回第一個
                    if data:
                        return float(data[0].get('收盤指數', 0))
        except Exception as e:
            print(f"市場指數查詢失敗：{e}")
        return 0
    
    def calculate_rsi(self, prices, period=14):
        """計算 RSI 指標"""
        if len(prices) < period + 1:
            return 50.0
        delta = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [max(0, d) for d in delta]
        losses = [max(0, -d) for d in delta]
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        if avg_loss == 0:
            return 100.0 if avg_gain > 0 else 50.0
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, prices):
        """計算 MACD 指標"""
        if len(prices) < 26:
            return {'macd': 0, 'signal': 0, 'histogram': 0}
        def ema(data, span):
            result = [data[0]]
            for i in range(1, len(data)):
                result.append((2 * data[i] - (span - 1) / (span + 1) * (result[-1] - data[i-1])))
            return result
        exp1 = ema(prices, 12)
        exp2 = ema(prices, 26)
        macd_line = [e1 - e2 for e1, e2 in zip(exp1, exp2)]
        signal_line = ema(macd_line, 9)
        return {
            'macd': macd_line[-1] if macd_line else 0,
            'signal': signal_line[-1] if signal_line else 0,
            'histogram': (macd_line[-1] - signal_line[-1]) if macd_line and signal_line else 0
        }
    
    def analyze_trend(self, prices):
        """分析趨勢"""
        if len(prices) < 20:
            return "數據不足"
        ma20 = sum(prices[-20:]) / 20
        current = prices[-1]
        if current > ma20 * 1.02:
            return "強上升趨勢"
        elif current > ma20:
            return "上升趨勢"
        elif current < ma20 * 0.98:
            return "下降趨勢"
        else:
            return "震盪"
    
    def calculate_support_resistance(self, prices, window=20):
        """計算支撐壓力位"""
        if len(prices) < window:
            window = len(prices)
        recent = prices[-window:]
        high = max(recent)
        low = min(recent)
        upper = sorted(prices[-window:])[int(0.8 * window)]
        lower = sorted(prices[-window:])[int(0.2 * window)]
        return {'high': high, 'low': low, 'resistance': upper, 'support': lower}
    
    def generate_report(self, symbol, data):
        """生成分析報告"""
        if not data:
            return "無數據"
        # 處理繁體中文欄位名
        closing_prices = []
        for item in data:
            price = item.get('收盤價') or item.get('ClosingPrice')
            if price:
                closing_prices.append(float(price))
        if not closing_prices:
            return "無有效股價數據"
        current_price = closing_prices[-1]
        if len(closing_prices) >= 2:
            prev_close = closing_prices[-2]
            change = current_price - prev_close
            change_pct = (change / prev_close) * 100 if prev_close else 0
        else:
            change = 0
            change_pct = 0
        rsi = self.calculate_rsi(closing_prices)
        ma = self.calculate_macd(closing_prices)
        trend = self.analyze_trend(closing_prices)
        sr = self.calculate_support_resistance(closing_prices)
        market_data = self.get_market_index()
        taiwan_weighted = 0
        if market_data:
            taiwan_weighted = market_data
        report = f"""## 台灣股市分析報告

### 個股資訊
- **代碼**: {symbol}
- **當前價**: {current_price:.2f} 元
- **漲跌**: {change:+.2f} ({change_pct:+.2f}%)
 - **數據筆數**: {len(closing_prices)} 筆
- **最新日期**: {data[-1].get('存續日', 'N/A') if data else 'N/A'}

### 市場指數
- **加權指數**: {taiwan_weighted:.2f} 點

### 技術指標
- **RSI (14)**: {rsi:.2f}
  - {self._interpret_rsi(rsi)}
- **MACD**:
  - MACD 線：{ma['macd']:.4f}
  - 信號線：{ma['signal']:.4f}
  - 柱狀圖：{ma['histogram']:.4f}
- **趨勢**: {trend}

### 支撐壓力
- **高點**: {sr['high']:.2f} 元
- **低點**: {sr['low']:.2f} 元
- **壓力位**: {sr['resistance']:.2f} 元
- **支撐位**: {sr['support']:.2f} 元

### 操作建議
- **趨勢**: {trend}
- **建議**: {self._get_recommendation(rsi, trend)}
- **停損**: {current_price * 0.95:.2f} 元 (-5%)
- **目標**: {current_price * 1.1:.2f} 元 (+10%)

---
*生成時間：{datetime.now().strftime('%Y/%m/%d %H:%M')}*
*資料來源：[TWSE 公開 API](https://openapi.twse.com.tw/v1)*
"""
        return report
    
    def _interpret_rsi(self, rsi):
        if rsi > 70:
            return "超買 (考慮賣出)"
        elif rsi < 30:
            return "超賣 (考慮買入)"
        else:
            return "正常區間"
    
    def _get_recommendation(self, rsi, trend):
        if trend == "上升趨勢" and rsi < 70:
            return "買入/持有"
        elif trend == "下降趨勢" and rsi > 30:
            return "賣出/觀望"
        elif rsi > 70:
            return "賣出"
        elif rsi < 30:
            return "買入"
        else:
            return "觀望"
    
    def save_data(self, symbol, data):
        """儲存原始數據"""
        DATA_RAW.mkdir(parents=True, exist_ok=True)
        date_str = datetime.now().strftime('%Y%m%d')
        filename = f"twse_{symbol}_{date_str}.json"
        filepath = DATA_RAW / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 原始數據已儲存：{filepath}")
    
    def save_processed_data(self, symbol, prices, analysis):
        """儲存處理後的數據"""
        DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
        date_str = datetime.now().strftime('%Y%m%d')
        filename = f"twse_{symbol}_{date_str}_processed.json"
        filepath = DATA_PROCESSED / filename
        data = {'symbol': symbol, 'prices': prices, 'analysis': analysis, 'timestamp': datetime.now().isoformat()}
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 處理後數據已儲存：{filepath}")


def main():
    """主程式"""
    print("=" * 60)
    print("台灣股市分析工具 v4.0 (公開 API 版)")
    print("=" * 60)
    analyzer = TWSEAnalyzer()
    symbols = ["2330", "1216", "2303", "9925"]
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
    print(f"\n📊 查詢個股：{', '.join(symbols)}")
    print(f"日期範圍：{start_date} 至 {end_date}")
    print("\n正在獲取市場指數...")
    taiwan_weighted = analyzer.get_market_index()
    if taiwan_weighted:
        print(f"✅ 加權指數：{taiwan_weighted:.2f} 點")
    else:
        print("✅ 加權指數：無法獲取")
    date_str = datetime.now().strftime('%Y%m%d')
    for symbol in symbols:
        print(f"\n{'='*60}")
        print(f"📈 分析個股：{symbol}")
        print("正在獲取數據...")
        data = analyzer.get_stock_day_data(symbol, start_date, end_date)
        if data and len(data) > 0:
            # 處理繁體中文欄位
            prices = []
            for item in data:
                price = item.get('收盤價') or item.get('ClosingPrice')
                if price:
                    prices.append(float(price))
            if prices:
                analyzer.save_data(symbol, data)
                rsi = analyzer.calculate_rsi(prices)
                ma = analyzer.calculate_macd(prices)
                trend = analyzer.analyze_trend(prices)
                sr = analyzer.calculate_support_resistance(prices)
                analysis = {'rsi': rsi, 'macd': ma, 'trend': trend, 'support_resistance': sr}
                analyzer.save_processed_data(symbol, prices, analysis)
                print("\n--- 分析報告 ---")
                report = analyzer.generate_report(symbol, data)
                print(report)
                REPORTS_DIR.mkdir(parents=True, exist_ok=True)
                filename = f"twse_report_{symbol}_{date_str}.md"
                filepath = REPORTS_DIR / filename
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"📄 報告已儲存：{filepath}")
                print("\n📝 更新 Obsidian 筆記...")
                update_obsidian_note(symbol, report)
    print("\n" + "=" * 60)
    print("✅ 分析完成！")
    print("=" * 60)


def update_obsidian_note(symbol, report):
    """更新 Obsidian 筆記"""
    note_path = VAULT_ROOT / "memory" / f"twse_{symbol}.md"
    note_path.parent.mkdir(parents=True, exist_ok=True)
    if note_path.exists():
        with open(note_path, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = f"# TWSE {symbol} 觀察筆記\n\n"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    content += f"\n---\n\n### {timestamp}\n\n{report}\n"
    with open(note_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ 已更新筆記：{note_path}")


if __name__ == "__main__":
    main()
