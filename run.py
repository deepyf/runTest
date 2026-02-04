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
    writer.writerow(["T","P1","P2","O1","O2","T1","T2","V1","V2","V3","V4","C","S","I"])
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
        O1 = info.get("numberOfAnalystOpinions","") or ""
        
        O2 = ""
        if ticker is not None:
            try:
                rec_summary = ticker.recommendations_summary
                if rec_summary is not None and not rec_summary.empty:
                    zero_m_data = rec_summary[rec_summary['period'] == '0m']
                    if not zero_m_data.empty:
                        rec_cols = ['strongBuy', 'buy', 'hold', 'sell', 'strongSell']
                        total = 0
                        for col in rec_cols:
                            if col in zero_m_data.columns:
                                total += int(zero_m_data[col].iloc[0])
                        O2 = total
            except Exception:
                pass
        
        T1 = info.get("targetMeanPrice","") or ""
        T2 = info.get("targetMedianPrice","") or ""
        V1 = info.get("averageDailyVolume10Day","") or ""
        V2 = info.get("averageVolume10days","") or ""
        V3 = info.get("averageDailyVolume3Month","") or ""
        V4 = info.get("averageVolume","") or ""
        C = info.get("marketCap","") or ""
        S = info.get("sector","") or ""
        I = info.get("industry","") or ""
        writer.writerow([sym, P1, P2, O1, O2, T1, T2, V1, V2, V3, V4, C, S, I])
        time.sleep(random.uniform(1.7,2))
