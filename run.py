import csv
import time
import random
from curl_cffi import requests
import yfinance as yf

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.170 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/115.0.1901.203",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 OPR/101.0.0.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.170 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S916B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5897.77 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6_8) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15"
]

def get_session():
    s = requests.Session()
    s.headers.update({"User-Agent": random.choice(USER_AGENTS)})
    return s

with open("ghIn", newline="") as fin:
    reader = csv.DictReader(fin)
    symbols = [row["T"] for row in reader]

with open("ghOut", "w", newline="", encoding="utf-8") as fout:
    writer = csv.writer(fout)
    writer.writerow(["T","P1","P2","O","T1","T2","T3","V1","V2","V3","V4","C","S","I"])
    for sym in symbols:
        info = {}
        ticker = None
        for attempt in range(4):
            try:
                sess = get_session()
                yf.utils.requests = sess
                ticker = yf.Ticker(sym)
                info = ticker.info or {}
                break
            except Exception:
                if attempt == 0:
                    wait = random.uniform(3.4,3.7)
                elif attempt == 1:
                    wait = random.uniform(5.1,5.4)
                elif attempt == 2:
                    wait = random.uniform(6.8,7.1)
                else:
                    break
                time.sleep(wait)
        
        P1 = info.get("currentPrice","") or ""
        P2 = info.get("regularMarketPrice","") or ""
        O = info.get("numberOfAnalystOpinions","") or ""
        T1 = info.get("targetMeanPrice","") or ""
        T2 = info.get("targetMedianPrice","") or ""
        
        # Get analyst recommendations for 0m period
        T3 = ""
        if ticker is not None:
            try:
                # Check if recommendationTrend exists as a property
                if hasattr(ticker, 'recommendation_trend') and ticker.recommendation_trend is not None:
                    df = ticker.recommendation_trend
                    if not df.empty and 'period' in df.columns:
                        # Filter for 0m period
                        zero_m = df[df['period'] == '0m']
                        if not zero_m.empty:
                            # Sum all recommendation types
                            rec_cols = ['strongBuy', 'buy', 'hold', 'sell', 'strongSell']
                            existing_cols = [col for col in rec_cols if col in zero_m.columns]
                            if existing_cols:
                                T3 = int(zero_m[existing_cols].sum(axis=1).iloc[0])
            except Exception as e:
                # Fallback: try getting from info dict
                try:
                    rec_trend = info.get("recommendationTrend")
                    if rec_trend and isinstance(rec_trend, dict):
                        trend_list = rec_trend.get("trend", [])
                        for trend in trend_list:
                            if trend.get("period") == "0m":
                                total = (trend.get("strongBuy", 0) + trend.get("buy", 0) + 
                                        trend.get("hold", 0) + trend.get("sell", 0) + 
                                        trend.get("strongSell", 0))
                                T3 = total
                                break
                except:
                    pass
        
        V1 = info.get("averageDailyVolume10Day","") or ""
        V2 = info.get("averageVolume10days","") or ""
        V3 = info.get("averageDailyVolume3Month","") or ""
        V4 = info.get("averageVolume","") or ""
        C = info.get("marketCap","") or ""
        S = info.get("sector","") or ""
        I = info.get("industry","") or ""
        writer.writerow([sym, P1, P2, O, T1, T2, T3, V1, V2, V3, V4, C, S, I])
        time.sleep(random.uniform(1.7,2))
