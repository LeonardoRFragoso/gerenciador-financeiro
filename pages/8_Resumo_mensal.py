import streamlit as st
import pandas as pd
from utils import get_receitas, get_gastos, get_dividas, get_parcelas
from datetime import datetime

st.set_page_config(page_title="Resumo Mensal", layout="wide")

# Botão voltar
if st.button("🔙 Voltar à Página Inicial"):
    st.switch_page("main.py")

st.markdown("<h2 style='color:#F37529;'>📅 Resumo Financeiro Mensal</h2>", unsafe_allow_html=True)

# Carregar dados
receitas = get_receitas()
gastos = get_gastos()
dividas = get_dividas()
parcelas = get_parcelas()

# Converter para DataFrames
df_receitas = pd.DataFrame(receitas, columns=["id", "descricao", "valor", "data", "categoria"])
df_gastos = pd.DataFrame(gastos, columns=["id", "descricao", "valor", "data", "categoria"])
df_dividas = pd.DataFrame(dividas, columns=["id", "descricao", "valor", "data", "categoria"])
df_parcelas = pd.DataFrame(parcelas, columns=["id", "descricao", "valor", "data"])

# Converter colunas de data
for df in [df_receitas, df_gastos, df_dividas, df_parcelas]:
    if not df.empty:
        df["data"] = pd.to_datetime(df["data"], errors='coerce')

# Seleção de mês
mes_ano = st.selectbox("Selecione o mês de análise:",
                       options=pd.date_range(start="2023-01-01", end=datetime.today(), freq='MS').strftime("%Y-%m").tolist()[::-1])

filtro_data = lambda df: df[(df["data"].dt.strftime("%Y-%m") == mes_ano)] if not df.empty else pd.DataFrame()

# Filtrar por mês selecionado
r_mensal = filtro_data(df_receitas)
g_mensal = filtro_data(df_gastos)
d_mensal = filtro_data(df_dividas)
p_mensal = filtro_data(df_parcelas)

# Calcular totais
total_receitas = r_mensal["valor"].sum() if not r_mensal.empty else 0
total_gastos = g_mensal["valor"].sum() if not g_mensal.empty else 0
total_dividas = d_mensal["valor"].sum() if not d_mensal.empty else 0
total_parcelas = p_mensal["valor"].sum() if not p_mensal.empty else 0
saldo = total_receitas - total_gastos - total_dividas - total_parcelas

# Exibir métricas
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Receitas", f"R$ {total_receitas:,.2f}")
col2.metric("Gastos", f"R$ {total_gastos:,.2f}")
col3.metric("Dívidas", f"R$ {total_dividas:,.2f}")
col4.metric("Parcelas", f"R$ {total_parcelas:,.2f}")
col5.metric("Saldo Mensal", f"R$ {saldo:,.2f}", delta_color="inverse")

# Detalhes opcionais
with st.expander("🔍 Ver Detalhamento por Categoria"):
    if not r_mensal.empty:
        st.subheader("Receitas")
        st.dataframe(r_mensal[["descricao", "valor", "data", "categoria"]])
    if not g_mensal.empty:
        st.subheader("Gastos")
        st.dataframe(g_mensal[["descricao", "valor", "data", "categoria"]])
    if not d_mensal.empty:
        st.subheader("Dívidas")
        st.dataframe(d_mensal[["descricao", "valor", "data", "categoria"]])
    if not p_mensal.empty:
        st.subheader("Parcelas")
        st.dataframe(p_mensal[["descricao", "valor", "data"]])
