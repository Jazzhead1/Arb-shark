import streamlit as st
import ccxt
import pandas as pd
import time

st.title("🤖 Arbitrage Scanner")
st.write("Real-time crypto arbitrage opportunities across Kraken and KuCoin")

# Exchanges in use
exchanges = {
    "Kraken": ccxt.kraken(),
    "KuCoin": ccxt.kucoin()
}

# Crypto pair to track
symbol = "BTC/USDT"

def fetch_price(exchange_obj, symbol):
    try:
        ticker = exchange_obj.fetch_ticker(symbol)
        return ticker['last']
    except Exception as e:
        st.write(f"❌ {exchange_obj.id}: {e}")
        return None

# Main loop (refresh every 30 seconds)
while True:
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

        st.success(f"💰 Arbitrage Opportunity: Buy on {low['Exchange']} at {low['Price']:.2f}, "
                   f"Sell on {high['Exchange']} at {high['Price']:.2f} → Profit: {profit_percent:.2f}%")
    else:
        st.warning("⚠️ Not enough data to compare prices")

    st.write("⏱ Refreshing in 30 seconds...")
    time.sleep(30)
    st.rerun()
