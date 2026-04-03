use crate::utils::state::AppState;
use log::{info, error};
use std::sync::Arc;
use teloxide::prelude::*;
use teloxide::types::Me;

pub async fn run_telegram_bot(state: Arc<AppState>) {
    info!("📱 Telegram Bot запущен...");
    
    let token = std::env::var("TELEGRAM_BOT_TOKEN").unwrap_or_else(|_| "DEMO_TOKEN".to_string());
    
    if token == "DEMO_TOKEN" {
        info!("⚠️ Токен не установлен, бот работает в демо-режиме (симуляция)");
        
        // Демо-режим: симуляция отправки уведомлений
        let mut interval = tokio::time::interval(tokio::time::Duration::from_secs(15));
        loop {
            interval.tick().await;
            info!("📩 [TELEGRAM] Симуляция отправки уведомления подписчикам (@CryptoGodVIP)...");
            info!("   Сообщение: '🚀 Новый сигнал: SOL SNIPE +450%!'");
        }
    } else {
        // Реальный режим
        let bot = Bot::new(token);
        
        // Обработчик команд
        let handler = Update::filter_message()
            .branch(dptree::endpoint(|bot: Bot, msg: Message| async move {
                if let Some(text) = msg.text() {
                    match text {
                        "/start" => bot.send_message(msg.chat.id, "🚀 Crypto God Bot активирован!\nИспользуйте /signals для получения последних сигналов.").await?,
                        "/signals" => bot.send_message(msg.chat.id, "📊 Активные сигналы:\n1. SOL SNIPE +450%\n2. BTC LIQUIDATION SHORT\n3. P2P USDT/RUB 1.02%").await?,
                        _ => bot.send_message(msg.chat.id, "Команды: /start, /signals").await?,
                    }
                }
                Ok::<_, Box<dyn std::error::Error + Send + Sync>>(())
            }));

        Dispatcher::builder(bot, handler)
            .enable_ctrlc_handler()
            .build()
            .dispatch()
            .await;
    }
}
