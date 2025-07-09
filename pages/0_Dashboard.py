import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_receitas, get_gastos, get_contas, get_dividas, get_parcelas, add_meta, get_metas, configurar_pagina
import datetime
from style import apply_style, theme_toggle

configurar_pagina("Dashboard")

# Seleção de tema e aplicação de estilos
theme = theme_toggle()
apply_style(theme)

# Estilo moderno e futurista
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.dashboard-header {
    background: linear-gradient(135deg, rgba(138, 5, 190, 0.1) 0%, rgba(181, 255, 90, 0.05) 100%);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 30px;
    border: 1px solid rgba(138, 5, 190, 0.2);
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin: 20px 0;
}

.metric-card {
    background: rgba(10, 10, 15, 0.5);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(138, 5, 190, 0.2);
    border-radius: 15px;
    padding: 20px;
    transition: all 0.3s ease;
}

.metric-card:hover {
    border-color: rgba(181, 255, 90, 0.4);
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(138, 5, 190, 0.1);
}

.label {
    color: rgba(245, 245, 245, 0.7);
    font-size: 0.9rem;
    margin-bottom: 8px;
}

.value {
    color: #B5FF5A;
    font-size: 1.8rem;
    font-weight: 600;
    margin: 0;
}

.percent {
    color: rgba(245, 245, 245, 0.6);
    font-size: 0.85rem;
    display: block;
    margin-top: 5px;
}

.section-title {
    color: #8A05BE;
    font-size: 1.5rem;
    font-weight: 600;
    margin: 30px 0 20px;
    padding-bottom: 10px;
    border-bottom: 2px solid rgba(138, 5, 190, 0.2);
}

.alert {
    background: rgba(255, 183, 77, 0.1);
    border: 1px solid rgba(255, 183, 77, 0.3);
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    color: rgba(245, 245, 245, 0.9);
}

.success {
    background: rgba(181, 255, 90, 0.1);
    border: 1px solid rgba(181, 255, 90, 0.3);
}

.warning {
    background: rgba(255, 77, 77, 0.1);
    border: 1px solid rgba(255, 77, 77, 0.3);
}

