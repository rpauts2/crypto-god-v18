import json
import asyncio
import ccxt.async_support as ccxt
from datetime import datetime

# Конфигурация
EXCHANGES_TO_CHECK = [
    'binance', 'kraken', 'bitfinex', 'kucoin', 'gateio', 'huobi', 
    'bitget', 'mexc', 'latoken', 'zebpay', 'btcturk', 'poloniex', 
    'lbank', 'hitbtc', 'bingx', 'upbit', 'bithumb', 'coinone', 
    'korbit', 'indodax', 'tokocrypto', 'wazirx', 'coindcx', 'bitbns'
]
PAIRS = ['BTC/USDT', 'ETH/USDT', 'DOGE/USDT', 'MATIC/USDT', 'XMR/USDT', 'SOL/USDT', 'AVAX/USDT', 'TON/USDT']
COINS_TO_CHECK = ['BTC', 'ETH', 'DOGE', 'MATIC', 'XMR', 'SOL', 'USDT', 'TON', 'AVAX', 'TRX']

async def check_withdrawals():
    results = []
    print('🚀 ЗАПУСК ПРОВЕРКИ ВЫВОДОВ И ЛИМИТОВ...')
    
    tasks = []
    for ex_id in EXCHANGES_TO_CHECK:
        try:
            exchange = getattr(ccxt, ex_id)({'enableRateLimit': True, 'timeout': 15000})
            tasks.append(check_exchange(exchange, ex_id))
        except Exception as e:
            print(f'❌ Ошибка инициализации {ex_id}: {e}')
            
    gathered = await asyncio.gather(*tasks, return_exceptions=True)
    
    for res in gathered:
        if isinstance(res, dict):
            results.append(res)
        elif isinstance(res, Exception):
            print(f'❌ Ошибка выполнения: {res}')
            
    return results

async def check_exchange(exchange, ex_id):
    data = {
        'exchange': ex_id,
        'status': 'OK',
        'wallets': {},
        'fees': {},
        'limits': {},
        'risks': []
    }
    
    try:
        # 1. Проверка статусов кошельков
        try:
            currencies = await exchange.fetch_currencies()
            for coin in COINS_TO_CHECK:
                if coin in currencies:
                    info = currencies[coin]
                    can_withdraw = info.get('withdraw', False)
                    can_deposit = info.get('deposit', False)
                    network_fee = info.get('fee', 'N/A')
                    
                    data['wallets'][coin] = {
                        'withdraw': can_withdraw,
                        'deposit': can_deposit,
                        'fee': str(network_fee)
                    }
                    
                    if not can_withdraw:
                        data['risks'].append(f'⛔ Вывод {coin} закрыт!')
                    
                    # Проверка высоких комиссий (порог $5 для примера)
                    if network_fee:
                        try:
                            fee_val = float(str(network_fee).replace(',', '.'))
                            if fee_val > 5:
                                data['risks'].append(f'💸 Высокая комиссия на вывод {coin}: {network_fee}')
                        except:
                            pass
        except Exception as e:
            data['risks'].append(f'Не удалось получить статус кошельков: {str(e)[:60]}')

        # 2. Проверка лимитов на ордера
        try:
            markets = await exchange.fetch_markets()
            for pair in PAIRS:
                # Ищем точное совпадение или похожую пару
                matched_pair = None
                for m_symbol in [m['symbol'] for m in markets]:
                    if pair == m_symbol or pair.replace('/USDT', '') in m_symbol and 'USDT' in m_symbol:
                        matched_pair = m_symbol
                        break
                
                if matched_pair:
                    market = next((m for m in markets if m['symbol'] == matched_pair), None)
                    if market:
                        limits = market.get('limits', {})
                        cost_limit = limits.get('cost', {})
                        amount_limit = limits.get('amount', {})
                        
                        min_cost = cost_limit.get('min', 0)
                        min_amount = amount_limit.get('min', 0)
                        
                        data['limits'][matched_pair] = {
                            'min_cost': min_cost, 
                            'min_amount': min_amount
                        }
                        
                        if min_cost and min_cost > 50:
                            data['risks'].append(f'📉 Высокий мин. ордер для {matched_pair}: ${min_cost}')
        except Exception as e:
            data['risks'].append(f'Ошибка получения лимитов: {str(e)[:60]}')
            
    except Exception as e:
        data['status'] = 'ERROR'
        data['risks'].append(f'Критическая ошибка API: {str(e)[:60]}')
    finally:
        await exchange.close()
        
    return data

