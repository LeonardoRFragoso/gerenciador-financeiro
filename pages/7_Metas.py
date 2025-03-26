import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
from utils import add_meta, update_meta, delete_meta, get_metas, rerun, configurar_pagina
from style import apply_style, format_currency, COLORS, PLOTLY_LAYOUT

configurar_pagina("Metas")

# Aplicar estilos
apply_style()

# Botão para voltar
if st.button("🔙 Voltar à Página Inicial"):
    st.switch_page("main.py")

if "edit_meta_id" not in st.session_state:
    st.session_state.edit_meta_id = None

# Header da página
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🎯 Controle de Metas Financeiras</h1>
    <p class="header-subtitle">Estabeleça e acompanhe suas metas financeiras para alcançar seus objetivos</p>
</div>
""", unsafe_allow_html=True)

# Container para adicionar nova meta
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h3 class="section-title">➕ Nova Meta</h3>', unsafe_allow_html=True)
with st.form("form_meta"):
    col1, col2 = st.columns(2)
    with col1:
        descricao = st.text_input("Descrição da Meta")
        valor = st.number_input("Valor da Meta", min_value=0.0, format="%.2f")
    with col2:
        data_limite = st.date_input("Data Limite", datetime.date.today())
        progresso = st.number_input("Progresso Atual", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Criar Meta")
    if submitted:
        add_meta(descricao, valor, str(data_limite), progresso)
        st.markdown("""
        <div class="alert success">
            ✅ Meta criada com sucesso!
        </div>
        """, unsafe_allow_html=True)
        rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Container para edição de meta
if st.session_state.edit_meta_id is not None:
    meta = next((m for m in get_metas() if m[0] == st.session_state.edit_meta_id), None)
    if meta:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">✏️ Editar Meta</h3>', unsafe_allow_html=True)
        with st.form("edit_meta_form"):
            col1, col2 = st.columns(2)
            with col1:
                nova_descricao = st.text_input("Descrição", value=meta[1])
                novo_valor = st.number_input("Valor da Meta", min_value=0.0, value=meta[2], format="%.2f")
            with col2:
                nova_data = st.date_input("Data Limite", value=datetime.datetime.strptime(meta[3], "%Y-%m-%d").date())
                novo_progresso = st.number_input("Progresso Atual", min_value=0.0, value=meta[4], format="%.2f")
            edit_submitted = st.form_submit_button("Salvar Alterações")
            if edit_submitted:
                update_meta(meta[0], nova_descricao, novo_valor, str(nova_data), novo_progresso)
                st.markdown("""
                <div class="alert success">
                    ✅ Meta atualizada com sucesso!
                </div>
                """, unsafe_allow_html=True)
                st.session_state.edit_meta_id = None
                rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# Lista e análise de metas
metas = get_metas()
if metas:
    st.markdown('<h3 class="section-title">📊 Análise de Metas</h3>', unsafe_allow_html=True)
    
    # Métricas principais
    meta_fields = ['id', 'descricao', 'valor', 'data_limite', 'valor_atual', 'categoria']
    metas_dict = [dict(zip(meta_fields, meta)) for meta in metas]

    total_metas = sum(float(meta.get('valor', 0)) for meta in metas_dict)
    total_progresso = sum(float(meta.get('valor_atual', 0)) for meta in metas_dict)
    percentual_geral = (total_progresso / total_metas * 100) if total_metas > 0 else 0
    
    metas_proximas = [
        meta for meta in metas_dict
        if (datetime.datetime.strptime(meta.get('data_limite', '1970-01-01'), "%Y-%m-%d").date() - datetime.date.today()).days <= 30
    ]
    
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <p class="metric-label">Total em Metas</p>
            <h2 class="metric-value">{format_currency(total_metas)}</h2>
            <span class="metric-subtitle">Soma de todas as metas</span>
        </div>
        <div class="metric-card">
            <p class="metric-label">Progresso Geral</p>
            <h2 class="metric-value">{percentual_geral:.1f}%</h2>
            <span class="metric-subtitle">{format_currency(total_progresso)} alcançado</span>
        </div>
        <div class="metric-card">
            <p class="metric-label">Metas Próximas</p>
            <h2 class="metric-value">{len(metas_proximas)}</h2>
            <span class="metric-subtitle">Vencem em 30 dias</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de progresso das metas
        df_metas = pd.DataFrame([
            {
                'Meta': m.get('descricao', ''),
                'Valor': m.get('valor', 0),
                'Progresso': m.get('valor_atual', 0),
                'Restante': m.get('valor', 0) - m.get('valor_atual', 0)
            } for m in metas_dict
        ])
        
        fig_progresso = px.bar(
            df_metas,
            x='Meta',
            y=['Progresso', 'Restante'],
            title='Progresso das Metas',
            labels={'value': 'Valor', 'variable': 'Tipo'},
            color_discrete_map={'Progresso': COLORS['secondary'], 'Restante': COLORS['text_secondary']}
        )
        fig_progresso.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_progresso, use_container_width=True)
    
    with col2:
        # Timeline das metas
        df_timeline = pd.DataFrame([
            {
                'Meta': m.get('descricao', ''),
                'Data': pd.to_datetime(m.get('data_limite', '1970-01-01')),
                'Valor': m.get('valor', 0),
                'Progresso': (m.get('valor_atual', 0) / m.get('valor', 1) * 100) if m.get('valor', 0) > 0 else 0
            } for m in metas_dict
        ]).sort_values('Data')
        
        fig_timeline = px.scatter(
            df_timeline,
            x='Data',
            y='Valor',
            size='Progresso',
            text='Meta',
            title='Timeline de Metas',
            color_discrete_sequence=[COLORS['secondary']]
        )
        fig_timeline.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Lista de metas
    st.markdown('<h3 class="section-title">📋 Metas Cadastradas</h3>', unsafe_allow_html=True)
    st.markdown('<div class="grid">', unsafe_allow_html=True)
    for meta in metas_dict:
        progresso_percentual = (meta.get('valor_atual', 0) / meta.get('valor', 1) * 100) if meta.get('valor', 0) > 0 else 0
        dias_restantes = (datetime.datetime.strptime(meta.get('data_limite', '1970-01-01'), "%Y-%m-%d").date() - datetime.date.today()).days
        
        st.markdown(f"""
            <div class="card">
                <h3 style="color: {COLORS['secondary']}; font-size: 1.2rem; margin-bottom: 10px;">{meta.get('descricao', '')}</h3>
                <p style="color: {COLORS['text']}; font-size: 1.5rem; margin-bottom: 5px;">{format_currency(meta.get('valor', 0))}</p>
                <div class="progress-bar" style="margin: 10px 0;">
                    <div class="progress" style="width: {progresso_percentual}%;"></div>
                </div>
                <p style="color: {COLORS['text_secondary']}; font-size: 0.9rem;">
                    Progresso: {format_currency(meta.get('valor_atual', 0))} ({progresso_percentual:.1f}%)<br>
                    Prazo: {meta.get('data_limite', '1970-01-01')} ({dias_restantes} dias restantes)
                </p>
                <div style="display: flex; gap: 10px; margin-top: 15px;">
                    <button class="stButton" onclick="document.querySelector('#edit_meta_{meta['id']}').click()">✏️ Editar</button>
                    <button class="stButton" onclick="document.querySelector('#delete_meta_{meta['id']}').click()">🗑️ Excluir</button>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Botões ocultos para funcionalidade
        if st.button("✏️", key=f"edit_meta_{meta['id']}", help="Editar meta"):
            st.session_state.edit_meta_id = meta['id']
            rerun()
        if st.button("🗑️", key=f"delete_meta_{meta['id']}", help="Excluir meta"):
            delete_meta(meta['id'])
            st.markdown("""
            <div class="alert success">
                ✅ Meta excluída com sucesso!
            </div>
            """, unsafe_allow_html=True)
            rerun()
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="alert">
        ℹ️ Nenhuma meta cadastrada. Comece definindo seus objetivos financeiros.
    </div>
    """, unsafe_allow_html=True)