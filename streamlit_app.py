import streamlit as st
import pandas as pd
import os
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Stock Performance Dashboard", layout="wide")
st.title("📊 Stock Performance Dashboard")

# Load all CSV files from data_csv folder
data_folder = Path(r"C:\stock analysis\data_csv")
all_data = []

with st.spinner("Loading stock data..."):
    for csv_file in data_folder.glob("*.csv"):
        df = pd.read_csv(csv_file)
        # Add symbol column if Ticker is present
        if "Ticker" in df.columns and "symbol" not in df.columns:
            df["symbol"] = df["Ticker"]
        all_data.append(df)

    # Merge all data
    df = pd.concat(all_data, ignore_index=True)
    
    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

# Sidebar filters
st.sidebar.header("Filters")
selected_stocks = st.sidebar.multiselect(
    "Select Stocks",
    options=sorted(df["symbol"].unique()),
    default=sorted(df["symbol"].unique())[:5]
)

date_range = st.sidebar.date_input(
    "Date Range",
    value=(df["date"].min(), df["date"].max()),
    min_value=df["date"].min(),
    max_value=df["date"].max()
)

# Filter data
if len(date_range) == 2:
    mask = (df["date"] >= pd.to_datetime(date_range[0])) & (df["date"] <= pd.to_datetime(date_range[1]))
    if selected_stocks:
        mask = mask & (df["symbol"].isin(selected_stocks))
    filtered_df = df[mask].copy()
else:
    filtered_df = df[df["symbol"].isin(selected_stocks)].copy() if selected_stocks else df.copy()

# Overview metrics
st.header("📈 Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Records", f"{len(filtered_df):,}")
with col2:
    st.metric("Number of Stocks", filtered_df["symbol"].nunique())
with col3:
    st.metric("Date Range", f"{filtered_df['date'].min().date()} to {filtered_df['date'].max().date()}")
with col4:
    avg_volume = filtered_df["volume"].mean()
    st.metric("Avg Volume", f"{avg_volume:,.0f}")

# Tab layout
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Price Trends", 
    "📉 Volatility Analysis", 
    "💰 Cumulative Returns", 
    "🔗 Correlation", 
    "🏆 Top Gainers/Losers",
    "📋 Latest Prices"
])

