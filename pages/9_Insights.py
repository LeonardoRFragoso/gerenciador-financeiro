import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
from utils import get_receitas, get_gastos, get_contas, get_dividas, get_parcelas, add_meta, get_metas, configurar_pagina
from style import apply_style, format_currency, COLORS, PLOTLY_LAYOUT

configurar_pagina("Insights")

# Aplicar estilos
apply_style()

# Botão voltar para home
if st.button("🔙 Voltar à Página Inicial"):
    st.switch_page("main.py")

# Header da página
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🤖 Insights Financeiros com IA</h1>
    <p class="header-subtitle">Análise inteligente e recomendações personalizadas para suas finanças</p>
</div>
""", unsafe_allow_html=True)

def obter_insights_financeiros():
    contas = get_contas()
    gastos = get_gastos()
    metas = get_metas()
    dividas = get_dividas()
    parcelas = get_parcelas()
    receitas = get_receitas()

    total_receitas = sum(r[2] for r in receitas)
    total_gastos = sum(g[2] for g in gastos)
    total_dividas = sum(d[2] for d in dividas)
    total_parcelas = sum(p[2] for p in parcelas)
    poupanca_real = total_receitas - total_gastos - total_dividas - total_parcelas
    poupanca_real = max(poupanca_real, 0)

    categorias_necessidades = ['moradia', 'alimentacao', 'alimentacão', 'transporte', 'saúde', 'educacao', 'educação']
    gastos_necessidades = sum(g[2] for g in gastos if g[4].lower() in categorias_necessidades)
    gastos_desejos = total_gastos - gastos_necessidades

    percentual_necessidades = (gastos_necessidades / total_receitas) * 100 if total_receitas else 0
    percentual_desejos = (gastos_desejos / total_receitas) * 100 if total_receitas else 0
    percentual_poupanca = (poupanca_real / total_receitas) * 100 if total_receitas else 0

    # Exibir métricas principais
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <p class="metric-label">Necessidades (50%)</p>
            <h2 class="metric-value">{format_currency(gastos_necessidades)}</h2>
            <span class="metric-subtitle">{percentual_necessidades:.1f}% da renda</span>
        </div>
        <div class="metric-card">
            <p class="metric-label">Desejos (30%)</p>
            <h2 class="metric-value">{format_currency(gastos_desejos)}</h2>
            <span class="metric-subtitle">{percentual_desejos:.1f}% da renda</span>
        </div>
        <div class="metric-card">
            <p class="metric-label">Poupança (20%)</p>
            <h2 class="metric-value">{format_currency(poupanca_real)}</h2>
            <span class="metric-subtitle">{percentual_poupanca:.1f}% da renda</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Gráficos de análise
    col1, col2 = st.columns(2)

    with col1:
        # Gráfico de distribuição 50/30/20
        df_distribuicao = pd.DataFrame([
            {
                'Categoria': 'Necessidades',
                'Valor': gastos_necessidades,
                'Meta': total_receitas * 0.5,
                'Percentual': percentual_necessidades
            },
            {
                'Categoria': 'Desejos',
                'Valor': gastos_desejos,
                'Meta': total_receitas * 0.3,
                'Percentual': percentual_desejos
            },
            {
                'Categoria': 'Poupança',
                'Valor': poupanca_real,
                'Meta': total_receitas * 0.2,
                'Percentual': percentual_poupanca
            }
        ])

        fig_distribuicao = px.bar(
            df_distribuicao,
            x='Categoria',
            y=['Valor', 'Meta'],
            title='Distribuição Real vs. Meta (50/30/20)',
            barmode='group',
            color_discrete_map={
                'Valor': COLORS['primary'],
                'Meta': COLORS['secondary']
            }
        )
        fig_distribuicao.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_distribuicao, use_container_width=True)

    with col2:
        # Gráfico de composição financeira
        df_composicao = pd.DataFrame([
            {
                'Tipo': 'Receitas',
                'Valor': total_receitas
            },
            {
                'Tipo': 'Gastos',
                'Valor': total_gastos
            },
            {
                'Tipo': 'Dívidas',
                'Valor': total_dividas
            },
            {
                'Tipo': 'Parcelas',
                'Valor': total_parcelas
            },
            {
                'Tipo': 'Poupança',
                'Valor': poupanca_real
            }
        ])

        fig_composicao = px.pie(
            df_composicao,
            values='Valor',
            names='Tipo',
            title='Composição Financeira',
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        fig_composicao.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_composicao, use_container_width=True)

    resumo = (
        f"Receitas totais: R$ {total_receitas:.2f}\n"
        f"Gastos com necessidades: R$ {gastos_necessidades:.2f} ({percentual_necessidades:.1f}%)\n"
        f"Gastos com desejos: R$ {gastos_desejos:.2f} ({percentual_desejos:.1f}%)\n"
        f"Poupança real: R$ {poupanca_real:.2f} ({percentual_poupanca:.1f}%)\n"
        f"Total de dívidas: R$ {total_dividas:.2f}\n"
        f"Total de parcelas: R$ {total_parcelas:.2f}\n"
        f"Metas atuais: {len(metas)}\n"
    )

    prompt_template = (
        "Você é um consultor financeiro pessoal. Com base nos dados abaixo, dê recomendações claras e práticas "
        "seguindo a estratégia 50/30/20. Oriente sobre: como equilibrar os gastos com necessidades e desejos, "
        "como aumentar a poupança, quitar dívidas e definir metas financeiras. Liste os conselhos em tópicos "
        "explicando o motivo de cada um.\n\n"
        "{dados}"
    )

    prompt = PromptTemplate(input_variables=["dados"], template=prompt_template)
    openai_api_key = st.secrets.get("OPENAI_API_KEY", "")
    if not openai_api_key:
        st.markdown("""
        <div class="alert warning">
            ⚠️ Configure sua chave da API OpenAI em st.secrets ou via variável de ambiente para receber insights personalizados.
        </div>
        """, unsafe_allow_html=True)
        return None

    llm = OpenAI(openai_api_key=openai_api_key, temperature=0.7)
    chain = LLMChain(llm=llm, prompt=prompt)
    resposta = chain.run({"dados": resumo})
    return resposta

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h3 class="section-title">🎯 Análise Financeira</h3>', unsafe_allow_html=True)
st.write("Clique no botão abaixo para obter uma análise detalhada e sugestões personalizadas com base nos seus dados financeiros.")

if st.button("Gerar Insights com IA", type="primary"):
    with st.spinner("Analisando seus dados financeiros com IA..."):
        resposta = obter_insights_financeiros()
        if resposta:
            st.markdown("""
            <div class="alert success">
                ✅ Análise concluída com sucesso!
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class="card">
                <h3 class="section-title">💡 Recomendações do Assistente</h3>
                <div class="insight-text">
            """, unsafe_allow_html=True)
            st.markdown(resposta)
            st.markdown("</div></div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
