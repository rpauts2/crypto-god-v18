import asyncio, json
from datetime import datetime
from config import EXCHANGES, PAIRS, CHECKS, MAX_CONN, TIMEOUT, RETRIES
from scanner import Scanner

async def main():
    print("\n"+"🌟"*35+"\n   QUANTUM SCANNER v3.0\n   Maximum Coverage\n"+"🌟"*35+"\n")
    sc = Scanner({'EXCHANGES':EXCHANGES,'PAIRS':PAIRS,'CHECKS':CHECKS,'MAX_CONN':MAX_CONN,'TIMEOUT':TIMEOUT,'RETRIES':RETRIES})
    try:
        await sc.init_exchanges()
        if not sc.exchanges: print("❌ No exchanges"); return
        res = await sc.run_scan()
        print(sc.report())
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"scan_{ts}.json",'w') as f: json.dump(res,f,indent=2,default=str)
        print(f"💾 Saved: scan_{ts}.json")
        html = gen_html(res)
        with open(f"report_{ts}.html",'w') as f: f.write(html)
        print(f"📄 Saved: report_{ts}.html")
    except Exception as e: print(f"❌ Error: {e}")
    finally: await sc.close()

def gen_html(r):
    s = r.get('summary',{})
    arb = sorted(r.get('arbitrage_opportunities',[]),key=lambda x:x.get('spread_percent',0),reverse=True)[:15]
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Quantum Report</title>
<style>body{{font-family:Arial;background:linear-gradient(135deg,#667eea,#764ba2);padding:20px}}.c{{max-width:1100px;margin:0 auto;background:white;border-radius:15px;box-shadow:0 10px 40px rgba(0,0,0,0.3)}}.h{{background:linear-gradient(135deg,#2c3e50,#3498db);color:white;padding:25px;text-align:center;border-radius:15px 15px 0 0}}.st{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;padding:25px;background:#f8f9fa}}.stat{{background:white;padding:15px;border-radius:8px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.1)}}.sv{{font-size:1.8em;font-weight:bold;color:#3498db}}.sl{{color:#7f8c8d;font-size:0.8em;text-transform:uppercase}}.sec{{padding:25px}}.sec h2{{color:#2c3e50;border-bottom:3px solid #3498db;padding-bottom:8px}}.card{{background:#fff;border-left:5px solid #27ae60;padding:12px;margin:8px 0;border-radius:6px;box-shadow:0 2px 6px rgba(0,0,0,0.1)}}.card.h{{border-left-color:#e74c3c}}.card.m{{border-left-color:#f39c12}}table{{width:100%;border-collapse:collapse;margin-top:12px}}th,td{{padding:8px;text-align:left;border-bottom:1px solid #dee2e6}}th{{background:#3498db;color:white}}.bd{{display:inline-block;padding:2px 8px;border-radius:10px;font-size:0.75em;font-weight:bold}}.bw{{background:#fff3cd;color:#856404}}.br{{background:#f8d7da;color:#721c24}}</style></head><body>
<div class="c"><div class="h"><h1>🚀 Quantum Scanner Report</h1><p>{r.get('timestamp','N/A')}</p></div>
<div class="st"><div class="stat"><div class="sv">{s.get('exchanges_scanned',0)}</div><div class="sl">Exchanges</div></div><div class="stat"><div class="sv">{s.get('pairs_scanned',0)}</div><div class="sl">Pairs</div></div><div class="stat"><div class="sv">{s.get('total_checks_available',0)}+</div><div class="sl">Checks</div></div><div class="stat"><div class="sv">{s.get('total_vulnerabilities',0)}</div><div class="sl">Findings</div></div><div class="stat"><div class="sv">{s.get('arbitrage_found',0)}</div><div class="sl">Arb Ops</div></div><div class="stat"><div class="sv">{s.get('scan_duration_seconds',0)}s</div><div class="sl">Duration</div></div></div>
<div class="sec"><h2>💰 Top Arbitrage</h2>{''.join([f'<div class="card {"h" if o["spread_percent"]>2 else "m" if o["spread_percent"]>1 else ""}"><strong>{o["symbol"]}</strong>: {o["buy_exchange"]}→{o["sell_exchange"]} | Spread: {o["spread_percent"]:.4f}% | Profit: ${o["profit_per_1000"]}/$1k</div>' for o in arb])}</div>
<div class="sec"><h2>🕳️ Liquidity Anomalies</h2><table><tr><th>Exchange</th><th>Pair</th><th>Type</th><th>Details</th></tr>{''.join([f"<tr><td>{a['exchange']}</td><td>{a['symbol']}</td><td><span class=\"bd bw\">{a['type'].replace('_',' ').title()}</span></td><td>{a.get('spread_percent',a.get('imbalance_ratio',''))}</td></tr>" for a in r.get('liquidity_anomalies',[])[:15]])}</table></div>
<div class="sec"><h2>🐢 Latency Issues</h2><table><tr><th>Exchange</th><th>Max Lag</th><th>Severity</th></tr>{''.join([f"<tr><td>{e}</td><td>{l:.2f}s</td><td><span class=\"bd {'br' if l>30 else 'bw'}\">{'CRITICAL' if l>30 else 'WARNING'}</span></td></tr>" for e,l in sorted({i['exchange']:max(j['price_age_seconds'] for j in r.get('latency_issues',[]) if j['exchange']==i['exchange']) for i in r.get('latency_issues',[]) if i['type']=='stale_price'}.items(),key=lambda x:x[1],reverse=True)[:10]])}</table></div>
</div></body></html>"""

if __name__ == "__main__": asyncio.run(main())
