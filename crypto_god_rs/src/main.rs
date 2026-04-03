mod core;
mod scanners;
mod bot;
mod web;
mod utils;

use log::{info, error};
use std::sync::Arc;
use tokio::sync::RwLock;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Инициализация логгера
    env_logger::init_from_env(env_logger::Env::default().default_filter_or("info"));

    info!("🚀 CRYPTO GOD v13.0 'PURE RUST GODMODE' — ЗАПУСК");
    info!("Ядро: 100% Rust | Потоков: максимальное количество");

    // Загрузка конфигурации
    let config = Arc::new(RwLock::new(core::config::load_config()?));
    
    // Инициализация общих состояний
    let state = Arc::new(utils::state::AppState::new(config.clone()).await);

    // Запуск всех модулей параллельно
    let mut tasks = vec![];

    // 1. Сканеры (250+ потоков)
    tasks.push(tokio::spawn(scanners::run_all_scanners(state.clone())));

    // 2. Telegram Бот
    tasks.push(tokio::spawn(bot::run_telegram_bot(state.clone())));

    // 3. SaaS Веб-сервер
    tasks.push(tokio::spawn(web::run_saas_server(state.clone())));

    // 4. MEV Движок (Solana + Ethereum)
    tasks.push(tokio::spawn(scanners::mev::run_mev_engine(state.clone())));

    // 5. Solana Sniper
    tasks.push(tokio::spawn(scanners::solana_sniper::run_solana_sniper(state.clone())));

    info!("✅ Все модули запущены. Система работает в режиме 24/7.");
    
    // Ожидание завершения всех задач (бесконечный цикл)
    for task in tasks {
        if let Err(e) = task.await {
            error!("❌ Критическая ошибка в модуле: {:?}", e);
        }
    }

    Ok(())
}
