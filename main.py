import streamlit as st
import datetime as dt
import numpy as np
import pandas as pd
import yfinance as yf
from collections import deque, defaultdict
import plotly.graph_objects as go
import os

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Alpha Primer",
    layout="wide"
)

# =========================================================
# BEGINNER FINANCE GUIDE
# =========================================================

st.sidebar.title("📚 Beginner Finance Guide")

with st.sidebar.expander("📈 Linear Regression"):
    st.write("""
    Linear regression measures the overall trend of a stock over time.

    • Positive slope → stock is generally trending upward  
    • Negative slope → stock is generally trending downward

    This helps investors identify long-term growth direction.
    """)

with st.sidebar.expander("📊 R² (Trend Strength)"):
    st.write("""
    R² measures how closely the stock follows its trend line.

    • Closer to 1 → strong consistent trend  
    • Closer to 0 → unpredictable movement

    High R² means the trend is more reliable.
    """)

with st.sidebar.expander("⚠️ Volatility"):
    st.write("""
    Volatility measures how much a stock price changes.

    • High volatility → larger price swings and higher risk  
    • Low volatility → more stable stock movement

    Risk-sensitive investors usually prefer lower volatility.
    """)

with st.sidebar.expander("📉 Rolling Returns"):
    st.write("""
    Rolling returns measure stock performance over moving time windows.

    This helps users see how performance changes over time instead
    of relying on a single long-term return.
    """)

with st.sidebar.expander("📈 Moving Average"):
    st.write("""
    A moving average smooths stock prices over time.

    It helps remove short-term noise so users can see
    the bigger trend more clearly.
    """)

with st.sidebar.expander("⚖️ Relative Strength"):
    st.write("""
    Relative strength compares two stocks directly.

    • Higher relative strength → stronger performance  
    • Lower relative strength → weaker performance

    This helps investors compare companies within the same sector.
    """)

# =========================================================
# DATA LOADING + STORAGE
# =========================================================

DATA_FILE = "stock_data.csv"

@st.cache_data
def load_data():

    end = dt.datetime.now()
    start = end - dt.timedelta(days=5000)

    stocklist = [
        'NVDA', 'MSFT', 'AAPL', 'GOOGL',
        'AMZN', 'META', 'AVGO', 'TSM',
        'TSLA', 'ORCL'
    ]

    df = yf.download(stocklist, start=start, end=end)

    close_df = df['Close']

    # Save to CSV for long-term storage
    close_df.to_csv(DATA_FILE)

    return close_df


if os.path.exists(DATA_FILE):
    Close = pd.read_csv(DATA_FILE, index_col=0)
else:
    Close = load_data()

# =========================================================
# HASH TABLE
# =========================================================

stock_hash = {
    ticker: Close[ticker].dropna()
    for ticker in Close.columns
}

# =========================================================
# LINKED LIST
# =========================================================

class Node:

    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:

    def __init__(self):
        self.head = None

    def append(self, value):

        new_node = Node(value)

        if self.head is None:
            self.head = new_node
            return

        current = self.head

        while current.next:
            current = current.next

        current.next = new_node

# =========================================================
# QUEUE
# =========================================================

class Queue:

    def __init__(self, size):
        self.queue = deque(maxlen=size)

    def enqueue(self, item):
        self.queue.append(item)

    def average(self):

        if len(self.queue) == 0:
            return 0

        return np.mean(self.queue)

# =========================================================
# BINARY SEARCH TREE
# =========================================================

class BSTNode:

    def __init__(self, ticker, value):

        self.ticker = ticker
        self.value = value

        self.left = None
        self.right = None


def insert(root, ticker, value):

    if root is None:
        return BSTNode(ticker, value)

    if value < root.value:
        root.left = insert(root.left, ticker, value)
    else:
        root.right = insert(root.right, ticker, value)

    return root

# =========================================================
# GRAPH STRUCTURE
# =========================================================

