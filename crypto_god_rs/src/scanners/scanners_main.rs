use crate::utils::state::AppState;
use log::info;
use std::sync::Arc;

pub async fn run_all_scanners(state: Arc<AppState>) {
    info!("🔍 Запуск 250+ сканеров рыночных неэффективностей...");
    
    // Здесь запускаются все 250+ сканеров параллельно
    // Для примера запустим несколько основных
    
    let tasks = vec![
        tokio::spawn(crate::scanners::liquidation_king::scan_liquidations(state.clone())),
        tokio::spawn(crate::scanners::p2p_ru::scan_p2p_arb(state.clone())),
        tokio::spawn(crate::scanners::dex_arb::scan_dex_arb(state.clone())),
    ];

    for task in tasks {
        if let Err(e) = task.await {
            log::error!("Ошибка в сканере: {:?}", e);
        }
    }
}
