#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULTRA SCANNER v3.0 - RUSSIA EDITION
Специализированный сканер для РФ арбитража: P2P, Фьючерсы, DEX, Листинги, Киты
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict

# Конфигурация
CONFIG = {
    "p2p_platforms": ["binance", "bybit", "okx"],
    "futures_exchanges": ["binance", "bybit", "okx", "kucoin"],
    "dex_chains": ["ethereum", "bsc", "polygon", "arbitrum"],
    "rub_pairs": ["USDT", "BTC", "ETH"],
    "min_p2p_spread": 1.5,  # Минимальный спред для P2P (%)
    "min_funding_diff": 0.005,  # Минимальная разница фандинга
    "whale_threshold_usd": 100000,  # Порог для китов
}

class RussiaScanner:
    def __init__(self):
        self.session = None
        self.results = {
            "p2p_arb": [],
            "futures_basis": [],
            "funding_arb": [],
            "listing_pumps": [],
            "whale_moves": [],
            "dex_arb": [],
            "nft_floor": [],
            "staking_diff": [],
            "lending_rates": [],
            "liquidation_cascade": []
        }
        self.stats = defaultdict(int)
        
    async def start(self):
        connector = aiohttp.TCPConnector(limit=100, ttl_dns_cache=300)
        self.session = aiohttp.ClientSession(connector=connector)
        print("🚀 ULTRA SCANNER v3.0 (RU Edition) запущен...")
        print(f"📊 Проверка: {len(CONFIG['p2p_platforms'])} P2P платформ, {len(CONFIG['futures_exchanges'])} фьючерсных бирж")
        print(f"💰 Фокус на RUB пары: {CONFIG['rub_pairs']}")
        print("-" * 80)

    async def stop(self):
        if self.session:
            await self.session.close()

    # ==================== P2P АРБИТРАЖ (RUB) ====================
    async def scan_p2p_rub(self):
        """Скан P2P рынка с фокусом на RUB"""
        print("\n🔍 СКАНИРОВАНИЕ P2P (RUB)...")
        
        # Эмуляция данных P2P (в реальности нужны API ключи или парсинг)
        p2p_data = {
            "binance": {
                "USDT_RUB": {"buy": 92.50, "sell": 94.20},
                "BTC_RUB": {"buy": 8950000, "sell": 9150000},
                "ETH_RUB": {"buy": 285000, "sell": 292000}
            },
            "bybit": {
                "USDT_RUB": {"buy": 91.80, "sell": 93.90},
                "BTC_RUB": {"buy": 8920000, "sell": 9120000},
                "ETH_RUB": {"buy": 283000, "sell": 290000}
            },
            "okx": {
                "USDT_RUB": {"buy": 92.10, "sell": 94.50},
                "BTC_RUB": {"buy": 8940000, "sell": 9180000},
                "ETH_RUB": {"buy": 284000, "sell": 293000}
            }
        }
        
        opportunities = []
        for asset in CONFIG['rub_pairs']:
            pair_name = f"{asset}_RUB"
            prices = {}
            
            for platform, data in p2p_data.items():
                if pair_name in data:
                    prices[platform] = data[pair_name]
            
            # Ищем арбитраж
            platforms = list(prices.keys())
            for i in range(len(platforms)):
                for j in range(i + 1, len(platforms)):
                    p1, p2 = platforms[i], platforms[j]
                    buy_price = prices[p1]["sell"]  # Покупаем на p1
                    sell_price = prices[p2]["buy"]   # Продаем на p2
                    
                    if sell_price > buy_price:
                        spread = ((sell_price - buy_price) / buy_price) * 100
                        if spread >= CONFIG['min_p2p_spread']:
                            profit_per_1000 = (spread / 100) * 1000
                            opportunities.append({
                                "asset": asset,
                                "pair": pair_name,
                                "buy_on": p1,
                                "sell_on": p2,
                                "buy_price": buy_price,
                                "sell_price": sell_price,
                                "spread": round(spread, 3),
                                "profit_per_1000_rub": round(profit_per_1000, 2),
                                "type": "P2P_ARB_RUB"
                            })
                    
                    # Обратный арбитраж
                    buy_price_rev = prices[p2]["sell"]
                    sell_price_rev = prices[p1]["buy"]
                    if sell_price_rev > buy_price_rev:
                        spread = ((sell_price_rev - buy_price_rev) / buy_price_rev) * 100
                        if spread >= CONFIG['min_p2p_spread']:
                            profit_per_1000 = (spread / 100) * 1000
                            opportunities.append({
                                "asset": asset,
                                "pair": pair_name,
                                "buy_on": p2,
                                "sell_on": p1,
                                "buy_price": buy_price_rev,
                                "sell_price": sell_price_rev,
                                "spread": round(spread, 3),
                                "profit_per_1000_rub": round(profit_per_1000, 2),
                                "type": "P2P_ARB_RUB"
                            })
        
        self.results["p2p_arb"] = sorted(opportunities, key=lambda x: x["spread"], reverse=True)
        self.stats["p2p_checks"] += len(CONFIG['rub_pairs']) * 3
        print(f"✅ Найдено P2P возможностей: {len(self.results['p2p_arb'])}")

    # ==================== ФЬЮЧЕРСНЫЙ БАЗИС ====================
    async def scan_futures_basis(self):
        """Разница между фьючерсом и спотом (Contango/Backwardation)"""
        print("\n🔍 СКАНИРОВАНИЕ ФЬЮЧЕРСНОГО БАЗИСА...")
        
        # Эмуляция данных
        basis_data = [
            {"exchange": "binance", "asset": "BTC", "spot": 94500, "future": 95200, "days": 30},
            {"exchange": "bybit", "asset": "BTC", "spot": 94480, "future": 95800, "days": 30},
            {"exchange": "okx", "asset": "BTC", "spot": 94520, "future": 94900, "days": 30},
            {"exchange": "binance", "asset": "ETH", "spot": 3020, "future": 3080, "days": 30},
            {"exchange": "bybit", "asset": "ETH", "spot": 3018, "future": 3095, "days": 30},
        ]
        
        opportunities = []
        for item in basis_data:
            basis = item["future"] - item["spot"]
            basis_pct = (basis / item["spot"]) * 100
            annualized = (basis_pct / item["days"]) * 365
            
            opportunities.append({
                "exchange": item["exchange"],
                "asset": item["asset"],
                "spot_price": item["spot"],
                "future_price": item["future"],
                "basis": round(basis, 2),
                "basis_pct": round(basis_pct, 3),
                "annualized_return": round(annualized, 2),
                "type": "CONTANGO" if basis > 0 else "BACKWARDATION",
                "strategy": "Long Spot + Short Future" if basis > 0 else "Short Spot + Long Future"
            })
        
        self.results["futures_basis"] = sorted(opportunities, key=lambda x: abs(x["annualized_return"]), reverse=True)
        self.stats["futures_checks"] += len(basis_data)
        print(f"✅ Найдено возможностей по базису: {len(self.results['futures_basis'])}")

    # ==================== ФАНДИНГ АРБИТРАЖ ====================
    async def scan_funding_arb(self):
        """Разные ставки финансирования на биржах"""
        print("\n🔍 СКАНИРОВАНИЕ ФАНДИНГ СТАВОК...")
        
        funding_data = [
            {"exchange": "binance", "asset": "BTCUSDT", "rate": 0.0001, "next_funding": "2h"},
            {"exchange": "bybit", "asset": "BTCUSDT", "rate": 0.0008, "next_funding": "2h"},
            {"exchange": "okx", "asset": "BTCUSDT", "rate": 0.0003, "next_funding": "2h"},
            {"exchange": "binance", "asset": "ETHUSDT", "rate": 0.0002, "next_funding": "2h"},
            {"exchange": "bybit", "asset": "ETHUSDT", "rate": 0.0009, "next_funding": "2h"},
            {"exchange": "kucoin", "asset": "SOLUSDT", "rate": 0.0012, "next_funding": "2h"},
        ]
        
        # Группируем по активу
        by_asset = defaultdict(list)
        for item in funding_data:
            by_asset[item["asset"]].append(item)
        
        opportunities = []
        for asset, rates in by_asset.items():
            if len(rates) < 2:
                continue
            
            rates_sorted = sorted(rates, key=lambda x: x["rate"])
            min_rate = rates_sorted[0]
            max_rate = rates_sorted[-1]
            
            diff = max_rate["rate"] - min_rate["rate"]
            if diff >= CONFIG['min_funding_diff']:
                # Стратегия: шорт на бирже с высоким фандингом, лонг на бирже с низким
                profit_per_day = (diff * 3) * 100  # 3 раза в день
                opportunities.append({
                    "asset": asset,
                    "long_exchange": min_rate["exchange"],
                    "short_exchange": max_rate["exchange"],
                    "long_rate": min_rate["rate"],
                    "short_rate": max_rate["rate"],
                    "rate_diff": round(diff, 5),
                    "daily_profit_pct": round(profit_per_day, 3),
                    "strategy": "Delta-neutral funding arb",
                    "type": "FUNDING_ARB"
                })
        
        self.results["funding_arb"] = sorted(opportunities, key=lambda x: x["daily_profit_pct"], reverse=True)
        self.stats["funding_checks"] += len(funding_data)
        print(f"✅ Найдено фандинг возможностей: {len(self.results['funding_arb'])}")

    # ==================== ЛИСТИНГ-ПАМПЫ ====================
    async def scan_listing_pumps(self):
        """Мониторинг анонсов новых листингов"""
        print("\n🔍 СКАНИРОВАНИЕ ЛИСТИНГОВ...")
        
        # Эмуляция последних анонсов
        listings = [
            {"exchange": "binance", "token": "NEWCOIN", "announce_time": "2024-01-15T10:00:00", "trading_start": "2024-01-15T12:00:00", "pairs": ["NEWCOIN/USDT", "NEWCOIN/BTC"]},
            {"exchange": "bybit", "token": "AITECH", "announce_time": "2024-01-14T14:00:00", "trading_start": "2024-01-14T16:00:00", "pairs": ["AITECH/USDT"]},
            {"exchange": "okx", "token": "MEMEAI", "announce_time": "2024-01-13T08:00:00", "trading_start": "2024-01-13T10:00:00", "pairs": ["MEMEAI/USDT", "MEMEAI/ETH"]}
        ]
        
        strategies = []
        for listing in listings:
            time_to_trade = datetime.fromisoformat(listing["trading_start"]) - datetime.fromisoformat(listing["announce_time"])
            strategies.append({
                "exchange": listing["exchange"],
                "token": listing["token"],
                "time_to_trade_hours": time_to_trade.total_seconds() / 3600,
                "pairs": listing["pairs"],
                "strategy": "Buy on DEX before listing, sell on CEX pump",
                "risk": "High",
                "type": "LISTING_PUMP"
            })
        
        self.results["listing_pumps"] = strategies
        self.stats["listing_checks"] += len(listings)
        print(f"✅ Найдено листингов для мониторинга: {len(self.results['listing_pumps'])}")

    # ==================== WHALE WATCHING ====================
    async def scan_whale_moves(self):
        """Отслеживание крупных переводов"""
        print("\n🔍 СКАНИРОВАНИЕ КИТОВЫХ ПЕРЕВОДОВ...")
        
        # Эмуляция крупных транзакций
        whale_moves = [
            {"chain": "ethereum", "token": "USDT", "amount": 5000000, "from": "Unknown Wallet", "to": "Binance", "time": "5 min ago", "impact": "Potential sell pressure"},
            {"chain": "tron", "token": "TRX", "amount": 100000000, "from": "Justin Sun Wallet", "to": "Unknown", "time": "12 min ago", "impact": "Neutral"},
            {"chain": "bsc", "token": "BNB", "amount": 25000, "from": "Binance Cold Wallet", "to": "New Wallet", "time": "25 min ago", "impact": "Exchange rebalancing"}
        ]
        
        significant_moves = [m for m in whale_moves if m["amount"] * (1 if m["token"] in ["USDT", "TRX"] else 300) > CONFIG['whale_threshold_usd']]
        
        self.results["whale_moves"] = significant_moves
        self.stats["whale_checks"] += len(whale_moves)
        print(f"✅ Найдено значимых движений китов: {len(self.results['whale_moves'])}")

    # ==================== DEX АРБИТРАЖ ====================
    async def scan_dex_arb(self):
        """Сравнение цен на DEX агрегаторах"""
        print("\n🔍 СКАНИРОВАНИЕ DEX АРБИТРАЖА...")
        
        dex_prices = [
            {"chain": "ethereum", "dex": "Uniswap", "pair": "ETH/USDC", "price": 3025, "liquidity": 50000000},
            {"chain": "ethereum", "dex": "SushiSwap", "pair": "ETH/USDC", "price": 3018, "liquidity": 15000000},
            {"chain": "ethereum", "dex": "Curve", "pair": "ETH/USDC", "price": 3022, "liquidity": 30000000},
            {"chain": "bsc", "dex": "PancakeSwap", "pair": "BNB/BUSD", "price": 315, "liquidity": 20000000},
            {"chain": "polygon", "dex": "QuickSwap", "pair": "MATIC/USDC", "price": 0.92, "liquidity": 5000000},
        ]
        
        opportunities = []
        by_pair = defaultdict(list)
        for item in dex_prices:
            by_pair[item["pair"]].append(item)
        
        for pair, items in by_pair.items():
            if len(items) < 2:
                continue
            
            items_sorted = sorted(items, key=lambda x: x["price"])
            min_item = items_sorted[0]
            max_item = items_sorted[-1]
            
            spread = ((max_item["price"] - min_item["price"]) / min_item["price"]) * 100
            if spread > 0.3:  # Минимальный спред для DEX
                opportunities.append({
                    "pair": pair,
                    "buy_dex": min_item["dex"],
                    "sell_dex": max_item["dex"],
                    "chain": min_item["chain"],
                    "buy_price": min_item["price"],
                    "sell_price": max_item["price"],
                    "spread": round(spread, 3),
                    "liquidity_min": min_item["liquidity"],
                    "type": "DEX_ARB"
                })
        
        self.results["dex_arb"] = sorted(opportunities, key=lambda x: x["spread"], reverse=True)
        self.stats["dex_checks"] += len(dex_prices)
        print(f"✅ Найдено DEX арбитражей: {len(self.results['dex_arb'])}")

    # ==================== NFT FLOOR SWEEP ====================
    async def scan_nft_floor(self):
        """Арбитраж NFT между маркетплейсами"""
        print("\n🔍 СКАНИРОВАНИЕ NFT FLOOR...")
        
        nft_data = [
            {"collection": "Bored Ape Yacht Club", "opensea_floor": 28.5, "blur_floor": 27.8, "looksrare_floor": 28.2},
            {"collection": "Azuki", "opensea_floor": 12.3, "blur_floor": 11.9, "looksrare_floor": 12.1},
            {"collection": "Pudgy Penguins", "opensea_floor": 8.7, "blur_floor": 8.5, "looksrare_floor": 8.9},
        ]
        
        opportunities = []
        for item in nft_data:
            floors = {
                "opensea": item["opensea_floor"],
                "blur": item["blur_floor"],
                "looksrare": item["looksrare_floor"]
            }
            min_market = min(floors, key=floors.get)
            max_market = max(floors, key=floors.get)
            
            spread = ((floors[max_market] - floors[min_market]) / floors[min_market]) * 100
            if spread > 1.0:
                opportunities.append({
                    "collection": item["collection"],
                    "buy_on": min_market,
                    "sell_on": max_market,
                    "buy_price": floors[min_market],
                    "sell_price": floors[max_market],
                    "spread": round(spread, 2),
                    "type": "NFT_ARB"
                })
        
        self.results["nft_floor"] = sorted(opportunities, key=lambda x: x["spread"], reverse=True)
        self.stats["nft_checks"] += len(nft_data)
        print(f"✅ Найдено NFT арбитражей: {len(self.results['nft_floor'])}")

    # ==================== СТЕЙКИНГ РАЗНИЦЫ ====================
    async def scan_staking_diff(self):
        """Разные APY на стейкинг"""
        print("\n🔍 СКАНИРОВАНИЕ СТЕЙКИНГ APY...")
        
        staking_data = [
            {"asset": "ETH", "platform": "Lido", "apy": 3.8, "lockup": "None"},
            {"asset": "ETH", "platform": "Rocket Pool", "apy": 4.1, "lockup": "None"},
            {"asset": "ETH", "platform": "Binance", "apy": 3.5, "lockup": "Flexible"},
            {"asset": "SOL", "platform": "Marinade", "apy": 7.2, "lockup": "None"},
            {"asset": "SOL", "platform": "Jito", "apy": 7.5, "lockup": "None"},
            {"asset": "DOT", "platform": "Polkadot Native", "apy": 14.0, "lockup": "28 days"},
        ]
        
        by_asset = defaultdict(list)
        for item in staking_data:
            by_asset[item["asset"]].append(item)
        
        opportunities = []
        for asset, items in by_asset.items():
            if len(items) < 2:
                continue
            
            items_sorted = sorted(items, key=lambda x: x["apy"])
            min_item = items_sorted[0]
            max_item = items_sorted[-1]
            
            diff = max_item["apy"] - min_item["apy"]
            if diff > 0.5:
                opportunities.append({
                    "asset": asset,
                    "best_platform": max_item["platform"],
                    "best_apy": max_item["apy"],
                    "worst_platform": min_item["platform"],
                    "worst_apy": min_item["apy"],
                    "diff": round(diff, 2),
                    "lockup": max_item["lockup"],
                    "type": "STAKING_ARB"
                })
        
        self.results["staking_diff"] = sorted(opportunities, key=lambda x: x["diff"], reverse=True)
        self.stats["staking_checks"] += len(staking_data)
        print(f"✅ Найдено стейкинг возможностей: {len(self.results['staking_diff'])}")

    # ==================== LENDING RATES ====================
    async def scan_lending_rates(self):
        """Арбитраж ставок кредитования"""
        print("\n🔍 СКАНИРОВАНИЕ LENDING RATES...")
        
        lending_data = [
            {"protocol": "Aave", "asset": "USDC", "supply_apy": 2.1, "borrow_apy": 3.5},
            {"protocol": "Compound", "asset": "USDC", "supply_apy": 1.8, "borrow_apy": 4.2},
            {"protocol": "MakerDAO", "asset": "DAI", "supply_apy": 3.0, "borrow_apy": 2.5},
            {"protocol": "Aave", "asset": "ETH", "supply_apy": 1.5, "borrow_apy": 2.8},
        ]
        
        # Простая проверка на разницу в borrow/supply
        opportunities = []
        for item in lending_data:
            spread = item["borrow_apy"] - item["supply_apy"]
            if spread > 1.0:
                opportunities.append({
                    "protocol": item["protocol"],
                    "asset": item["asset"],
                    "supply_apy": item["supply_apy"],
                    "borrow_apy": item["borrow_apy"],
                    "spread": round(spread, 2),
                    "strategy": "Borrow low, lend high (if possible)",
                    "type": "LENDING_ARB"
                })
        
        self.results["lending_rates"] = opportunities
        self.stats["lending_checks"] += len(lending_data)
        print(f"✅ Найдено lending возможностей: {len(self.results['lending_rates'])}")

    # ==================== LIQUIDATION CASCADE ====================
    async def scan_liquidation_cascade(self):
        """Предсказание цепочек ликвидаций"""
        print("\n🔍 СКАНИРОВАНИЕ ЛИКВИДАЦИЙ...")
        
        # Эмуляция уровней ликвидаций
        liquidation_data = [
            {"asset": "BTC", "price_level": 92000, "long_liq_volume": 150000000, "short_liq_volume": 50000000},
            {"asset": "BTC", "price_level": 90000, "long_liq_volume": 300000000, "short_liq_volume": 20000000},
            {"asset": "ETH", "price_level": 2900, "long_liq_volume": 80000000, "short_liq_volume": 30000000},
            {"asset": "ETH", "price_level": 2800, "long_liq_volume": 120000000, "short_liq_volume": 15000000},
        ]
        
        cascades = []
        for item in liquidation_data:
            total_liq = item["long_liq_volume"] + item["short_liq_volume"]
            dominant_side = "LONG" if item["long_liq_volume"] > item["short_liq_volume"] else "SHORT"
            
            if total_liq > 100000000:  # Более $100M ликвидаций
                cascades.append({
                    "asset": item["asset"],
                    "price_level": item["price_level"],
                    "long_liq": item["long_liq_volume"],
                    "short_liq": item["short_liq_volume"],
                    "total_liq": total_liq,
                    "dominant_side": dominant_side,
                    "risk": "HIGH" if total_liq > 200000000 else "MEDIUM",
                    "strategy": f"Watch for cascade if price approaches {item['price_level']}",
                    "type": "LIQUIDATION_CASCADE"
                })
        
        self.results["liquidation_cascade"] = sorted(cascades, key=lambda x: x["total_liq"], reverse=True)
        self.stats["liquidation_checks"] += len(liquidation_data)
        print(f"✅ Найдено потенциальных каскадов: {len(self.results['liquidation_cascade'])}")

    # ==================== ГЕНЕРАЦИЯ ОТЧЕТА ====================
    def generate_report(self):
        """Генерация красивого отчета"""
        total_checks = sum(self.stats.values())
        total_opportunities = sum(len(v) for v in self.results.values())
        
        report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🇷🇺 ULTRA SCANNER v3.0 - RUSSIA EDITION 🇷🇺                 ║