async def main():
    start_time = datetime.now()
    report = await check_withdrawals()
    end_time = datetime.now()
    
    # Формирование итогового отчета
    final_report = {
        'scan_type': 'Withdrawal & Limits Check + Advanced Arb Validation',
        'timestamp': start_time.isoformat(),
        'duration': str(end_time - start_time),
        'exchanges_checked': len(report),
        'critical_findings': [],
        'summary': {
            'total_risks': 0,
            'exchanges_with_closed_withdrawals': 0,
            'exchanges_with_high_fees': 0,
            'exchanges_with_high_min_orders': 0
        },
        'detailed_data': report
    }
    
    risk_counts = {
        'closed_withdrawals': 0,
        'high_fees': 0,
        'high_min_orders': 0
    }
    
    for ex in report:
        if ex['risks']:
            for risk in ex['risks']:
                final_report['critical_findings'].append(f"{ex['exchange']}: {risk}")
                final_report['summary']['total_risks'] += 1
                
                if '⛔' in risk:
                    risk_counts['closed_withdrawals'] += 1
                elif '💸' in risk:
                    risk_counts['high_fees'] += 1
                elif '📉' in risk:
                    risk_counts['high_min_orders'] += 1

    final_report['summary']['exchanges_with_closed_withdrawals'] = risk_counts['closed_withdrawals']
    final_report['summary']['exchanges_with_high_fees'] = risk_counts['high_fees']
    final_report['summary']['exchanges_with_high_min_orders'] = risk_counts['high_min_orders']
    
    # Сохранение
    filename = f'withdrawal_check_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(final_report, f, indent=2, ensure_ascii=False)
        
    print('\n' + '='*70)
    print('📊 ОТЧЕТ ПО ПРОВЕРКЕ ВЫВОДОВ И ЛИМИТОВ')
    print('='*70)
    print(f'⏱ Время скана: {final_report["duration"]}')
    print(f'🏢 Бирж проверено: {len(report)}')
    print(f'⚠ Найдено рисков: {final_report["summary"]["total_risks"]}')
    print('-'*70)
    
    print('\n📈 СТАТИСТИКА:')
    print(f'  • Закрытые выводы: {risk_counts["closed_withdrawals"]} случаев')
    print(f'  • Высокие комиссии: {risk_counts["high_fees"]} случаев')
    print(f'  • Высокие мин. ордера: {risk_counts["high_min_orders"]} случаев')
    print('-'*70)
    
    if final_report['critical_findings']:
        print('\n🔥 ТОП ПРОБЛЕМ (Арбитраж невозможен или рискован):')
        for i, finding in enumerate(final_report['critical_findings'][:20], 1):
            print(f'{i}. {finding}')
        if len(final_report['critical_findings']) > 20:
            print(f'\n... и еще {len(final_report["critical_findings"]) - 20} проблем в файле {filename}')
    else:
        print('\n✅ Критических проблем с выводом не найдено (или API не вернул данные).')
        
    print('\n' + '-'*70)
    print('💡 СОВЕТЫ ПО ВЫСОКИМ СПРЕДАМ:')
    print('1. Latoken/Zebpay/BtcTurk/Indodax: Часто закрывают вывод при пампах.')
    print('2. Проверяйте P2P курсы: Спот может быть 500%, но P2P вход/выход съест 20%.')
    print('3. Лимиты: На мелких биржах мин. ордер может быть $50+, что убивает микро-арбитраж.')
    print('4. Верификация: На некоторых биржах (Upbit, Bithumb) нужен KYC для вывода.')
    print('5. Локальные ограничения: TRY, INR, KRW пары часто имеют капитал-контроль.')
    print('='*70)
    print(f'📁 Полный отчет сохранен в: {filename}')
    print('='*70)

if __name__ == '__main__':
    asyncio.run(main())
