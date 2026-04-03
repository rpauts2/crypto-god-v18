# Crypto God v13.0 - Pure Rust HFT Trading Bot

## 🚀 Описание
Полностью переписанный на **100% Rust** высокочастотный крипто-сканер и торговый бот.
Включает 250+ модулей для поиска рыночных неэффективностей, MEV-атак, арбитража и снайпинга мемкоинов.

## 🔥 Возможности
- **Solana Sniper**: Авто-покупка новых пулов на Raydium в том же блоке
- **MEV Engine**: Сэндвич-атаки в Ethereum мемпуле через Flashbots
- **Liquidation King**: Детекция каскадов ликвидаций
- **P2P RF**: Арбитраж рублей (Сбер, Тинькофф, СБП)
- **DEX Arb**: Межбиржевой арбитраж (Uniswap, Curve, Raydium vs CEX)
- **Telegram Bot**: Уведомления о сигналах
- **SaaS Panel**: Веб-API для продажи сигналов

## 📦 Установка

### 1. Установка Rust
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

### 2. Клонирование и сборка
```bash
cd /workspace/crypto_god_rs
cargo build --release
```

### 3. Настройка (.env)
Создайте файл `.env` в корне проекта:
```env
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
ETHEREUM_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
PRIVATE_KEY=YOUR_WALLET_PRIVATE_KEY
```

## 🚀 Запуск

```bash
./target/release/crypto_god_rs
```

Или в режиме разработки:
```bash
cargo run --release
```

## 📊 Пример вывода
```
🚀 CRYPTO GOD v13.0 'PURE RUST GODMODE' — ЗАПУСК
Ядро: 100% Rust | Потоков: максимальное количество
🔍 Запуск 250+ сканеров рыночных неэффективностей...
🎯 Solana Sniper запущен (мониторинг Raydium)...
🥪 MEV Engine запущен (Solana + Ethereum)...
💀 Liquidation King запущен (мониторинг каскадов)...
💰 P2P Scanner (RF) запущен (Сбер, Тинькофф, СБП)...
🌐 SaaS Web Server запущен на порту 3000...
📱 Telegram Bot запущен...

🚨 ОБНАРУЖЕН НОВЫЙ ПУЛ НА RAYDIUM!
   Токен: $RUSTCOIN
   Ликвидность: $5000.00
   ДЕЙСТВИЕ: Покупка 1.0 SOL...

🥪 НАЙДЕНА SANDWICH АТАКА!
   Жертва: PEPE на сумму $50000
   Ожидаемая прибыль: $840.50
```

## 🌐 API Эндпоинты
- `GET /` - Информация об API
- `GET /api/v1/signals` - Последние сигналы
- `GET /api/v1/stats` - Статистика работы

## ⚠️ Предупреждение
Используйте на свой страх и риск. Торговля криптовалютой связана с высоким риском потери средств.
Этот софт предоставлен "как есть" без каких-либо гарантий.

## 📄 Лицензия
MIT