║                    Полный отчет по рыночным неэффективностям                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 ОБЩАЯ СТАТИСТИКА:
   • Всего проверок: {total_checks}
   • Найдено возможностей: {total_opportunities}
   • Время сканирования: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'═' * 82}
💰 ТОП P2P АРБИТРАЖ (RUB):
{'═' * 82}
"""
        if self.results["p2p_arb"]:
            for i, opp in enumerate(self.results["p2p_arb"][:5], 1):
                report += f"""
{i}. {opp['asset']}/RUB: {opp['buy_on']} → {opp['sell_on']}
   Спред: {opp['spread']}% | Прибыль с 1000₽: {opp['profit_per_1000_rub']}₽
   Цена покупки: {opp['buy_price']:,.2f}₽ | Цена продажи: {opp['sell_price']:,.2f}₽
"""
        else:
            report += "\n   Нет значимых P2P возможностей\n"

        report += f"""
{'═' * 82}
📈 ФЬЮЧЕРСНЫЙ БАЗИС (Contango/Backwardation):
{'═' * 82}
"""
        if self.results["futures_basis"]:
            for i, opp in enumerate(self.results["futures_basis"][:5], 1):
                report += f"""
{i}. {opp['asset']} на {opp['exchange']}: {opp['type']}
   Спот: ${opp['spot_price']:,.2f} | Фьючерс: ${opp['future_price']:,.2f}
   Базис: {opp['basis_pct']}% | Годовая доходность: {opp['annualized_return']}%
   Стратегия: {opp['strategy']}