/* Botão estilizado */
.stButton > button {
    background: linear-gradient(135deg, #8A05BE 0%, #B5FF5A 100%);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(138, 5, 190, 0.2);
}

/* Gráfico estilizado */
.plot-container {
    background: rgba(10, 10, 15, 0.5);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(138, 5, 190, 0.2);
    border-radius: 15px;
    padding: 20px;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# Botão de retorno estilizado
if st.button("🔙 Voltar à Página Inicial"):
    st.switch_page("main.py")

# Header do Dashboard
st.markdown("""
<div class="dashboard-header">
    <h1 style='color: #B5FF5A; margin-bottom: 10px;'>📊 Dashboard Financeiro</h1>
    <p style='color: rgba(245, 245, 245, 0.7);'>Análise completa da sua saúde financeira com recomendações personalizadas</p>
</div>
""", unsafe_allow_html=True)

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

# Métricas principais
st.markdown("""
<div class="metric-grid">
    <div class="metric-card">
        <p class="label">Saldo Total em Contas</p>
        <h2 class="value">R$ {:.2f}</h2>
        <span class="percent">Atualizado em tempo real</span>
    </div>
    <div class="metric-card">
        <p class="label">Receitas do Mês</p>
        <h2 class="value">R$ {:.2f}</h2>
        <span class="percent">Total acumulado</span>
    </div>
    <div class="metric-card">
        <p class="label">Gastos do Mês</p>
        <h2 class="value">R$ {:.2f}</h2>
        <span class="percent">Total acumulado</span>
    </div>
</div>
""".format(total_contas, total_receitas, total_gastos), unsafe_allow_html=True)

# Seção de Análise 50/30/20
st.markdown("<h2 class='section-title'>📈 Análise 50/30/20</h2>", unsafe_allow_html=True)

# Classificação dos gastos
categorias_necessidades = ['moradia', 'alimentacao', 'alimentacão', 'transporte', 'saúde', 'educacao', 'educação']
gastos_necessidades = sum(g[2] for g in gastos if g[4].lower() in categorias_necessidades) if gastos else 0
gastos_desejos = total_gastos - gastos_necessidades
poupanca_real = total_receitas - total_gastos - total_dividas - total_parcelas
poupanca_real = max(poupanca_real, 0)

if total_receitas > 0:
    # Ideais
    ideal_necessidades = 0.50 * total_receitas
    ideal_desejos = 0.30 * total_receitas
    ideal_poupanca = 0.20 * total_receitas

    # Grid de métricas da análise 50/30/20
    st.markdown("""
    <div class="metric-grid">
        <div class="metric-card">
            <p class="label">Necessidades</p>
            <h2 class="value">R$ {:.2f}</h2>
            <span class="percent">{:.1f}% (Meta: 50%)</span>
        </div>
        <div class="metric-card">
            <p class="label">Desejos</p>
            <h2 class="value">R$ {:.2f}</h2>
            <span class="percent">{:.1f}% (Meta: 30%)</span>
        </div>
        <div class="metric-card">
            <p class="label">Poupança</p>
            <h2 class="value">R$ {:.2f}</h2>
            <span class="percent">{:.1f}% (Meta: 20%)</span>
        </div>
    </div>
    """.format(
        gastos_necessidades, (gastos_necessidades/total_receitas)*100,
        gastos_desejos, (gastos_desejos/total_receitas)*100,
        poupanca_real, (poupanca_real/total_receitas)*100
    ), unsafe_allow_html=True)

    # Alertas e recomendações
    if (gastos_necessidades / total_receitas) > 0.5:
        st.markdown("""
        <div class="alert warning">
            ⚠️ Seus gastos com necessidades estão acima de 50% da receita. Considere:
            <ul>
                <li>Renegociar contratos de serviços essenciais</li>
                <li>Buscar alternativas mais econômicas</li>
                <li>Avaliar possibilidade de redução em algumas categorias</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    if (gastos_desejos / total_receitas) > 0.3:
        st.markdown("""
        <div class="alert warning">
            ⚠️ Seus gastos com desejos ultrapassam 30%. Sugestões:
            <ul>
                <li>Priorize gastos essenciais</li>
                <li>Crie um orçamento para gastos não essenciais</li>
                <li>Considere adiar algumas compras</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    if (poupanca_real / total_receitas) < 0.2:
        st.markdown("""
        <div class="alert warning">
            ⚠️ Sua poupança está abaixo de 20%. Recomendações:
            <ul>
                <li>Estabeleça uma reserva de emergência</li>
                <li>Automatize sua poupança</li>
                <li>Revise gastos não essenciais</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Gráfico comparativo
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
        template="plotly_dark",
        color_discrete_sequence=["#8A05BE", "#B5FF5A"]
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter"),
        title_font_size=20,
        title_font_color="#B5FF5A",
        legend_font_color="rgba(245, 245, 245, 0.7)",
        xaxis=dict(
            gridcolor="rgba(138, 5, 190, 0.1)",
            tickfont=dict(color="rgba(245, 245, 245, 0.7)")
        ),
        yaxis=dict(
            gridcolor="rgba(138, 5, 190, 0.1)",
            tickfont=dict(color="rgba(245, 245, 245, 0.7)")
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    # Sugestão de meta automática
    descricao_meta = "Reserva Automática sugerida pelo sistema"
    meta_existente = any(m[1] == descricao_meta for m in metas)

    if poupanca_real >= 50 and not meta_existente:
        st.markdown("""
        <div class="alert success">
            💡 Com base na sua poupança atual, que está saudável, que tal criar uma meta para mantê-la?
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("✨ Criar Meta Sugerida"):
            data_limite = (datetime.date.today() + datetime.timedelta(days=90)).strftime("%Y-%m-%d")
            add_meta(descricao_meta, round(poupanca_real, 2), data_limite)
            st.success(f"✅ Meta criada com sucesso! Valor: R$ {poupanca_real:,.2f} para os próximos 3 meses")
    elif meta_existente:
        st.markdown("""
        <div class="alert success">
            ✅ Você já possui uma meta de reserva automática configurada. Continue assim!
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="alert">
        ℹ️ Nenhuma receita registrada para análise. Comece registrando suas fontes de renda para obter insights personalizados.
    </div>
    """, unsafe_allow_html=True)
