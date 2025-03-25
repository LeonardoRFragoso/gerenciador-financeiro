import streamlit as st
import datetime
from utils import get_contas, get_gastos, get_metas, get_dividas, get_parcelas, get_receitas
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

st.set_page_config(page_title="Insights AI", layout="wide")

# Botão voltar para home
if st.button("🔙 Voltar à Página Inicial"):
    st.switch_page("main.py")

st.markdown("""
<style>
.insight-card {
    background-color: #1e1e1e;
    border-left: 5px solid #8A05BE;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 0 10px rgba(138, 5, 190, 0.3);
    color: #F5F5F5;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='color:#F37529;'>🤖 Insights Financeiros com IA</h2>", unsafe_allow_html=True)
st.write("Clique no botão abaixo para obter sugestões personalizadas com base nos seus dados financeiros.")

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
        st.error("Defina sua chave da API do OpenAI em st.secrets ou via variável de ambiente.")
        return None

    llm = OpenAI(openai_api_key=openai_api_key, temperature=0.7)
    chain = LLMChain(llm=llm, prompt=prompt)
    resposta = chain.run({"dados": resumo})
    return resposta

if st.button("Gerar Insights com IA"):
    with st.spinner("Analisando seus dados financeiros com IA..."):
        resposta = obter_insights_financeiros()
        if resposta:
            st.success("Insights obtidos com sucesso!")
            with st.expander("🔎 Veja as recomendações do assistente"):
                st.markdown(f"<div class='insight-card'>{resposta}</div>", unsafe_allow_html=True)
