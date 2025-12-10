# Data-Driven Stock Analysis: Organizing, Cleaning, and Visualizing Market Trends

A comprehensive stock market analysis project that extracts, cleans, stores, and visualizes stock data using Python, MySQL, Streamlit, and Power BI.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Visualizations](#visualizations)
- [Technologies Used](#technologies-used)
- [License](#license)

## 🎯 Overview

This project provides an end-to-end pipeline for stock market data analysis:

1. **Data Extraction**: Extract stock data from YAML files and convert to CSV format
2. **Data Loading**: Load cleaned data into a MySQL database for structured storage
3. **Data Analysis**: Perform various analyses including volatility, returns, and correlations
4. **Visualization**: Interactive dashboards using Streamlit and Power BI

## ✨ Features

- **YAML to CSV Conversion**: Automated extraction of stock data from YAML files
- **MySQL Database Integration**: Structured storage with comprehensive schema
- **Volatility Analysis**: Identify the most volatile stocks using standard deviation of daily returns
- **Cumulative Returns**: Track and compare stock performance over time
- **Sector-wise Performance**: Analyze average returns by sector
- **Correlation Heatmap**: Visualize relationships between stock prices
- **Monthly Gainers/Losers**: Identify top performing and underperforming stocks each month
- **Interactive Dashboard**: Real-time filtering and visualization with Streamlit
- **Power BI Reports**: Professional business intelligence reporting

## 📁 Project Structure

```
├── README.md                # Project documentation
├── extract_yaml.py          # Extract YAML data to CSV files
├── load_to_database.py      # Load CSV data into MySQL database
├── database_setup.sql       # SQL schema for database tables
├── analysis.py              # Stock analysis with matplotlib visualizations
├── streamlit_app.py         # Interactive Streamlit dashboard
└── Analysis data.pbix       # Power BI report file
```

## 📋 Prerequisites

- Python 3.8 or higher
- MySQL Server
- Power BI Desktop (for .pbix file)

### Python Dependencies

- pandas
- matplotlib
- mysql-connector-python
- pyyaml
- streamlit
- plotly
- numpy

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/R9696-12/Data-Driven-Stock-Analysis-Organizing-Cleaning-and-Visualizing-Market-Trends.git
   cd Data-Driven-Stock-Analysis-Organizing-Cleaning-and-Visualizing-Market-Trends
   ```

2. **Install Python dependencies**
   ```bash
   pip install pandas matplotlib mysql-connector-python pyyaml streamlit plotly numpy
   ```

3. **Set up the MySQL database**
   - Open MySQL and run the `database_setup.sql` script:
     ```sql
     source database_setup.sql;
     ```

4. **Configure file paths**
   - Update the file paths in `extract_yaml.py`, `load_to_database.py`, `analysis.py`, and `streamlit_app.py` to match your local data directory.

5. **Configure database connection**
   - Update the `DB_CONFIG` in `load_to_database.py` with your MySQL credentials.

## 📖 Usage

### Step 1: Extract Data from YAML Files

```bash
python extract_yaml.py
```

This script reads YAML files from your data folder and converts them to individual CSV files per stock symbol.

### Step 2: Load Data into MySQL Database

```bash
python load_to_database.py
```

This script:
- Loads all CSV files into the `stock_prices_clean` table
- Populates the `stock_sector_map` table with sector information
- Calculates and stores yearly metrics in `stock_metrics_yearly`

### Step 3: Run Analysis

```bash
python analysis.py
```

Generates matplotlib visualizations for:
- Top 10 most volatile stocks
- Cumulative returns over time
- Sector-wise performance
- Stock price correlation heatmap
- Monthly top gainers and losers

### Step 4: Launch Streamlit Dashboard

```bash
streamlit run streamlit_app.py
```

Access the interactive dashboard at `http://localhost:8501`

### Step 5: Power BI Report

Open `Analysis data.pbix` in Power BI Desktop for advanced business intelligence visualizations.

## 🗄️ Database Schema

The MySQL database includes the following tables:

| Table Name | Description |
|------------|-------------|
| `stock_prices_clean` | Daily stock price data with calculated returns |
| `stock_sector_map` | Mapping of stock symbols to sectors |
| `stock_metrics_yearly` | Yearly performance metrics per stock |
| `stock_data` | Base stock data with date information |
| `volatility` | Volatility calculations per stock/year |
| `yearly_returns` | Annual return calculations |
| `monthly_returns` | Monthly return calculations |
| `cumulative_returns` | Cumulative return tracking |
| `correlation_matrix` | Stock price correlations |
| `sector_performance` | Aggregated sector performance metrics |

## 📊 Visualizations

### Streamlit Dashboard Features

- **Price Trends**: Interactive line charts for stock closing prices
- **Volatility Analysis**: Bar charts showing annualized volatility
- **Cumulative Returns**: Track investment growth over time
- **Correlation Matrix**: Heatmap showing stock relationships
- **Top Gainers/Losers**: Monthly performance rankings
- **Latest Prices**: Current stock price summary

### Matplotlib Analysis

- Top 10 most volatile stocks (bar chart)
- Cumulative return comparison (line chart)
- Sector-wise average returns (bar chart)
- Stock correlation heatmap

## 🛠️ Technologies Used

- **Python**: Core programming language
- **Pandas**: Data manipulation and analysis
- **Matplotlib**: Static visualizations
- **Plotly**: Interactive charts in Streamlit
- **Streamlit**: Web-based dashboard
- **MySQL**: Relational database storage
- **PyYAML**: YAML file parsing
- **Power BI**: Business intelligence reporting

## 📄 License

This project is open source.