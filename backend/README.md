# 🏦 Finance Control API - Backend Django

API REST completa para sistema de controle financeiro pessoal, desenvolvida em Django com Django REST Framework.

## 🚀 Tecnologias Utilizadas

- **Python 3.11+**
- **Django 4.2.7**
- **Django REST Framework 3.14.0**
- **Simple JWT** (Autenticação)
- **Django CORS Headers** (Integração com React)
- **DRF-YASG** (Documentação Swagger)
- **SQLite** (Desenvolvimento)

## 📋 Funcionalidades

### 🔐 Autenticação
- JWT Token Authentication
- Registro de usuários
- Login/Logout
- Refresh de tokens

### 👤 Usuários
- Modelo customizado com campos financeiros
- Perfil detalhado
- Configurações pessoais
- Cálculo automático de saldo

### 💰 Transações
- CRUD completo (receitas e despesas)
- Categorização personalizada
- Métodos de pagamento
- Filtros e busca avançada
- Relatórios e resumos
- Tags e observações

### 🎯 Metas Financeiras
- Criação e acompanhamento de metas
- Cálculo automático de progresso
- Contribuições para metas
- Prioridades e categorias
- Status (ativa, pausada, concluída)

### 📊 Categorias
- Categorias personalizáveis por usuário
- Ícones e cores customizáveis
- Categorias padrão automáticas
- Separação por tipo (receita/despesa)

### 📈 Relatórios
- Resumo financeiro mensal
- Relatórios por categoria
- Gráficos de evolução
- Análise de gastos

## 🛠️ Configuração e Instalação

### 1. Pré-requisitos
```bash
# Python 3.11+
python --version

# Git
git --version
```

### 2. Instalação
```bash
# Clone o repositório
git clone <repository-url>
cd Controle-Financeiro/backend

# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### 3. Configuração Inicial
```bash
# Execute o script de setup (recomendado)
python setup.py

# OU configure manualmente:
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 4. Executar o Servidor
```bash
python manage.py runserver
```

O servidor estará disponível em: `http://localhost:8000`

## 📚 Documentação da API

### Endpoints Principais

#### 🔐 Autenticação
```
POST /api/auth/login/          # Login (obter tokens)
POST /api/auth/refresh/        # Refresh token
POST /api/auth/verify/         # Verificar token
```

#### 👤 Usuários
```
GET    /api/accounts/users/me/     # Dados do usuário atual
PUT    /api/accounts/profile/      # Atualizar perfil
POST   /api/accounts/register/     # Registro de usuário
```

#### 💰 Transações
```
GET    /api/transactions/transactions/           # Listar transações
POST   /api/transactions/transactions/           # Criar transação
GET    /api/transactions/transactions/{id}/      # Detalhes da transação
PUT    /api/transactions/transactions/{id}/      # Atualizar transação
DELETE /api/transactions/transactions/{id}/      # Deletar transação

GET    /api/transactions/summary/                # Resumo financeiro
GET    /api/transactions/monthly-report/         # Relatório mensal
GET    /api/transactions/categories-report/      # Relatório por categoria
GET    /api/transactions/transactions/recent/    # Transações recentes
```

#### 🎯 Metas
```
GET    /api/goals/goals/                    # Listar metas
POST   /api/goals/goals/                    # Criar meta
GET    /api/goals/goals/{id}/               # Detalhes da meta
PUT    /api/goals/goals/{id}/               # Atualizar meta
DELETE /api/goals/goals/{id}/               # Deletar meta

GET    /api/goals/summary/                  # Resumo de metas
POST   /api/goals/{id}/contribute/          # Contribuir para meta
GET    /api/goals/goals/active/             # Metas ativas
GET    /api/goals/goals/completed/          # Metas concluídas
```

#### 📊 Categorias
```
GET    /api/categories/categories/          # Listar categorias
POST   /api/categories/categories/          # Criar categoria
GET    /api/categories/categories/{id}/     # Detalhes da categoria
PUT    /api/categories/categories/{id}/     # Atualizar categoria
DELETE /api/categories/categories/{id}/     # Deletar categoria

POST   /api/categories/defaults/            # Criar categorias padrão
GET    /api/categories/categories/by_type/  # Categorias por tipo
```

### 📖 Documentação Interativa

- **Swagger UI:** `http://localhost:8000/api/docs/`
- **ReDoc:** `http://localhost:8000/api/redoc/`
- **Admin Django:** `http://localhost:8000/admin/`

## 🔧 Configurações

### Variáveis de Ambiente (.env)
```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOW_ALL_ORIGINS=True
```

### CORS para React
O backend está configurado para aceitar requisições do frontend React:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

## 🧪 Dados de Teste

O script `setup.py` cria automaticamente:

### Usuário Admin
- **Username:** admin
- **Password:** admin123
- **Email:** admin@financecontrol.com

### Usuário Demo
- **Username:** demo
- **Password:** demo123
- **Email:** demo@financecontrol.com

O usuário demo inclui:
- Categorias padrão
- Transações de exemplo
- Meta de exemplo

## 🔒 Autenticação JWT

### Como usar nos requests:
```javascript
// Headers para requisições autenticadas
{
  'Authorization': 'Bearer <access_token>',
  'Content-Type': 'application/json'
}
```

### Exemplo de Login:
```javascript
// POST /api/auth/login/
{
  "username": "demo",
  "password": "demo123"
}

// Resposta:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## 🚀 Integração com Frontend React

### Configuração no React:
```javascript
// API Base URL
const API_BASE_URL = 'http://localhost:8000/api';

// Exemplo de requisição
const response = await fetch(`${API_BASE_URL}/transactions/transactions/`, {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
  },
});
```

## 📁 Estrutura do Projeto

```
backend/
├── finance_api/           # Configurações do Django
│   ├── settings.py       # Configurações principais
│   ├── urls.py          # URLs principais
│   └── wsgi.py          # WSGI config
├── accounts/             # App de usuários
│   ├── models.py        # Modelo User customizado
│   ├── serializers.py   # Serializers DRF
│   ├── views.py         # Views da API
│   └── urls.py          # URLs da app
├── transactions/         # App de transações
├── goals/               # App de metas
├── categories/          # App de categorias
├── requirements.txt     # Dependências
├── setup.py            # Script de configuração
├── manage.py           # Django management
└── README.md           # Esta documentação
```

## 🐛 Troubleshooting

### Problemas Comuns:

1. **Erro de CORS**
   - Verifique se o frontend está rodando em `localhost:3000`
   - Confirme as configurações CORS no `settings.py`

2. **Erro de Token JWT**
   - Verifique se o token não expirou
   - Use o endpoint `/api/auth/refresh/` para renovar

3. **Erro de Migração**
   - Execute: `python manage.py makemigrations`
   - Execute: `python manage.py migrate`

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique a documentação Swagger
2. Consulte os logs do Django
3. Verifique as configurações de CORS

---

**Desenvolvido para integração perfeita com o frontend React do Finance Control** 🚀
