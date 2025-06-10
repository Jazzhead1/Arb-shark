import streamlit as st
import ccxt
import pandas as pd
import time

# --- App Title ---
st.markdown(
    "<h1 style='text-align: center; color: #FFA500;'>🚀 SOLScout: Solana Arbitrage Tracker</h1>",
    unsafe_allow_html=True,
)

# --- CSS Styling ---
st.markdown(
    """
    <style>
        .stDataFrame {
            border: 2px solid #FFA500;
            border-radius: 10px;
        }
        .stButton>button {
            background-color: #FFA500;
            color: white;
            font-weight: bold;
            border-radius: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Initialize Exchanges ---
kraken = ccxt.kraken()
kucoin = ccxt.kucoin()
coinbase = ccxt.coinbase()

kraken.load_markets()
kucoin.load_markets()
coinbase.load_markets()

# --- Define SOL pairs to track ---
symbol_map = {
    "SOL": {
        "Kraken": "SOL/USD",
        "KuCoin": "SOL/USDT",
        "Coinbase": "SOL/USD"
    }
}

exchanges = {
    "Kraken": kraken,
    "KuCoin": kucoin,
    "Coinbase": coinbase
}

def fetch_price(exchange_obj, symbol):
    try:
        ticker = exchange_obj.fetch_ticker(symbol)
        return ticker['last']
    except Exception as e:
        st.error(f"❌ Error fetching {symbol} from {exchange_obj.id}: {e}")
        return None

# --- Display Prices ---
for asset, exchange_symbols in symbol_map.items():
    st.subheader(f"📊 Prices for {asset}")
    prices = {}
    for name, exchange in exchanges.items():
        symbol = exchange_symbols.get(name)
        if symbol:
            price = fetch_price(exchange, symbol)
            if price:
                prices[name] = price
    if len(prices) >= 2:
        df = pd.DataFrame(prices.items(), columns=["Exchange", "Price"]).sort_values(by="Price")
        st.dataframe(df)
        low = df.iloc[0]
        high = df.iloc[-1]
        spread = high["Price"] - low["Price"]
        profit_percent = (spread / low["Price"]) * 100
        st.success(f"Buy on {low['Exchange']} at {low['Price']:.4f}, sell on {high['Exchange']} at {high['Price']:.4f} → Profit: {profit_percent:.2f}%")
    else:
        st.warning(f"Not enough data for {asset}")

st.caption("🔁 Auto-refresh every 30 seconds...")
time.sleep(30)
st.experimental_rerun()
