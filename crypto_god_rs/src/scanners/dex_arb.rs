use crate::utils::state::AppState;
use log::info;
use std::sync::Arc;
use tokio::time::{Duration, interval};

pub async fn scan_dex_arb(state: Arc<AppState>) {
    info!("🌉 DEX Arbitrage Scanner запущен (Uniswap, Curve, Raydium)...");
    let mut interval = interval(Duration::from_secs(4));

    loop {
        interval.tick().await;
        
        // Симуляция поиска арбитража
        info!("🔁 НАЙДЕН DEX АРБИТРАЖ!");
        info!("   Пара: SOL/USDT");
        info!("   Buy: Raydium ($145.20)");
        info!("   Sell: Binance ($147.80)");
        info!("   Спред: 1.79%");
        
        state.send_signal("🌉 DEX Arb: SOL спред 1.79% (Raydium -> Binance)".to_string()).await;
    }
}
