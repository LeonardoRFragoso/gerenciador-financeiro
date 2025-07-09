"""Estilos centralizados e temas para o Gerenciador Financeiro."""

# Paletas de cores para os temas claro e escuro
THEMES = {
    "dark": {
        "primary": "#8A05BE",          # Roxo principal
        "secondary": "#B5FF5A",        # Verde neon
        "background": "#0A0A0F",       # Fundo escuro
        "surface": "rgba(10, 10, 15, 0.5)",
        "text": "#F5F5F5",             # Texto principal
        "text_secondary": "rgba(245, 245, 245, 0.7)",
        "success": "#B5FF5A",
        "warning": "#FFB74D",
        "error": "#FF4D4D",
    },
    "light": {
        "primary": "#8A05BE",
        "secondary": "#B5FF5A",
        "background": "#FFFFFF",
        "surface": "rgba(255, 255, 255, 0.8)",
        "text": "#0A0A0F",
        "text_secondary": "rgba(10, 10, 15, 0.7)",
        "success": "#4CAF50",
        "warning": "#FFB74D",
        "error": "#FF4D4D",
    },
}

# Cores ativas (inicialmente tema escuro)
COLORS = THEMES["dark"]

# Estilos CSS comuns
STYLES_TEMPLATE = """
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

/* Grid de cards da página inicial */
.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 25px;
    padding: 20px;
}

/* Cartão da página inicial */
.card-container {
    background: linear-gradient(135deg, rgba(138, 5, 190, 0.1) 0%%, rgba(181, 255, 90, 0.05) 100%%);
    border: 1px solid rgba(138, 5, 190, 0.3);
    border-radius: 15px;
    padding: 25px;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.card-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, %(primary)s, %(secondary)s);
    transform: scaleX(0);
    transition: transform 0.4s ease;
}

.card-container:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(138, 5, 190, 0.2);
    border-color: rgba(138, 5, 190, 0.5);
}

.card-container:hover::before {
    transform: scaleX(1);
}

.card-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: %(secondary)s;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.card-desc {
    font-size: 0.9rem;
    color: %(text_secondary)s;
    line-height: 1.5;
}

/* Footer */
.footer {
    text-align: center;
    padding: 30px;
    background: linear-gradient(0deg, rgba(138, 5, 190, 0.1) 0%%, rgba(10, 10, 15, 0) 100%%);
    margin-top: 60px;
}

.footer-text {
    color: %(text_secondary)s;
    font-size: 0.9rem;
}

/* Cards */
.card {
    background: %(surface)s;
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
    background: %(surface)s;
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
    background: %(surface)s;
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
    background: %(surface)s;
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
"""

def _build_plotly_layout(colors: dict, theme: str) -> dict:
    """Retorna o layout padrão do Plotly de acordo com o tema."""
    template = "plotly_dark" if theme == "dark" else "plotly_white"
    return {
        "template": template,
        "plot_bgcolor": "rgba(0,0,0,0)",
        "paper_bgcolor": "rgba(0,0,0,0)",
        "font": {
            "family": "Inter",
            "color": colors["text"],
        },
        "title": {"font": {"size": 20, "color": colors["secondary"]}},
        "xaxis": {
            "gridcolor": "rgba(138, 5, 190, 0.1)",
            "tickfont": {"color": colors["text_secondary"]},
        },
        "yaxis": {
            "gridcolor": "rgba(138, 5, 190, 0.1)",
            "tickfont": {"color": colors["text_secondary"]},
        },
    }


def apply_style(theme: str | None = None):
    """Aplica os estilos definidos na página atual.

    O tema pode ser "dark" ou "light". Se nenhum for informado, utiliza o
    valor armazenado em ``st.session_state['theme']`` ou ``"dark"``.
    """
    import streamlit as st

    if theme is None:
        theme = st.session_state.get("theme", "dark")

    theme = theme if theme in THEMES else "dark"

    # Atualiza cores e layout globais
    global COLORS, PLOTLY_LAYOUT
    COLORS = THEMES[theme]
    PLOTLY_LAYOUT = _build_plotly_layout(COLORS, theme)

    st.session_state["theme"] = theme
    st.markdown(STYLES_TEMPLATE % COLORS, unsafe_allow_html=True)


def theme_toggle(label: str = "Tema") -> str:
    """Exibe um seletor de tema e retorna o tema escolhido."""
    import streamlit as st

    current = st.session_state.get("theme", "dark")
    option = st.radio(
        label,
        ["Claro", "Escuro"],
        horizontal=True,
        index=0 if current == "light" else 1,
    )
    theme = "light" if option == "Claro" else "dark"
    st.session_state["theme"] = theme
    return theme

# Layout padrão inicial para Plotly
PLOTLY_LAYOUT = _build_plotly_layout(COLORS, "dark")

def format_currency(value):
    """Formata um valor para moeda brasileira."""
    return f"R$ {value:,.2f}"

def format_percent(value):
    """Formata um valor para porcentagem."""
    return f"{value:.1f}%"