use crate::utils::state::AppState;
use log::info;
use std::sync::Arc;
use tokio::time::{Duration, interval};

pub async fn scan_p2p_arb(state: Arc<AppState>) {
    info!("💰 P2P Scanner (RF) запущен (Сбер, Тинькофф, СБП)...");
    let mut interval = interval(Duration::from_secs(10));

    loop {
        interval.tick().await;
        
        // Симуляция поиска арбитража
        info!("🇷🇺 НАЙДЕН P2P АРБИТРАЖ USDT/RUB!");
        info!("   Покупка: Bybit (Sber) - 92.50 RUB");
        info!("   Продажа: Binance (Tinkoff) - 93.45 RUB");
        info!("   Спред: 1.02%");
        
        state.send_signal("💰 P2P: USDT/RUB спред 1.02% (Bybit Sber -> Binance Tinkoff)".to_string()).await;
    }
}
