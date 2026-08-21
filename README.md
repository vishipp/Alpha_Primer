# 📊 Alpha Primer

A Streamlit web app that helps beginner investors explore stock trends, risk, and comparative performance for 10 major technology companies — using easy-to-understand financial metrics and visualizations.

## Overview

The app pulls historical daily closing prices (2012–present) for:

`NVDA`, `MSFT`, `AAPL`, `GOOGL`, `AMZN`, `META`, `AVGO`, `TSM`, `TSLA`, `ORCL`

and lets users:

- Analyze a single stock's trend, trend strength, and volatility
- View price, moving average, and regression trend on an interactive chart
- View rolling returns over time
- Compare two stocks side-by-side (slope, R², volatility, relative strength)
- Explore which stocks tend to move together, via a correlation-based graph

A sidebar "Beginner Finance Guide" explains each metric (linear regression, R², volatility, rolling returns, moving average, relative strength) in plain language.

## Features

### Single-stock analysis
- **Trend Slope** — direction of the stock's long-term linear trend (via linear regression)
- **R²** — how well the linear trend fits the actual price data (trend reliability)
- **Volatility** — standard deviation of daily returns (risk indicator)
- **Price chart** — raw price, 20-day moving average, and regression trend line, plotted together
- **Rolling returns** — 20-day rolling percent change over time

### Two-stock comparison
- Side-by-side table of slope, R², and volatility for both stocks
- **Relative strength** — ratio of the two stocks' most recent prices
- Overlaid price chart for both stocks

### Related stocks
- Stocks are connected in a graph when their daily-return correlation exceeds 0.6
- The app displays which other stocks in the universe tend to move similarly to the selected stock (via BFS traversal of the correlation graph)

## Tech Stack

- **[Streamlit](https://streamlit.io/)** — web app framework/UI
- **[yfinance](https://pypi.org/project/yfinance/)** — historical stock price data
- **pandas / numpy** — data handling and numerical computation
- **[Plotly](https://plotly.com/python/)** — interactive charts

## Under the hood

Beyond the finance logic, the app includes a few classic data-structure/algorithm implementations, used internally to drive parts of the analysis:

- **Hash table** (`stock_hash`) — dict mapping each ticker to its cleaned price series
- **Linked list** — stores recent rolling-return values per stock
- **Queue** (fixed-size `deque`) — tracks a rolling window of recent daily returns
- **Binary Search Tree** — stocks indexed by trend slope
- **Graph + BFS** — stocks connected by return correlation > 0.6; BFS traverses related stocks
- **Linear search / binary search** — used when looking up the selected ticker
- **Bubble sort** — sorts stocks by trend slope

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd SPP
```

### 2. Install dependencies

```bash
python3 -m pip install streamlit yfinance numpy pandas plotly
```

(Or, if you add a `requirements.txt`: `pip install -r requirements.txt`)

### 3. Run the app

```bash
streamlit run main.py
```

This opens the app in your browser, typically at `http://localhost:8501`.

## Data caching

On first run, the app downloads price history via `yfinance` and saves it locally to `stock_data.csv`. On subsequent runs, it loads directly from this CSV instead of re-downloading, so startup is faster. Delete `stock_data.csv` if you want to force a fresh data pull.

## Disclaimer

This project is for educational purposes only and does not constitute financial advice. All metrics (trend, volatility, relative strength, etc.) are simplified for beginner learning purposes and should not be used as the sole basis for investment decisions.