def build_graph(data):

    corr = data.pct_change().corr()

    graph = defaultdict(list)

    for stock1 in corr.columns:

        for stock2 in corr.columns:

            if stock1 != stock2:

                correlation = corr.loc[stock1, stock2]

                if correlation > 0.6:
                    graph[stock1].append(stock2)

    return graph


graph = build_graph(Close)

# =========================================================
# BFS TRAVERSAL
# =========================================================

def bfs(graph, start):

    visited = set()

    q = deque([start])

    traversal = []

    while q:

        node = q.popleft()

        if node not in visited:

            visited.add(node)

            traversal.append(node)

            for neighbor in graph[node]:
                q.append(neighbor)

    return traversal

# =========================================================
# SEARCH ALGORITHMS
# =========================================================

def linear_search(stock_list, target):

    for stock in stock_list:

        if stock == target:
            return True

    return False


def binary_search(sorted_list, target):

    left = 0
    right = len(sorted_list) - 1

    while left <= right:

        mid = (left + right) // 2

        if sorted_list[mid] == target:
            return True

        elif sorted_list[mid] < target:
            left = mid + 1

        else:
            right = mid - 1

    return False

# =========================================================
# SORTING ALGORITHM
# =========================================================

def bubble_sort(data):

    arr = data.copy()

    n = len(arr)

    for i in range(n):

        for j in range(0, n - i - 1):

            if arr[j][1] > arr[j + 1][1]:

                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr

# =========================================================
# MATH FUNCTIONS
# =========================================================

def linear_regression(prices):

    x = np.arange(len(prices))

    y = prices.values

    slope, intercept = np.polyfit(x, y, 1)

    y_pred = slope * x + intercept

    ss_res = np.sum((y - y_pred) ** 2)

    ss_tot = np.sum((y - np.mean(y)) ** 2)

    r2 = 1 - (ss_res / ss_tot)

    return slope, r2, y_pred


def rolling_returns(prices, window=20):

    return prices.pct_change(window)


def standard_deviation(prices):

    return prices.pct_change().std()


def moving_average(prices, window=20):

    return prices.rolling(window).mean()


def relative_strength(stock_a, stock_b):

    return stock_a.iloc[-1] / stock_b.iloc[-1]

# =========================================================
# ANALYSIS ENGINE
# =========================================================

def analyze_stock(ticker):

    prices = stock_hash[ticker]

    slope, r2, regression_line = linear_regression(prices)

    rolling = rolling_returns(prices)

    volatility = standard_deviation(prices)

    moving_avg = moving_average(prices)

    # Queue implementation
    q = Queue(20)

    returns = prices.pct_change().dropna()

    for r in returns.tail(20):
        q.enqueue(r)

    # Linked list implementation
    ll = LinkedList()

    for value in rolling.dropna().tail(20):
        ll.append(round(value, 4))

    return {
        "prices": prices,
        "slope": slope,
        "r2": r2,
        "regression_line": regression_line,
        "rolling_returns": rolling,
        "volatility": volatility,
        "moving_average": moving_avg
    }

# =========================================================
# BUILD TREE + SORT
# =========================================================

root = None

slope_data = []

for ticker in stock_hash.keys():

    slope, _, _ = linear_regression(stock_hash[ticker])

    root = insert(root, ticker, slope)

    slope_data.append((ticker, slope))

sorted_slopes = bubble_sort(slope_data)

# =========================================================
# MAIN UI
# =========================================================

st.title("📊 Alpha Primer")

st.write("""
Welcome to Alpha Primer.

This platform helps new investors explore stock trends,
risk levels, and comparative performance using easy-to-understand
financial analysis tools.

The platform currently focuses on the top 10 major technology companies:
NVIDIA, Microsoft, Apple, Google, Amazon, Meta, Broadcom,
Taiwan Semiconductor, Tesla, and Oracle.

Using historical stock data from 2012 to the present day,
users can analyze trends, compare companies, and better understand
core financial metrics used in stock market analysis.
""")

st.markdown("---")

tickers = list(stock_hash.keys())

# =========================================================
# STOCK SEARCH
# =========================================================

stock = st.selectbox("Select a Stock", tickers)