# Tab 1: Price Trends
with tab1:
    st.subheader("Stock Price Trends")
    
    if not filtered_df.empty and selected_stocks:
        fig = go.Figure()
        
        for stock in selected_stocks:
            stock_data = filtered_df[filtered_df["symbol"] == stock]
            fig.add_trace(go.Scatter(
                x=stock_data["date"],
                y=stock_data["close"],
                mode='lines',
                name=stock,
                hovertemplate='<b>%{fullData.name}</b><br>Date: %{x}<br>Close: ₹%{y:.2f}<extra></extra>'
            ))
        
        fig.update_layout(
            title="Closing Prices Over Time",
            xaxis_title="Date",
            yaxis_title="Close Price (₹)",
            hovermode='x unified',
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Please select stocks to view price trends")

# Tab 2: Volatility Analysis
with tab2:
    st.subheader("Volatility Analysis (Standard Deviation of Daily Returns)")
    
    if not filtered_df.empty and selected_stocks:
        volatility_data = []
        
        for stock in selected_stocks:
            stock_data = filtered_df[filtered_df["symbol"] == stock].sort_values("date")
            stock_data["returns"] = stock_data["close"].pct_change()
            volatility = stock_data["returns"].std() * np.sqrt(252)  # Annualized volatility
            volatility_data.append({"Symbol": stock, "Volatility": volatility * 100})
        
        vol_df = pd.DataFrame(volatility_data).sort_values("Volatility", ascending=False)
        
        fig = px.bar(vol_df, x="Symbol", y="Volatility", 
                     title="Stock Volatility (Annualized %)",
                     labels={"Volatility": "Volatility (%)", "Symbol": "Stock"},
                     color="Volatility",
                     color_continuous_scale="Reds")
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(vol_df.style.background_gradient(cmap='Reds', subset=['Volatility']), use_container_width=True)
        with col2:
            st.write("**Interpretation:**")
            st.write("- Higher volatility = Higher risk & potential reward")
            st.write("- Lower volatility = More stable stock")
            st.write(f"- Most Volatile: **{vol_df.iloc[0]['Symbol']}** ({vol_df.iloc[0]['Volatility']:.2f}%)")
            st.write(f"- Least Volatile: **{vol_df.iloc[-1]['Symbol']}** ({vol_df.iloc[-1]['Volatility']:.2f}%)")
    else:
        st.info("Please select stocks to view volatility analysis")

# Tab 3: Cumulative Returns
with tab3:
    st.subheader("Cumulative Return Over Time")
    
    if not filtered_df.empty and selected_stocks:
        fig = go.Figure()
        
        for stock in selected_stocks:
            stock_data = filtered_df[filtered_df["symbol"] == stock].sort_values("date")
            if len(stock_data) > 0:
                initial_price = stock_data.iloc[0]["close"]
                stock_data["cumulative_return"] = ((stock_data["close"] / initial_price) - 1) * 100
                
                fig.add_trace(go.Scatter(
                    x=stock_data["date"],
                    y=stock_data["cumulative_return"],
                    mode='lines',
                    name=stock,
                    hovertemplate='<b>%{fullData.name}</b><br>Date: %{x}<br>Return: %{y:.2f}%<extra></extra>'
                ))
        
        fig.update_layout(
            title="Cumulative Returns (%)",
            xaxis_title="Date",
            yaxis_title="Cumulative Return (%)",
            hovermode='x unified',
            height=500
        )
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary table
        returns_summary = []
        for stock in selected_stocks:
            stock_data = filtered_df[filtered_df["symbol"] == stock].sort_values("date")
            if len(stock_data) > 1:
                initial = stock_data.iloc[0]["close"]
                final = stock_data.iloc[-1]["close"]
                total_return = ((final / initial) - 1) * 100
                returns_summary.append({"Symbol": stock, "Total Return (%)": total_return})
        
        returns_df = pd.DataFrame(returns_summary).sort_values("Total Return (%)", ascending=False)
        st.dataframe(returns_df.style.background_gradient(cmap='RdYlGn', subset=['Total Return (%)']), use_container_width=True)
    else:
        st.info("Please select stocks to view cumulative returns")

# Tab 4: Correlation
with tab4:
    st.subheader("Stock Price Correlation Matrix")
    
    if not filtered_df.empty and len(selected_stocks) > 1:
        # Create pivot table
        pivot_df = filtered_df.pivot_table(index="date", columns="symbol", values="close")
        
        # Calculate correlation
        corr_matrix = pivot_df[selected_stocks].corr()
        
        fig = px.imshow(corr_matrix, 
                        text_auto='.2f',
                        aspect="auto",
                        color_continuous_scale="RdBu_r",
                        title="Correlation Heatmap",
                        labels=dict(color="Correlation"))
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("**Interpretation:**")
        st.write("- Values close to 1: Stocks move together")
        st.write("- Values close to -1: Stocks move in opposite directions")
        st.write("- Values close to 0: No correlation")
    else:
        st.info("Please select at least 2 stocks to view correlation")

# Tab 5: Top Gainers and Losers
with tab5:
    st.subheader("📊 Top 5 Gainers and Losers (Month-wise)")
    
    if not filtered_df.empty:
        # Add month column
        filtered_df["month"] = filtered_df["date"].dt.to_period("M")
        
        # Get available months
        available_months = sorted(filtered_df["month"].unique(), reverse=True)
        
        selected_month = st.selectbox(
            "Select Month",
            options=available_months,
            format_func=lambda x: x.strftime("%B %Y")
        )
        
        # Filter data for selected month
        month_data = filtered_df[filtered_df["month"] == selected_month]
        
        # Calculate monthly returns
        monthly_returns = []
        for stock in month_data["symbol"].unique():
            stock_data = month_data[month_data["symbol"] == stock].sort_values("date")
            if len(stock_data) > 1:
                start_price = stock_data.iloc[0]["close"]
                end_price = stock_data.iloc[-1]["close"]
                return_pct = ((end_price / start_price) - 1) * 100
                monthly_returns.append({
                    "Symbol": stock,
                    "Start Price": start_price,
                    "End Price": end_price,
                    "Return (%)": return_pct
                })
        
        if monthly_returns:
            returns_df = pd.DataFrame(monthly_returns).sort_values("Return (%)", ascending=False)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🏆 Top 5 Gainers")
                gainers = returns_df.head(5)
                fig = px.bar(gainers, x="Symbol", y="Return (%)", 
                            color="Return (%)",
                            color_continuous_scale="Greens",
                            title=f"Top Gainers - {selected_month.strftime('%B %Y')}")
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(gainers.style.background_gradient(cmap='Greens', subset=['Return (%)']), 
                           use_container_width=True)
            
            with col2:
                st.markdown("### 📉 Top 5 Losers")
                losers = returns_df.tail(5).sort_values("Return (%)")
                fig = px.bar(losers, x="Symbol", y="Return (%)", 
                            color="Return (%)",
                            color_continuous_scale="Reds",
                            title=f"Top Losers - {selected_month.strftime('%B %Y')}")
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(losers.style.background_gradient(cmap='Reds', subset=['Return (%)']), 
                           use_container_width=True)
        else:
            st.warning("No data available for the selected month")
    else:
        st.info("No data available")

# Tab 6: Latest Prices
with tab6:
    st.subheader("Latest Stock Prices")
    
    if not filtered_df.empty:
        # Get latest prices
        latest_prices = filtered_df.sort_values("date").groupby("symbol").last()[["close", "volume", "date"]]
        latest_prices = latest_prices.sort_values("close", ascending=False)
        latest_prices.columns = ["Close Price (₹)", "Volume", "Last Updated"]
        
        st.dataframe(
            latest_prices.style.background_gradient(cmap='YlGnBu', subset=['Close Price (₹)']),
            use_container_width=True
        )
