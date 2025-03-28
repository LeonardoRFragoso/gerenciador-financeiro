
# 💸 Gerenciador Financeiro com IA (Streamlit)

Um aplicativo moderno, visual e inteligente para organizar suas finanças pessoais. Desenvolvido em Python com Streamlit, ele utiliza a estratégia 50/30/20 e inteligência artificial (OpenAI) para oferecer insights personalizados com base nas suas receitas, despesas, metas e dívidas.

---

## ✅ Funcionalidades

### 📊 Dashboard
- Análise visual da proporção 50% necessidades, 30% desejos, 20% poupança
- Comparativo de valores reais vs ideais
- Sugestão automática de metas com base na poupança

### 💰 Receitas
- Cadastro e visualização de entradas financeiras
- Classificação por categoria e data

### 💸 Gastos
- Registro e controle de despesas
- Separação por categoria (necessidades/desejos)

### 🏦 Contas
- Cadastro de contas bancárias com saldo
- Exibição de total disponível

### 📆 Parcelas
- Controle de pagamentos recorrentes
- Visualização de vencimentos

### 📉 Dívidas
- Gerenciamento de débitos por valor, categoria e data

### 🎯 Metas
- Cadastro de objetivos financeiros com prazo
- Visualização de metas ativas

### 🤖 Insights com IA
- Geração de recomendações com base na estratégia 50/30/20
- Avaliação de gastos, dívidas e metas
- Uso da OpenAI (via LangChain)

---

## 🧑‍💻 Como Executar

1. Clone o projeto:
```bash
git clone https://github.com/LeonardoRFragoso/gerenciador-financeiro.git
cd gerenciador-financeiro
```

2. Crie o ambiente virtual:
```bash
python -m venv venv
venv\Scripts\activate  # (Windows) ou source venv/bin/activate (Linux/Mac)
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Adicione sua chave da OpenAI no arquivo:
```
.secrets.toml
```

```toml
OPENAI_API_KEY = "sua-chave-aqui"
```

5. Execute o app:
```bash
streamlit run main.py
```

---

## 🖼️ Interface

- Interface moderna, escura e responsiva
- Cards interativos com ícones e efeitos de hover
- Navegação visual (sem sidebar)

---

## 🧠 Tecnologias Utilizadas

- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [SQLite](https://www.sqlite.org/)
- [Plotly](https://plotly.com/)
- [OpenAI GPT-4](https://openai.com/)

---

## 📁 Estrutura de Arquivos

```
├── main.py
├── pages/
│   ├── 0_Dashboard.py
│   ├── 1_Contas.py
│   ├── 2_Gastos.py
│   ├── 3_Metas.py
│   ├── 4_Dividas.py
│   ├── 5_Parcelas.py
│   ├── 6_Receitas.py
│   └── 7_Insights.py
├── financas.db
├── utils.py
├── requirements.txt
└── README.md
```

---

## 📌 Regras Estratégicas

Este projeto segue a estratégia:
- 50% → Necessidades
- 30% → Desejos
- 20% → Poupança / Metas

---

## 📧 Suporte

Para dúvidas ou melhorias, entre em contato: [leonardorfragoso@gmail.com]
#   g e r e n c i a d o r - f i n a n c e i r o  
 