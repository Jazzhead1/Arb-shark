import streamlit as st
import ccxt
import time

st.set_page_config(page_title="Crypto Arbitrage Scanner", layout="centered")

st.title("📈 Real-Time Arbitrage Scanner")
st.markdown("Monitor price differences across exchanges and spot profit opportunities.")

# Select your trading pair
symbol = st.selectbox("Select Crypto Pair", ["BTC/USDT", "ETH/USDT", "XRP/USDT", "SOL/USDT"])

# Profit threshold
threshold = st.slider("Minimum Arbitrage % to Alert", min_value=0.1, max_value=10.0, value=1.0)

# Set update frequency
refresh_sec = st.selectbox("Refresh Every (seconds)", [5, 10, 15, 30, 60], index=1)

# Supported exchanges
exchanges = {
    "Binance": ccxt.binance(),
    "Kraken": ccxt.kraken(),
    "KuCoin": ccxt.kucoin(),
    "Bybit": ccxt.bybit(),
}

def fetch_price(exchange_obj, symbol):
    try:
        ticker = exchange_obj.fetch_ticker(symbol)
        return ticker['last']
    except Exception as e:
        return None

placeholder = st.empty()

while True:
    with placeholder.container():
        st.subheader(f"🔍 Prices for {symbol}")

        prices = {}
        for name, ex in exchanges.items():
            price = fetch_price(ex, symbol)
            if price:
                prices[name] = price
                st.write(f"{name}: ${price:,.2f}")
            else:
                st.write(f"{name}: ❌ Not available")

        if len(prices) >= 2:
            low_ex = min(prices, key=prices.get)
            high_ex = max(prices, key=prices.get)

            low_price = prices[low_ex]
            high_price = prices[high_ex]
            spread = high_price - low_price
            profit_pct = (spread / low_price) * 100

            if profit_pct >= threshold:
                st.success(f"💰 Arbitrage Opportunity! Buy on **{low_ex}** at ${low_price:.2f}, sell on **{high_ex}** at ${high_price:.2f} → Profit: **{profit_pct:.2f}%**")
            else:
                st.info(f"📊 Spread: {profit_pct:.2f}% — below threshold")
        else:
            st.warning("Not enough price data available.")

    time.sleep(refresh_sec)