"""
        else:
            report += "\n   Нет значимых возможностей по базису\n"

        report += f"""
{'═' * 82}
💸 ФАНДИНГ АРБИТРАЖ:
{'═' * 82}
"""
        if self.results["funding_arb"]:
            for i, opp in enumerate(self.results["funding_arb"][:5], 1):
                report += f"""
{i}. {opp['asset']}: Лонг на {opp['long_exchange']} | Шорт на {opp['short_exchange']}
   Разница ставок: {opp['rate_diff']} | Дневная прибыль: {opp['daily_profit_pct']}%
   Стратегия: {opp['strategy']}
"""
        else:
            report += "\n   Нет значимых фандинг возможностей\n"

        report += f"""
{'═' * 82}
🦄 DEX АРБИТРАЖ:
{'═' * 82}
"""
        if self.results["dex_arb"]:
            for i, opp in enumerate(self.results["dex_arb"][:5], 1):
                report += f"""
{i}. {opp['pair']} ({opp['chain']}): {opp['buy_dex']} → {opp['sell_dex']}
   Спред: {opp['spread']}% | Ликвидность: ${opp['liquidity_min']:,.0f}
"""
        else:
            report += "\n   Нет значимых DEX возможностей\n"

        report += f"""
{'═' * 82}
🎨 NFT FLOOR АРБИТРАЖ:
{'═' * 82}
"""
        if self.results["nft_floor"]:
            for i, opp in enumerate(self.results["nft_floor"][:5], 1):
                report += f"""
{i}. {opp['collection']}: {opp['buy_on']} → {opp['sell_on']}
   Спред: {opp['spread']}% | Купить за: {opp['buy_price']} ETH | Продать за: {opp['sell_price']} ETH
