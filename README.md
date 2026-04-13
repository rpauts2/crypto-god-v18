# 🚀 Crypto God v18 - Ultimate Trading & Scanner Suite

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Rust](https://img.shields.io/badge/Rust-1.70+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

**Мощнейший инструмент для крипто-трейдинга, сканирования рынка и анализа сигналов**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Structure](#-structure) • [Results](#-results)

</div>

---

## 🔥 Features

### 🐍 Python Core
- **`crypto_god_v14.py`** - Основная торговая логика с расширенными индикаторами
- **`crypto_god_v9.py`** - Стабильная версия для продакшена
- **`scanner_v3_ru.py`** - Продвинутый сканер рынка с поддержкой русского языка
- **`ultimate_scanner.py`** - Ультимативный сканер для поиска лучших точек входа
- **`withdrawal_checker.py`** - Проверка доступности вывода средств на биржах

### 🦀 Rust Performance
- **`crypto_god_rs/`** - Высокопроизводительная версия на Rust для критичных операций
- **`rust_crypto_god/`** - Оптимизированные алгоритмы торговли

### 📊 Analytics & Reporting
- Генерация детальных отчетов в JSON и TXT форматах
- Логирование всех сессий с временными метками
- Анализ сигналов с историческими данными
- Проверка ликвидности и объемов

---

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Rust 1.70+ (для Rust-компонентов)
- pip & cargo

### Quick Start
```bash
# Clone repository
git clone git@github.com:rpauts2/crypto-god-v18.git
cd crypto-god-v18

# Install Python dependencies
pip install -r requirements.txt

# Build Rust components (optional)
cd crypto_god_rs && cargo build --release
```

---

## 💻 Usage

### Run Main Trading Bot
```bash
python crypto_god_v14.py --mode=production --leverage=10
```

### Start Market Scanner
```bash
python scanner_v3_ru.py --exchange=binance --interval=5m --limit=100
```

### Ultimate Scan
```bash
python ultimate_scanner.py --all-pairs --min-volume=1000000
```

### Check Withdrawals
```bash
python withdrawal_checker.py --exchanges=binance,bybit,okx
```

### Run Rust Version
```bash
cd crypto_god_rs
cargo run --release -- --fast-mode
```

---

## 📁 Project Structure

```
crypto-god-v18/
├── crypto_god_v14.py          # Основная версия торгового бота
├── crypto_god_v9.py           # Стабильная версия
├── scanner_v3_ru.py           # Сканер с русским интерфейсом
├── ultimate_scanner.py        # Ультимативный сканер
├── withdrawal_checker.py      # Проверка вывода средств
├── crypto_god_rs/             # Rust реализация
│   ├── src/
│   ├── Cargo.toml
│   └── target/
├── rust_crypto_god/           # Дополнительные Rust модули
├── quantum_scanner/           # Квантовый анализатор
├── *.json                     # Результаты сканирования
├── *.log                      # Логи сессий
├── *.txt                      # Текстовые отчеты
├── .gitignore                 # Git игноры
└── README.md                  # Этот файл
```

---

## 📈 Sample Results

### Recent Scans
- **RU Scan**: 100+ пар проанализировано, 15 сильных сигналов
- **Ultimate Scan**: Топ-20 монет по объему и волатильности
- **Withdrawal Check**: Все основные биржи доступны для вывода

### Output Files
- `ru_scan_results.json` - Детальные результаты RU скана
- `ultimate_results.json` - Итоги ультимативного сканирования
- `scan_results.json` - Последние данные сканера
- `withdrawal_check_*.json` - Статус вывода по биржам

---

## ⚙️ Configuration

Создайте файл `.env` для настройки:

```env
API_KEY=your_api_key
API_SECRET=your_api_secret
EXCHANGE=binance
LEVERAGE=10
RISK_LEVEL=medium
LOG_LEVEL=INFO
```

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## ⚠️ Disclaimer

**Внимание**: Торговля криптовалютой связана с высоким риском. Используйте этот инструмент на свой страх и риск. Авторы не несут ответственности за любые финансовые потери.

---

## 📞 Support

- GitHub Issues: [Create an issue](https://github.com/rpauts2/crypto-god-v18/issues)
- Email: support@cryptogod.dev

---

<div align="center">

**Made with ❤️ by Crypto God Team**

⭐ Star this repo if you find it useful!

</div>
