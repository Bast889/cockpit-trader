import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Cockpit Trader",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Cockpit Trader Comportamental")
st.caption("Controle simples e automático de performance")

FILE = "cockpit_trader_comportamental_v4.xlsx"

df = pd.read_excel(FILE, sheet_name="Diario_Trades")
df = df.dropna(subset=["Resultado (R)"])

if df.empty:
    st.warning("Nenhum trade registrado ainda.")
    st.stop()

df["R Acumulado"] = df["Resultado (R)"].cumsum()

wins = (df["Resultado (R)"] > 0).sum()
loss = (df["Resultado (R)"] < 0).sum()
total = len(df)

winrate = wins / total
gain = df[df["Resultado (R)"] > 0]["Resultado (R)"].mean()
loss_med = df[df["Resultado (R)"] < 0]["Resultado (R)"].mean()
expectancia = winrate * gain + (1 - winrate) * loss_med

r_total = df["R Acumulado"].iloc[-1]
contratos = max(1, int(r_total / 20) + 1)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Trades", total)
c2.metric("Winrate", f"{winrate:.1%}")
c3.metric("Expectância (R)", f"{expectancia:.2f}")
c4.metric("R Total", f"{r_total:.1f}")
c5.metric("Contratos", contratos)

st.divider()

fig = px.line(df, y="R Acumulado", title="Equity Curve")
st.plotly_chart(fig, use_container_width=True)

st.divider()

st.metric("Foco médio", round(df["Foco"].mean(), 2))
st.metric("Ansiedade média", round(df["Ansiedade"].mean(), 2))

st.divider()

if r_total < -5:
    st.error("🚨 Stop diário atingido. Encerrar operações.")
else:
    st.success("✅ Operando dentro do plano.")

st.subheader("Últimos trades")
st.dataframe(df.tail(10), use_container_width=True)
