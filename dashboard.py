import streamlit as st
from app.market.market_scanner import scan_markets

st.set_page_config(
    page_title="SJ AI Trader",
    page_icon="📈",
    layout="wide"
)

st.title("📈 SJ AI Trader")
st.subheader("AI Powered Forex Market Scanner")

results = scan_markets()

st.dataframe(results, use_container_width=True)

best = results[0]

st.success(f"⭐ Best Opportunity: {best['pair']}")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Signal", best["signal"])

with col2:
    st.metric("Confidence", f"{best['confidence']}%")

with col3:
    st.metric("Risk", best["risk"])

st.markdown("---")

st.write("### Trade Plan")

st.write(f"**Entry:** {best['entry']}")
st.write(f"**Stop Loss:** {best['stop_loss']}")
st.write(f"**Take Profit:** {best['take_profit']}")

st.write("### AI Reasons")

for reason in best["reasons"]:
    st.write(reason)