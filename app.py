import streamlit as st
import pandas as pd
import plotly.express as px

# ===============================
# CONFIGURAÇÃO VISUAL
# ===============================
st.set_page_config(
    page_title="Cockpit Trader",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.big-text {
    font-size: 22px;
    font-weight: bold;
}
.box {
    background-color: #f4f6fa;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Cockpit Trader")
st.caption("Acompanhe seus resultados de forma simples, passo a passo")

# ===============================
# PASSO 1 — UPLOAD
# ===============================
st.markdown("## 1️⃣ Enviar planilha")
st.markdown("Envie sua planilha de trades para começar.")

uploaded_file = st.file_uploader(
    "Clique no botão abaixo para escolher o arquivo Excel",
    type=["xlsx"]
)

if uploaded_file is None:
    st.info("⬆️ Nenhum arquivo enviado ainda.")
    st.stop()

# ===============================
# LEITURA DA PLANILHA
# ===============================
try:
    df = pd.read_excel(uploaded_file, sheet_name="Diario_Trades")
except:
    st.error("❌ A planilha precisa ter uma aba chamada 'Diario_Trades'.")
    st.stop()

df = df.dropna(subset=["Resultado (R)"])

if df.empty:
    st.warning("A planilha não possui trades válidos.")
    st.stop()

st.success("✅ Planilha carregada com sucesso!")

# ===============================
# CÁLCULOS
# ===============================
df["R Acumulado"] = df["Resultado (R)"].cumsum()

wins = (df["Resultado (R)"] > 0).sum()
total = len(df)
winrate = wins / total
r_total = df["R Acumulado"].iloc[-1]

# ===============================
# PASSO 2 — RESULTADO SIMPLES
# ===============================
st.markdown("## 2️⃣ Resultado resumido")

c1, c2, c3 = st.columns(3)
c1.metric("Trades realizados", total)
c2.metric("Winrate", f"{winrate:.1%}")
c3.metric("Resultado total (R)", f"{r_total:.1f}")

if r_total < 0:
    st.error("⚠️ Resultado negativo. Atenção ao plano.")
else:
    st.success("✅ Resultado positivo.")

# ===============================
# PASSO 3 — GRÁFICO (OPCIONAL)
# ===============================
with st.expander("📈 Ver gráfico de evolução"):
    fig = px.line(df, y="R Acumulado", title="Evolução do Resultado")
    st.plotly_chart(fig, use_container_width=True)

# ===============================
# PASSO 4 — DETALHES (OPCIONAL)
# ===============================
with st.expander("📋 Ver detalhes das operações"):
    st.dataframe(df, use_container_width=True)
