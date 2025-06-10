import streamlit as st
import ccxt
import pandas as pd
import time

st.title("Arbitrage Scanner")

kraken = ccxt.kraken()
kucoin = ccxt.kucoin()

kraken.load_markets()
kucoin.load_markets()

symbol_map = {
    "BTC": {"Kraken": "BTC/USD", "KuCoin": "BTC/USDT"},
    "ETH": {"Kraken": "ETH/USDT", "KuCoin": "ETH/USDT"},
    "SOL": {"Kraken": "SOL/USDT", "KuCoin": "SOL/USDT"},
    "XRP": {"Kraken": "XRP/USD", "KuCoin": "XRP/USDT"}
}

def fetch_price(exchange_obj, symbol):
    if symbol == "BTC/USDT":
        st.warning(f"Skipping unsupported pair: {symbol}")
        return None
    try:
        ticker = exchange_obj.fetch_ticker(symbol)
        st.write(f"✅ Fetched {symbol} from {exchange_obj.id}: {ticker['last']}")
        return ticker['last']
    except Exception as e:
        st.error(f"❌ Error fetching {symbol} from {exchange_obj.id}: {e}")
        return None

while True:
    for asset, exchange_symbols in symbol_map.items():
        st.subheader(f"Prices for {asset}")
        prices = {}
        for exchange_name, exchange_obj in {"Kraken": kraken, "KuCoin": kucoin}.items():
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
            st.success(f"Buy on {low['Exchange']} at {low['Price']:.4f}, Sell on {high['Exchange']} at {high['Price']:.4f} → Profit: {profit_percent:.2f}%")
        else:
            st.warning(f"Not enough data for {asset}")
    st.write("Refreshing in 30 seconds...")
    time.sleep(30)
    st.experimental_rerun()