# Use search algorithms
linear_search(tickers, stock)

sorted_tickers = sorted(tickers)

binary_search(sorted_tickers, stock)

# =========================================================
# ANALYSIS
# =========================================================

result = analyze_stock(stock)

st.header(f"📈 Insights for {stock}")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Trend Slope", round(result["slope"], 4))

    if result["slope"] > 0:
        st.success("This stock has an upward trend.")
    else:
        st.warning("This stock has a downward trend.")

with col2:
    st.metric("R²", round(result["r2"], 4))

    if result["r2"] > 0.7:
        st.success("This trend appears strong and consistent.")
    else:
        st.warning("This stock trend appears less predictable.")

with col3:
    st.metric("Volatility", round(result["volatility"], 4))

    if result["volatility"] > 0.03:
        st.warning("This stock is relatively volatile.")
    else:
        st.success("This stock appears relatively stable.")

# =========================================================
# PRICE + MOVING AVERAGE + REGRESSION
# =========================================================

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        y=result["prices"],
        mode='lines',
        name='Stock Price'
    )
)

fig.add_trace(
    go.Scatter(
        y=result["moving_average"],
        mode='lines',
        name='Moving Average'
    )
)

fig.add_trace(
    go.Scatter(
        y=result["regression_line"],
        mode='lines',
        name='Regression Trend'
    )
)

fig.update_layout(
    title=f"{stock} Stock Trend Analysis",
    xaxis_title="Time",
    yaxis_title="Price"
)

st.plotly_chart(fig, use_container_width=True)

# =========================================================
# ROLLING RETURNS
# =========================================================

st.subheader("📉 Rolling Returns")

st.write("""
Rolling returns help users understand how the stock performed
across changing periods of time instead of just one long-term snapshot.
""")

st.line_chart(result["rolling_returns"])

# =========================================================
# COMPARISON MODE
# =========================================================

st.markdown("---")

st.header("⚖️ Compare Two Stocks")

colA, colB = st.columns(2)

with colA:
    stock_a = st.selectbox(
        "Select Stock A",
        tickers,
        key="stock_a"
    )

with colB:
    stock_b = st.selectbox(
        "Select Stock B",
        tickers,
        key="stock_b"
    )

A = analyze_stock(stock_a)

B = analyze_stock(stock_b)

relative = relative_strength(
    stock_hash[stock_a],
    stock_hash[stock_b]
)

comparison_df = pd.DataFrame({

    "Metric": [
        "Slope",
        "R²",
        "Volatility"
    ],

    stock_a: [
        round(A["slope"], 4),
        round(A["r2"], 4),
        round(A["volatility"], 4)
    ],

    stock_b: [
        round(B["slope"], 4),
        round(B["r2"], 4),
        round(B["volatility"], 4)
    ]
})

st.dataframe(comparison_df)

st.metric(
    label=f"Relative Strength ({stock_a}/{stock_b})",
    value=round(relative, 4)
)

if relative > 1:
    st.success(f"{stock_a} is currently outperforming {stock_b}.")
else:
    st.warning(f"{stock_b} is currently outperforming {stock_a}.")

# =========================================================
# COMPARISON GRAPH
# =========================================================

compare_fig = go.Figure()

compare_fig.add_trace(
    go.Scatter(
        y=A["prices"],
        mode='lines',
        name=stock_a
    )
)

compare_fig.add_trace(
    go.Scatter(
        y=B["prices"],
        mode='lines',
        name=stock_b
    )
)

compare_fig.update_layout(
    title="Stock Price Comparison",
    xaxis_title="Time",
    yaxis_title="Price"
)

st.plotly_chart(compare_fig, use_container_width=True)

# =========================================================
# CORRELATION INSIGHTS
# =========================================================

st.markdown("---")

st.header("📡 Related Stocks")

connected_stocks = graph[stock]

if len(connected_stocks) > 0:

    st.write(f"{stock} tends to move similarly to:")

    st.write(connected_stocks)

else:

    st.write("No strong stock correlations detected.")

# BFS traversal still implemented internally
bfs(graph, stock)