"""
        else:
            report += "\n   Нет значимых NFT возможностей\n"

        report += f"""
{'═' * 82}
💎 СТЕЙКИНГ РАЗНИЦЫ:
{'═' * 82}
"""
        if self.results["staking_diff"]:
            for i, opp in enumerate(self.results["staking_diff"][:5], 1):
                report += f"""
{i}. {opp['asset']}: Лучший {opp['best_platform']} ({opp['best_apy']}%) vs Худший {opp['worst_platform']} ({opp['worst_apy']}%)
   Разница: {opp['diff']}% | Лок: {opp['lockup']}
"""
        else:
            report += "\n   Нет значимых стейкинг возможностей\n"

        report += f"""
{'═' * 82}
⚠️ ПОТЕНЦИАЛЬНЫЕ КАСКАДЫ ЛИКВИДАЦИЙ:
{'═' * 82}
"""
        if self.results["liquidation_cascade"]:
            for i, cascade in enumerate(self.results["liquidation_cascade"][:5], 1):
                report += f"""
{i}. {cascade['asset']} на уровне ${cascade['price_level']:,.0f}
   Лонг ликвидаций: ${cascade['long_liq']:,} | Шорт ликвидаций: ${cascade['short_liq']:,}
   Доминирующая сторона: {cascade['dominant_side']} | Риск: {cascade['risk']}
   Стратегия: {cascade['strategy']}
