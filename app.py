import streamlit as st
import ccxt
import pandas as pd
import time

st.title("🤖 Arbitrage Scanner")
st.write("Live arbitrage opportunities between **Kraken** and **KuCoin**")

# Exchanges in use
exchanges = {
    "Kraken": ccxt.kraken(),
    "KuCoin": ccxt.kucoin()
}

# Crypto pairs to track
symbols = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT"]

def fetch_price(exchange_obj, symbol):
    try:
        ticker = exchange_obj.fetch_ticker(symbol)
        return ticker['last']
    except Exception as e:
        st.write(f"❌ {exchange_obj.id} {symbol}: {e}")
        return None

# Main loop
while True:
    for symbol in symbols:
        st.subheader(f"📈 Prices for {symbol}")
        prices = {}

        for name, exchange in exchanges.items():
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

            st.success(f"💰 Buy on {low['Exchange']} at {low['Price']:.4f}, "
                       f"Sell on {high['Exchange']} at {high['Price']:.4f} → Profit: {profit_percent:.2f}%")
        else:
            st.warning(f"⚠️ Not enough data to compare {symbol}")

    st.write("⏱ Refreshing in 30 seconds...")
    time.sleep(30)
    st.rerun()
