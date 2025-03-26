"""
Estilos centralizados para o Gerenciador Financeiro
"""

# Cores principais
COLORS = {
    'primary': '#8A05BE',      # Roxo principal
    'secondary': '#B5FF5A',    # Verde neon
    'background': '#0A0A0F',   # Fundo escuro
    'surface': '#1E1E1E',      # Superfície dos cards
    'text': '#F5F5F5',         # Texto principal
    'text_secondary': 'rgba(245, 245, 245, 0.7)',  # Texto secundário
    'success': '#B5FF5A',      # Sucesso (verde)
    'warning': '#FFB74D',      # Alerta (laranja)
    'error': '#FF4D4D',        # Erro (vermelho)
}

# Estilos CSS comuns
STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Reset e Estilos Base */
body {
    background-color: %(background)s;
    color: %(text)s;
    font-family: 'Inter', sans-serif;
}

#MainMenu, header, footer {visibility: hidden;}
section[data-testid="stSidebar"] { 
    display: none !important; 
    width: 0px !important;
    height: 0px !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    z-index: -1 !important;
}
div[data-testid="collapsedControl"] { display: none !important; }
.css-18e3th9 {padding-top: 0 !important;}
.css-1d391kg {padding-top: 3.5rem !important;}

/* Layout Components */
.page-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.header-container {
    background: linear-gradient(135deg, rgba(138, 5, 190, 0.1) 0%%, rgba(181, 255, 90, 0.05) 100%%);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 30px;
    border: 1px solid rgba(138, 5, 190, 0.2);
}

.header-title {
    background: linear-gradient(90deg, %(primary)s, %(secondary)s);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 15px;
}

.header-subtitle {
    color: %(text_secondary)s;
    font-size: 1.1rem;
}

/* Grid System */
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin: 20px 0;
}

/* Cards */
.card {
    background: rgba(10, 10, 15, 0.5);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(138, 5, 190, 0.2);
    border-radius: 15px;
    padding: 20px;
    transition: all 0.3s ease;
}

.card:hover {
    border-color: rgba(181, 255, 90, 0.4);
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(138, 5, 190, 0.1);
}

/* Métricas */
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

.metric-label {
    color: %(text_secondary)s;
    font-size: 0.9rem;
    margin-bottom: 8px;
}

.metric-value {
    color: %(secondary)s;
    font-size: 1.8rem;
    font-weight: 600;
    margin: 0;
}

.metric-subtitle {
    color: %(text_secondary)s;
    font-size: 0.85rem;
    margin-top: 5px;
}

/* Títulos e Textos */
.section-title {
    color: %(primary)s;
    font-size: 1.5rem;
    font-weight: 600;
    margin: 30px 0 20px;
    padding-bottom: 10px;
    border-bottom: 2px solid rgba(138, 5, 190, 0.2);
}

/* Alertas */
.alert {
    background: rgba(255, 183, 77, 0.1);
    border: 1px solid rgba(255, 183, 77, 0.3);
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    color: %(text)s;
}

.alert.success {
    background: rgba(181, 255, 90, 0.1);
    border-color: rgba(181, 255, 90, 0.3);
}

.alert.warning {
    background: rgba(255, 77, 77, 0.1);
    border-color: rgba(255, 77, 77, 0.3);
}

/* Botões */
.stButton > button {
    background: linear-gradient(135deg, %(primary)s 0%%, %(secondary)s 100%%);
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

/* Inputs e Forms */
.stTextInput > div > div > input {
    background-color: rgba(30, 30, 30, 0.5);
    border: 1px solid rgba(138, 5, 190, 0.2);
    border-radius: 8px;
    color: %(text)s;
}

.stTextInput > div > div > input:focus {
    border-color: %(primary)s;
    box-shadow: 0 0 0 1px %(primary)s;
}

/* Tabelas */
.dataframe {
    background: rgba(10, 10, 15, 0.5);
    border-radius: 10px;
    border: 1px solid rgba(138, 5, 190, 0.2);
}

.dataframe th {
    background: rgba(138, 5, 190, 0.1);
    color: %(secondary)s;
    padding: 12px;
}

.dataframe td {
    color: %(text)s;
    padding: 10px;
}

/* Gráficos */
.plot-container {
    background: rgba(10, 10, 15, 0.5);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(138, 5, 190, 0.2);
    border-radius: 15px;
    padding: 20px;
    margin: 20px 0;
}

/* Responsividade */
@media (max-width: 768px) {
    .grid {
        grid-template-columns: 1fr;
    }
    .header-title {
        font-size: 2rem;
    }
}
</style>
""" % COLORS

def apply_style():
    """Aplica os estilos definidos na página atual."""
    import streamlit as st
    st.markdown(STYLES, unsafe_allow_html=True)

def format_currency(value):
    """Formata um valor para moeda brasileira."""
    return f"R$ {value:,.2f}"

def format_percent(value):
    """Formata um valor para porcentagem."""
    return f"{value:.1f}%"

# Configurações padrão para gráficos Plotly
PLOTLY_LAYOUT = {
    "template": "plotly_dark",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "paper_bgcolor": "rgba(0,0,0,0)",
    "font": {
        "family": "Inter",
        "color": COLORS['text']
    },
    "title": {
        "font": {
            "size": 20,
            "color": COLORS['secondary']
        }
    },
    "xaxis": {
        "gridcolor": "rgba(138, 5, 190, 0.1)",
        "tickfont": {"color": COLORS['text_secondary']}
    },
    "yaxis": {
        "gridcolor": "rgba(138, 5, 190, 0.1)",
        "tickfont": {"color": COLORS['text_secondary']}
    }
}