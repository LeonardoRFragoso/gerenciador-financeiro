import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_receitas, get_gastos, get_contas, get_dividas, get_parcelas, add_meta, get_metas
import datetime

st.set_page_config(page_title="Dashboard", layout="wide")

# Botão para retornar à tela inicial
if st.button("🔙 Voltar à Página Inicial"):
    st.switch_page("main.py")

st.markdown("<h2 style='color:#F37529;'>📊 Dashboard Financeiro - Visão Geral</h2>", unsafe_allow_html=True)

# Obter dados
receitas = get_receitas()
gastos = get_gastos()
contas = get_contas()
dividas = get_dividas()
parcelas = get_parcelas()
metas = get_metas()

# Totais
total_receitas = sum(r[2] for r in receitas) if receitas else 0
total_gastos = sum(g[2] for g in gastos) if gastos else 0
total_dividas = sum(d[2] for d in dividas) if dividas else 0
total_parcelas = sum(p[2] for p in parcelas) if parcelas else 0
total_contas = sum(c[2] for c in contas) if contas else 0

st.markdown(f"""
<div class='metric-card'>
    <p class='label'>Saldo Total em Contas</p>
    <h2 class='value'>R$ {total_contas:,.2f}</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("<h3 style='color:#B5FF5A;'>📈 Análise 50/30/20</h3>", unsafe_allow_html=True)

# Classificação dos gastos: categorias de necessidades
categorias_necessidades = ['moradia', 'alimentacao', 'alimentacão', 'transporte', 'saúde', 'educacao', 'educação']
gastos_necessidades = sum(g[2] for g in gastos if g[4].lower() in categorias_necessidades) if gastos else 0
gastos_desejos = total_gastos - gastos_necessidades
poupanca_real = total_receitas - total_gastos - total_dividas - total_parcelas
poupanca_real = max(poupanca_real, 0)

# Ideais
ideal_necessidades = 0.50 * total_receitas
ideal_desejos = 0.30 * total_receitas
ideal_poupanca = 0.20 * total_receitas

if total_receitas > 0:
    st.markdown("""
    <div style='display:flex; gap:20px;'>
        <div class='metric-card'>
            <p class='label'>Necessidades</p>
            <h2 class='value'>R$ {:.2f}</h2>
            <span class='percent'>{:.1f}% (Ideal: 50%)</span>
        </div>
        <div class='metric-card'>
            <p class='label'>Desejos</p>
            <h2 class='value'>R$ {:.2f}</h2>
            <span class='percent'>{:.1f}% (Ideal: 30%)</span>
        </div>
        <div class='metric-card'>
            <p class='label'>Poupança Real</p>
            <h2 class='value'>R$ {:.2f}</h2>
            <span class='percent'>{:.1f}% (Ideal: 20%)</span>
        </div>
    </div>
    """.format(
        gastos_necessidades, (gastos_necessidades/total_receitas)*100,
        gastos_desejos, (gastos_desejos/total_receitas)*100,
        poupanca_real, (poupanca_real/total_receitas)*100
    ), unsafe_allow_html=True)

    if (gastos_necessidades / total_receitas) > 0.5:
        st.warning("⚠️ Gastos com necessidades acima de 50% da sua receita. Reduza se possível!")
    if (gastos_desejos / total_receitas) > 0.3:
        st.warning("⚠️ Gastos com desejos acima de 30%. Reavalie prioridades!")
    if (poupanca_real / total_receitas) < 0.2:
        st.warning("⚠️ Poupança abaixo de 20%. Tente reservar mais para emergências!")

    descricao_meta = "Reserva Automática sugerida pelo sistema"
    meta_existente = any(m[1] == descricao_meta for m in metas)

    if poupanca_real >= 50 and not meta_existente:
        if st.button("💡 Criar Meta Sugerida com base na Poupança"):
            data_limite = (datetime.date.today() + datetime.timedelta(days=90)).strftime("%Y-%m-%d")
            add_meta(descricao_meta, round(poupanca_real, 2), data_limite)
            st.success(f"Meta criada automaticamente com valor de R$ {poupanca_real:,.2f} para os próximos 3 meses!")
    elif meta_existente:
        st.info("✅ Meta sugerida já criada anteriormente.")
else:
    st.warning("Nenhuma receita registrada para análise.")

# Gráfico comparativo
if total_receitas > 0:
    df_comparativo = pd.DataFrame({
        "Categoria": ["Necessidades", "Desejos", "Poupança"],
        "Valor Real": [gastos_necessidades, gastos_desejos, poupanca_real],
        "Valor Ideal": [ideal_necessidades, ideal_desejos, ideal_poupanca]
    })
    fig = px.bar(
        df_comparativo, 
        x="Categoria", 
        y=["Valor Real", "Valor Ideal"],
        barmode="group", 
        title="Comparativo: Valores Reais x Ideais (50/30/20)",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)
