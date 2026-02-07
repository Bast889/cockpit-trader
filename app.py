import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Cockpit Trader",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Cockpit Trader Comportamental")
st.caption("Envie sua planilha e veja seus resultados automaticamente")

# =============================
# UPLOAD DO ARQUIVO
# =============================
uploaded_file = st.file_uploader(
    "📂 Envie sua planilha de trades (Excel)",
    type=["xlsx"]
)

if uploaded_file is None:
    st.info("⬆️ Envie um arquivo Excel para começar.")
    st.stop()

# =============================
# LEITURA DA PLANILHA
# =============================
try:
    df = pd.read_excel(uploaded_file, sheet_name="Diario_Trades")
except:
    st.error("❌ A planilha precisa ter a aba 'Diario_Trades'.")
    st.stop()

df = df.dropna(subset=["Resultado (R)"])

if df.empty:
    st.warning("A planilha não contém trades válidos.")
    st.stop()

# =============================
# CÁLCULOS
# =============================
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

# =============================
# DASHBOARD
# =============================
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Trades", total)
c2.metric("Winrate", f"{winrate:.1%}")
c3.metric("Expectância (R)", f"{expectancia:.2f}")
c4.metric("R Total", f"{r_total:.1f}")
c5.metric("Contratos sugeridos", contratos)

st.divider()

# =============================
# GRÁFICO
# =============================
fig = px.line(df, y="R Acumulado", title="📈 Equity Curve")
st.plotly_chart(fig, use_container_width=True)

st.divider()

# =============================
# ESTADO EMOCIONAL
# =============================
e1, e2 = st.columns(2)
e1.metric("Foco médio", round(df["Foco"].mean(), 2))
e2.metric("Ansiedade média", round(df["Ansiedade"].mean(), 2))

st.divider()

# =============================
# ALERTA
# =============================
if r_total < -5:
    st.error("🚨 Stop diário atingido. Encerrar operações.")
else:
    st.success("✅ Operando dentro do plano.")

st.subheader("📋 Últimos trades")
st.dataframe(df.tail(10), use_container_width=True)