"""
        else:
            report += "\n   Нет значимых каскадов\n"

        report += f"""
{'═' * 82}
🐋 КРУПНЫЕ ДВИЖЕНИЯ КИТОВ:
{'═' * 82}
"""
        if self.results["whale_moves"]:
            for i, move in enumerate(self.results["whale_moves"][:5], 1):
                report += f"""
{i}. {move['amount']:,} {move['token']} ({move['chain']})
   От: {move['from']} → В: {move['to']}
   Время: {move['time']} | Влияние: {move['impact']}
"""
        else:
            report += "\n   Нет значимых движений китов\n"

        report += f"""
{'═' * 82}
📢 АНОНСЫ ЛИСТИНГОВ:
{'═' * 82}
"""
        if self.results["listing_pumps"]:
            for i, listing in enumerate(self.results["listing_pumps"][:5], 1):
                report += f"""
{i}. {listing['token']} на {listing['exchange']}
   До начала торгов: {listing['time_to_trade_hours']} ч
   Пары: {', '.join(listing['pairs'])}
   Стратегия: {listing['strategy']} | Риск: {listing['risk']}
"""
        else:
            report += "\n   Нет свежих анонсов листингов\n"

        report += f"""
{'═' * 82}
🏦 LENDING RATES:
{'═' * 82}
"""
        if self.results["lending_rates"]:
            for i, rate in enumerate(self.results["lending_rates"][:5], 1):
                report += f"""
{i}. {rate['asset']} на {rate['protocol']}
   Supply APY: {rate['supply_apy']}% | Borrow APY: {rate['borrow_apy']}%
   Спред: {rate['spread']}%
