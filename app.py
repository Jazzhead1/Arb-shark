import streamlit as st
import ccxt
import pandas as pd
import time

st.title("🤖 Arbitrage Scanner")
st.write("Live arbitrage opportunities between Kraken and KuCoin")

# Initialize exchanges
kraken = ccxt.kraken()
kucoin = ccxt.kucoin()

exchanges = {
    "Kraken": kraken,
    "KuCoin": kucoin
}

# Symbol mapping: Exchange-specific symbol names
symbol_map = {
    "BTC": {"KuCoin": "BTC/USDT"},  # Kraken removed
    "ETH": {"Kraken": "ETH/USDT", "KuCoin": "ETH/USDT"},
    "SOL": {"Kraken": "SOL/USDT", "KuCoin": "SOL/USDT"},
    "XRP": {"Kraken": "XRP/USD",  "KuCoin": "XRP/USDT"}
}

def fetch_price(exchange_obj, symbol):
    try:
        ticker = exchange_obj.fetch_ticker(symbol)
        return ticker['last']
    except Exception as e:
        st.write(f"❌ {exchange_obj.id} {symbol}: {e}")
        return None

# Main loop: Refreshes all assets every 30 seconds
while True:
    for asset, exchange_symbols in symbol_map.items():
        st.subheader(f"📈 Prices for {asset}")
        prices = {}

        for exchange_name, exchange_obj in exchanges.items():
            symbol = exchange_symbols.get(exchange_name)
            if symbol:
                price = fetch_price(exchange_obj, symbol)
                if price:
                    prices[exchange_name] = price

        if len(prices) >= 2:
            df = pd.DataFrame(prices.items(), columns=["Exchange", "Price"]).sort_values(by="Price")
            st.dataframe(df)

            low = df.iloc[0]
            high = df.iloc[-1]
            spread = high["Price"] - low["Price"]
            profit_percent = (spread / low["Price"]) * 100

            st.success(f"💰 Buy on {low['Exchange']} at {low['Price']:.4f}, "
                       f"Sell on {high['Exchange']} at {high['Price']:.4f} → Profit: {profit_percent:.2f}%")
        else:
            st.warning(f"⚠️ Not enough data for {asset}")

    st.write("⏱ Refreshing in 30 seconds...")
    time.sleep(30)
    st.rerun()
