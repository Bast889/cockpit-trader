import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================
# CONFIGURAÇÃO VISUAL
# ==================================
st.set_page_config(
    page_title="Cockpit Trader",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.big-button button {
    font-size: 20px;
    padding: 15px;
}
.metric-box {
    background-color: #f0f2f6;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Cockpit Trader")
st.caption("Um painel simples para acompanhar seus resultados")

# ==================================
# ABAS
# ==================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Início",
    "📈 Resultados",
    "📊 Gráficos",
    "📋 Detalhes"
])

# ==================================
# ABA 1 — INÍCIO
# ==================================
with tab1:
    st.subheader("1️⃣ Envie sua planilha")

    uploaded_file = st.file_uploader(
        "Clique abaixo para selecionar seu arquivo Excel",
        type=["xlsx"]
    )

    if uploaded_file is None:
        st.info("⬆️ Envie sua planilha para continuar.")
        st.stop()

    try:
        df = pd.read_excel(uploaded_file, sheet_name="Diario_Trades")
    except:
        st.error("❌ A planilha precisa ter a aba 'Diario_Trades'.")
        st.stop()

    df = df.dropna(subset=["Resultado (R)"])

    if df.empty:
        st.warning("A planilha não contém trades válidos.")
        st.stop()

    st.success("✅ Planilha carregada com sucesso!")

# ==================================
# CÁLCULOS (uma vez só)
# ==================================
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

# ==================================
# ABA 2 — RESULTADOS
# ==================================
with tab2:
    st.subheader("2️⃣ Seus principais números")

    c1, c2, c3 = st.columns(3)

    c1.metric("Trades realizados", total)
    c2.metric("Winrate", f"{winrate:.1%}")
    c3.metric("Resultado Total (R)", f"{r_total:.1f}")

    st.divider()

    c4, c5 = st.columns(2)
    c4.metric("Expectância", f"{expectancia:.2f} R")
    c5.metric("Contratos sugeridos", contratos)

    st.divider()

    if r_total < -5:
        st.error("🚨 Atenção: Stop diário atingido.")
    else:
        st.success("✅ Você está dentro do plano.")

# ==================================
# ABA 3 — GRÁFICOS
# ==================================
with tab3:
    st.subheader("3️⃣ Evolução dos resultados")

    fig = px.line(
        df,
        y="R Acumulado",
        title="Evolução do Resultado (Equity Curve)"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==================================
# ABA 4 — DETALHES
# ==================================
with tab4:
    st.subheader("4️⃣ Detalhes das operações")

    st.dataframe(df, use_container_width=True)
