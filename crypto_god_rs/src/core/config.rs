use serde::Deserialize;
use std::path::Path;

#[derive(Debug, Clone, Deserialize)]
pub struct Config {
    pub solana_rpc_url: String,
    pub ethereum_rpc_url: String,
    pub telegram_bot_token: String,
    pub exchange_api_keys: Vec<ExchangeKey>,
    pub private_key: String,
}

#[derive(Debug, Clone, Deserialize)]
pub struct ExchangeKey {
    pub name: String,
    pub api_key: String,
    pub secret_key: String,
}

pub fn load_config() -> Result<Config, Box<dyn std::error::Error>> {
    dotenv::dotenv().ok();
    
    // Загрузка из переменных окружения или файла .env
    Ok(Config {
        solana_rpc_url: std::env::var("SOLANA_RPC_URL").unwrap_or_else(|_| "https://api.mainnet-beta.solana.com".to_string()),
        ethereum_rpc_url: std::env::var("ETHEREUM_RPC_URL").unwrap_or_else(|_| "https://eth-mainnet.g.alchemy.com/v2/demo".to_string()),
        telegram_bot_token: std::env::var("TELEGRAM_BOT_TOKEN").unwrap_or_default(),
        exchange_api_keys: vec![], // Заполняется из env
        private_key: std::env::var("PRIVATE_KEY").unwrap_or_default(),
    })
}
