# 💰 FinanceControl - Gerenciador Financeiro Pessoal

Um sistema completo de gestão financeira pessoal com interface moderna e intuitiva, desenvolvido com React no frontend e Django no backend.

## 🚀 Tecnologias

### Frontend
- **React** - Biblioteca JavaScript para interfaces
- **React Router** - Navegação entre páginas
- **CSS3** - Estilização moderna com gradientes e animações
- **Context API** - Gerenciamento de estado global

### Backend
- **Django** - Framework web Python
- **Django REST Framework** - APIs REST
- **SQLite** - Banco de dados (desenvolvimento)
- **Python 3.x** - Linguagem de programação

## ✨ Funcionalidades

### 🎯 Principais Features
- **Dashboard Interativo** - Visão geral das finanças
- **Gestão de Transações** - Adicionar, editar e excluir transações
- **Categorização** - Organização por categorias personalizáveis
- **Relatórios** - Análises e gráficos detalhados
- **Autenticação** - Sistema de login/registro seguro
- **Responsivo** - Interface adaptável a todos os dispositivos

### 🎨 Design System
- **Cores**: Branco, preto, cinza e dourado
- **Estilo**: Moderno, futurista e minimalista
- **UX**: Interface limpa com micro-interações suaves
- **Acessibilidade**: Suporte completo a leitores de tela

## 📁 Estrutura do Projeto

```
Controle-Financeiro/
├── frontend/                 # Aplicação React
│   ├── public/              # Arquivos públicos
│   ├── src/                 # Código fonte
│   │   ├── components/      # Componentes reutilizáveis
│   │   ├── pages/          # Páginas da aplicação
│   │   ├── contexts/       # Context API
│   │   ├── services/       # Serviços e APIs
│   │   └── styles/         # Estilos globais
│   └── package.json        # Dependências do frontend
├── backend/                 # API Django
│   ├── apps/               # Aplicações Django
│   ├── config/             # Configurações
│   ├── requirements.txt    # Dependências Python
│   └── manage.py          # Gerenciador Django
├── .gitignore             # Arquivos ignorados pelo Git
└── README.md              # Documentação do projeto
```

## 🛠️ Instalação e Configuração

### Pré-requisitos
- Node.js (v14 ou superior)
- Python (v3.8 ou superior)
- Git

### 1. Clone o repositório
```bash
git clone https://github.com/LeonardoRFragoso/gerenciador-financeiro.git
cd gerenciador-financeiro
```

### 2. Configuração do Backend (Django)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 3. Configuração do Frontend (React)
```bash
cd frontend
npm install
npm start
```

### 4. Acesso à Aplicação
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Admin Django**: http://localhost:8000/admin

## 🎯 Como Usar

### 1. **Primeiro Acesso**
- Acesse http://localhost:3000
- Crie uma conta ou faça login
- Configure suas categorias iniciais

### 2. **Adicionando Transações**
- Clique em "Nova Transação"
- Preencha os dados (valor, categoria, descrição)
- Salve para ver no dashboard

### 3. **Visualizando Relatórios**
- Acesse a seção "Relatórios"
- Filtre por período ou categoria
- Analise gráficos e estatísticas

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Leonardo Fragoso**
- GitHub: [@LeonardoRFragoso](https://github.com/LeonardoRFragoso)
- LinkedIn: [Leonardo Fragoso](https://www.linkedin.com/in/leonardo-fragoso-921b166a/)

## 🙏 Agradecimentos

- Comunidade React e Django
- Contribuidores do projeto
- Feedback dos usuários

---

⭐ Se este projeto te ajudou, considere dar uma estrela no repositório!
