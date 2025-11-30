-- Active: 1763465732781@@127.0.0.1@3306@stock_analysis_db
CREATE DATABASE IF NOT EXISTS stock_analysis_db;
USE stock_analysis_db;

CREATE TABLE stock_prices_clean (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    trade_date DATE NOT NULL,
    open_price DECIMAL(10,2),
    high_price DECIMAL(10,2),
    low_price DECIMAL(10,2),
    close_price DECIMAL(10,2),
    volume BIGINT,
    daily_return DECIMAL(12,6),
    year INT,
    month_name VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE stock_sector_map (
    symbol VARCHAR(20) PRIMARY KEY,
    sector VARCHAR(100)
);

CREATE TABLE stock_metrics_yearly (
    symbol VARCHAR(20),
    year INT,
    yearly_return DECIMAL(12,6),
    volatility DECIMAL(12,6),
    avg_price DECIMAL(10,2),
    avg_volume BIGINT,
    PRIMARY KEY (symbol, year)
);



CREATE TABLE IF NOT EXISTS correlation_matrix (
    symbol_a VARCHAR(20) NOT NULL,
    symbol_b VARCHAR(20) NOT NULL,
    correlation DECIMAL(9,6),
    computed_at DATE,
    PRIMARY KEY (symbol_a, symbol_b, computed_at)
);


CREATE TABLE IF NOT EXISTS cumulative_returns (
    symbol VARCHAR(20) NOT NULL,
    trade_date DATE NOT NULL,
    cumulative_return DECIMAL(12,6),
    PRIMARY KEY (symbol, trade_date)
);


CREATE TABLE IF NOT EXISTS monthly_returns (
    symbol VARCHAR(20) NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20),
    monthly_return DECIMAL(12,6),
    PRIMARY KEY (symbol, year, month)
);


CREATE TABLE IF NOT EXISTS sector_performance (
    sector VARCHAR(100) NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    avg_monthly_return DECIMAL(12,6),
    count_symbols INT,
    PRIMARY KEY (sector, year, month)
);

CREATE TABLE IF NOT EXISTS stock_data (
    symbol VARCHAR(20) NOT NULL,
    trade_date DATE NOT NULL,
    open_price DECIMAL(10,2),
    high_price DECIMAL(10,2),
    low_price DECIMAL(10,2),
    close_price DECIMAL(10,2),
    volume BIGINT,
    daily_return DECIMAL(12,6),
    year INT,
    month INT,
    month_name VARCHAR(20),
    PRIMARY KEY (symbol, trade_date)
);


CREATE TABLE IF NOT EXISTS volatility (
    symbol VARCHAR(20) NOT NULL,
    year INT NOT NULL,
    std_daily DECIMAL(12,6),
    annualized_volatility DECIMAL(12,6),
    PRIMARY KEY (symbol, year)
);


CREATE TABLE IF NOT EXISTS yearly_returns (
    symbol VARCHAR(20) NOT NULL,
    year INT NOT NULL,
    yearly_return DECIMAL(12,6),
    PRIMARY KEY (symbol, year)
);