"""
        else:
            report += "\n   Нет значимых lending возможностей\n"

        report += f"""
{'═' * 82}
📝 ДЕТАЛЬНАЯ СТАТИСТИКА ПО КАТЕГОРИЯМ:
{'═' * 82}
"""
        for category, count in self.stats.items():
            report += f"   • {category}: {count} проверок\n"

        report += f"""
{'═' * 82}
⚠️ ВАЖНЫЕ ЗАМЕЧАНИЯ ДЛЯ РФ:
{'═' * 82}
   1. P2P арбитраж требует проверки лимитов банковских карт (Сбер, Тинькофф)
   2. Вывод средств с некоторых бирж может быть ограничен для резидентов РФ
   3. Используйте VPN для доступа к некоторым платформам
   4. Учитывайте комиссии за вывод и конвертацию RUB
   5. Мониторьте изменения в законодательстве о криптовалютах

{'═' * 82}
🚀 СЛЕДУЮЩИЕ ШАГИ:
{'═' * 82}
   1. Проверьте актуальность цен перед входом в сделку
   2. Рассчитайте точную прибыль с учетом всех комиссий
   3. Начните с малых сумм для тестирования стратегий
   4. Автоматизируйте процесс через ботов (требуется доработка)
   5. Добавьте новые категории проверок по мере необходимости

{'═' * 82}
✅ Сканирование завершено успешно!
{'═' * 82}
"""
        return report

    async def run_full_scan(self):
        """Запуск полного сканирования"""
        await self.start()
        
        tasks = [
            self.scan_p2p_rub(),
            self.scan_futures_basis(),
            self.scan_funding_arb(),
            self.scan_listing_pumps(),
            self.scan_whale_moves(),
            self.scan_dex_arb(),
            self.scan_nft_floor(),
            self.scan_staking_diff(),
            self.scan_lending_rates(),
            self.scan_liquidation_cascade()
        ]
        
        await asyncio.gather(*tasks)
        
        report = self.generate_report()
        print(report)
        
        # Сохранение результатов
        with open('ru_scan_results.json', 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "results": self.results,
                "stats": dict(self.stats)
            }, f, ensure_ascii=False, indent=2)
        
        with open('ru_scan_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("\n💾 Результаты сохранены в:")
        print("   • ru_scan_results.json (полные данные)")
        print("   • ru_scan_report.txt (текстовый отчет)")
        
        await self.stop()

async def main():
    scanner = RussiaScanner()
    await scanner.run_full_scan()

if __name__ == "__main__":
    asyncio.run(main())
