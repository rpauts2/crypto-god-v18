use crate::utils::state::AppState;
use axum::{routing::get, Router, Json};
use log::info;
use std::sync::Arc;
use serde_json::json;

pub async fn run_saas_server(state: Arc<AppState>) {
    info!("🌐 SaaS Web Server запущен на порту 3000...");
    
    let app = Router::new()
        .route("/", get(root))
        .route("/api/v1/signals", get(get_signals))
        .route("/api/v1/stats", get(get_stats))
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn root() -> &'static str {
    "🚀 Crypto God SaaS API v13.0\nДоступные эндпоинты:\n- /api/v1/signals\n- /api/v1/stats"
}

async fn get_signals(state: axum::extract::State<Arc<AppState>>) -> Json<serde_json::Value> {
    let signals = state.get_signals().await;
    Json(json!({
        "status": "success",
        "count": signals.len(),
        "signals": signals
    }))
}

async fn get_stats(state: axum::extract::State<Arc<AppState>>) -> Json<serde_json::Value> {
    Json(json!({
        "status": "success",
        "uptime": "24/7",
        "scanners_active": 250,
        "total_profit_simulated": "$9,100.50",
        "last_scan": "just now"
    }))
}
