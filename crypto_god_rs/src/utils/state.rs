use tokio::sync::RwLock;
use std::collections::VecDeque;
use crate::core::config::Config;

pub struct AppState {
    pub config: RwLock<Config>,
    pub signals: RwLock<VecDeque<String>>,
}

impl AppState {
    pub async fn new(config: RwLock<Config>) -> Self {
        AppState {
            config,
            signals: RwLock::new(VecDeque::with_capacity(100)),
        }
    }

    pub async fn send_signal(&self, signal: String) {
        let mut signals = self.signals.write().await;
        signals.push_front(signal);
        if signals.len() > 100 {
            signals.pop_back();
        }
    }

    pub async fn get_signals(&self) -> Vec<String> {
        let signals = self.signals.read().await;
        signals.iter().cloned().collect()
    }
}
