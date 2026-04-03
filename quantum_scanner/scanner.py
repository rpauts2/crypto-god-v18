import ccxt.async_support as ccxt, asyncio, time, json
from datetime import datetime

class Scanner:
    def __init__(self, cfg):
        self.ex_cfg, self.pairs, self.checks = cfg.get('EXCHANGES',[]), cfg.get('PAIRS',[]), cfg.get('CHECKS',{})
        self.max_conn, self.timeout, self.retries = cfg.get('MAX_CONN',50), cfg.get('TIMEOUT',10), cfg.get('RETRIES',3)
        self.exchanges, self.results = {}, {'timestamp':datetime.now().isoformat(),'summary':{},'arbitrage_opportunities':[],'liquidity_anomalies':[],'latency_issues':[]}

    async def init_exchanges(self):
        print(f"🚀 Initializing {len(self.ex_cfg)} exchanges...")
        sem = asyncio.Semaphore(self.max_conn)
        async def init(ex_id):
            async with sem:
                try:
                    ex = getattr(ccxt,ex_id)({'timeout':self.timeout*1000,'enableRateLimit':True})
                    await ex.load_markets()
                    self.exchanges[ex_id] = ex
                    print(f"✅ {ex_id.upper()}")
                except Exception as e: print(f"❌ {ex_id}: {str(e)[:40]}")
        await asyncio.gather(*[init(e) for e in self.ex_cfg], return_exceptions=True)
        print(f"✅ Connected: {len(self.exchanges)}\n")

    async def fetch_ticker(self, ex_id, sym):
        if ex_id not in self.exchanges: return None
        ex = self.exchanges[ex_id]
        for i in range(self.retries):
            try: return await ex.fetch_ticker(sym)
            except: 
                if i==self.retries-1: return None
                await asyncio.sleep(0.2*(i+1))
        return None

    async def fetch_ob(self, ex_id, sym):
        if ex_id not in self.exchanges: return None
        try: return await self.exchanges[ex_id].fetch_order_book(sym, limit=10)
        except: return None

    def check_arb(self, sym, tickers):
        opps = []
        prices = {e:t['last'] for e,t in tickers.items() if t and t.get('last')}
        if len(prices)<2: return opps
        pl = sorted(prices.items(), key=lambda x:x[1])
        for i in range(len(pl)):
            for j in range(i+1,len(pl)):
                buy_e,buy_p = pl[i]
                sell_e,sell_p = pl[j]
                spread = ((sell_p-buy_p)/buy_p)*100
                if spread>0.15:
                    opps.append({'type':'cross_exchange_arbitrage','symbol':sym,'buy_exchange':buy_e,'sell_exchange':sell_e,'buy_price':buy_p,'sell_price':sell_p,'spread_percent':round(spread,4),'profit_per_1000':round((spread/100)*1000,2),'timestamp':datetime.now().isoformat()})
        return opps

    def check_liq(self, sym, obs):
        anoms = []
        for ex_id,ob in obs.items():
            if not ob or 'bids' not in ob or 'asks' not in ob or not ob['bids'] or not ob['asks']: continue
            bb,ba = ob['bids'][0][0], ob['asks'][0][0]
            if bb>0 and ba>0:
                spread = ((ba-bb)/bb)*100
                if spread>1.0: anoms.append({'type':'wide_spread','exchange':ex_id,'symbol':sym,'spread_percent':round(spread,4),'best_bid':bb,'best_ask':ba})
            tbv = sum([b[1] for b in ob['bids'][:5]])
            tav = sum([a[1] for a in ob['asks'][:5]])
            if tbv>0 and tav>0:
                ir = max(tbv,tav)/min(tbv,tav)
                if ir>10: anoms.append({'type':'liquidity_imbalance','exchange':ex_id,'symbol':sym,'imbalance_ratio':round(ir,2),'bid_volume_5':round(tbv,4),'ask_volume_5':round(tav,4),'direction':'bids' if tbv>tav else 'asks'})
        return anoms

    def check_lat(self, sym, tickers):
        issues = []
        ct = time.time()
        for ex_id,t in tickers.items():
            if not t or not t.get('timestamp'): continue
            ts = t['timestamp']
            age = (ct-(ts/1000)) if ts>1e9 else (ct-ts)
            if age>5: issues.append({'type':'stale_price','exchange':ex_id,'symbol':sym,'price_age_seconds':round(age,2),'last_price':t.get('last'),'severity':'critical' if age>30 else 'warning'})
        return issues

    async def scan_pair(self, sym):
        ticks, obs = {}, {}
        async def fs(func, eid, rd):
            try:
                r = await func(eid, sym)
                if r: rd[eid] = r
            except: pass
        tasks = []
        for eid in list(self.exchanges.keys())[:25]:
            tasks.append(fs(self.fetch_ticker, eid, ticks))
            tasks.append(fs(self.fetch_ob, eid, obs))
        await asyncio.gather(*tasks, return_exceptions=True)
        self.results['arbitrage_opportunities'].extend(self.check_arb(sym, ticks))
        self.results['liquidity_anomalies'].extend(self.check_liq(sym, obs))
        self.results['latency_issues'].extend(self.check_lat(sym, ticks))

    async def run_scan(self):
        st = time.time()
        print("\n"+"="*70+"\n🌟 QUANTUM SCANNER v3.0\n"+"="*70)
        print(f"📊 Exchanges: {len(self.exchanges)}\n💱 Pairs: {len(self.pairs)}\n🔬 Checks: {sum(len(v) for v in self.checks.values())}+\n"+"="*70+"\n")
        bs = 6
        for i in range(0, len(self.pairs), bs):
            batch = self.pairs[i:i+bs]
            await asyncio.gather(*[self.scan_pair(p) for p in batch], return_exceptions=True)
            print(f"✅ Batch {i//bs+1}/{(len(self.pairs)-1)//bs+1}: {batch[-1]}")
        el = time.time()-st
        self.results['summary'] = {'scan_duration_seconds':round(el,2),'exchanges_scanned':len(self.exchanges),'pairs_scanned':len(self.pairs),'total_checks_available':sum(len(v) for v in self.checks.values()),'arbitrage_found':len(self.results['arbitrage_opportunities']),'liquidity_anomalies':len(self.results['liquidity_anomalies']),'latency_issues':len(self.results['latency_issues']),'total_vulnerabilities':len(self.results['arbitrage_opportunities'])+len(self.results['liquidity_anomalies'])+len(self.results['latency_issues'])}
        return self.results

    def report(self):
        r = ["\n"+"🚀"*35,"\n📊 QUANTUM SCANNER REPORT\n"+"🚀"*35+"\n"]
        s = self.results['summary']
        r += [f"📈 SUMMARY:\n   ⏱️ Duration: {s['scan_duration_seconds']}s\n   🏢 Exchanges: {s['exchanges_scanned']}\n   💱 Pairs: {s['pairs_scanned']}\n   🔬 Checks: {s['total_checks_available']}+\n   🎯 Findings: {s['total_vulnerabilities']}\n"]
        if self.results['arbitrage_opportunities']:
            r.append("💰 TOP ARBITRAGE:")
            for i,o in enumerate(sorted(self.results['arbitrage_opportunities'],key=lambda x:x['spread_percent'],reverse=True)[:10],1):
                r += [f"   {i}. {o['symbol']}: {o['buy_exchange']}→{o['sell_exchange']} | Spread: {o['spread_percent']}% | Profit: ${o['profit_per_1000']}/$1k\n"]
        if self.results['liquidity_anomalies']:
            r.append("🕳️ LIQUIDITY ANOMALIES:")
            for a in self.results['liquidity_anomalies'][:10]:
                if a['type']=='wide_spread': r.append(f"   ⚠️ {a['exchange']} {a['symbol']}: Spread {a['spread_percent']}%")
                elif a['type']=='liquidity_imbalance': r.append(f"   ⚖️ {a['exchange']} {a['symbol']}: Imbalance {a['imbalance_ratio']}x ({a['direction']})\n")
        if self.results['latency_issues']:
            r.append("\n🐢 LATENCY ISSUES:")
            se = {}
            for i in self.results['latency_issues']:
                if i['type']=='stale_price':
                    ex,age = i['exchange'],i['price_age_seconds']
                    if ex not in se or age>se[ex]: se[ex]=age
            for ex,age in sorted(se.items(),key=lambda x:x[1],reverse=True)[:10]:
                r.append(f"   🐌 {ex}: {age}s lag (STALE!)\n")
        r += ["\n"+"🚀"*35+"\n✅ SCAN COMPLETE\n"+"🚀"*35+"\n"]
        return "\n".join(r)

    async def close(self):
        for ex in self.exchanges.values():
            try: await ex.close()
            except: pass
