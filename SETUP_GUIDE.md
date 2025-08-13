# 🚀 Finance Control - Guia de Configuração Completa

Este guia te ajudará a configurar e executar o sistema completo de controle financeiro com frontend React e backend Django.

## 📋 Pré-requisitos

- **Node.js 16+** (para o frontend React)
- **Python 3.11+** (para o backend Django)
- **Git** (para versionamento)

## 🏗️ Arquitetura do Sistema

```
Controle-Financeiro/
├── frontend/          # React App (já desenvolvido)
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── .env
├── backend/           # Django API (recém criado)
│   ├── finance_api/
│   ├── accounts/
│   ├── transactions/
│   ├── goals/
│   ├── categories/
│   ├── requirements.txt
│   └── manage.py
└── SETUP_GUIDE.md     # Este arquivo
```

## 🔧 Configuração do Backend Django

### 1. Navegar para o diretório backend
```bash
cd backend
```

### 2. Criar e ativar ambiente virtual
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (Windows)
venv\Scripts\activate

# Ativar ambiente virtual (Linux/Mac)
source venv/bin/activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar banco de dados e dados iniciais
```bash
# Opção 1: Script automático (RECOMENDADO)
python setup.py

# Opção 2: Manual
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 5. Executar servidor Django
```bash
python manage.py runserver
```

✅ **Backend estará rodando em:** `http://localhost:8000`

## ⚛️ Configuração do Frontend React

### 1. Abrir novo terminal e navegar para frontend
```bash
cd frontend
```

### 2. Instalar dependências (se ainda não instalado)
```bash
npm install
```

### 3. Configurar variáveis de ambiente
```bash
# Copiar arquivo de exemplo
copy .env.example .env

# Editar .env com as configurações:
# REACT_APP_API_URL=http://localhost:8000/api
```

### 4. Executar servidor React
```bash
npm start
```

✅ **Frontend estará rodando em:** `http://localhost:3000`

## 🔗 Testando a Integração

### 1. Acessar o Frontend
- Abra: `http://localhost:3000`
- O frontend React já está completo e funcional

### 2. Testar Backend API
- Documentação: `http://localhost:8000/api/docs/`
- Admin Django: `http://localhost:8000/admin/`

### 3. Usuários de Teste
**Usuário Demo:**
- Username: `demo`
- Password: `demo123`

**Admin:**
- Username: `admin`
- Password: `admin123`

## 🔄 Fluxo de Desenvolvimento

### Para trabalhar no projeto:

1. **Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate  # Windows
python manage.py runserver
```

2. **Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### Ambos devem estar rodando simultaneamente para funcionalidade completa.

## 📊 Funcionalidades Disponíveis

### ✅ Frontend React (Completo)
- ✅ Dashboard com resumo financeiro
- ✅ Gestão de transações (receitas/despesas)
- ✅ Sistema de metas financeiras
- ✅ Relatórios e gráficos
- ✅ Tema escuro/claro
- ✅ Design responsivo
- ✅ Validação de formulários

### ✅ Backend Django (Completo)
- ✅ API REST completa
- ✅ Autenticação JWT
- ✅ CRUD de usuários
- ✅ CRUD de transações
- ✅ CRUD de metas
- ✅ CRUD de categorias
- ✅ Relatórios e resumos
- ✅ Documentação Swagger

## 🔧 Próximos Passos para Integração

### 1. Conectar Frontend com Backend
O arquivo `frontend/src/services/api.js` já foi criado com todos os métodos necessários para integrar com o backend Django.

### 2. Substituir dados mockados
Nos componentes React, substituir dados estáticos pelos dados reais da API:

```javascript
// Exemplo: Em vez de dados mockados
const [transactions, setTransactions] = useState(mockData);

// Usar dados da API
import apiService from '../services/api';

useEffect(() => {
  const fetchTransactions = async () => {
    try {
      const data = await apiService.getTransactions();
      setTransactions(data.results);
    } catch (error) {
      console.error('Erro ao buscar transações:', error);
    }
  };
  
  fetchTransactions();
}, []);
```

### 3. Implementar autenticação
Adicionar sistema de login/logout no frontend que se conecta com a API Django.

## 🐛 Troubleshooting

### Problema: CORS Error
**Solução:** Verifique se o backend está configurado para aceitar requisições do frontend:
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`

### Problema: API não encontrada
**Solução:** Certifique-se que ambos servidores estão rodando:
```bash
# Verificar se portas estão em uso
netstat -an | findstr :8000  # Backend
netstat -an | findstr :3000  # Frontend
```

### Problema: Dependências
**Solução:** Reinstalar dependências:
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

## 📚 Documentação Adicional

- **API Backend:** `http://localhost:8000/api/docs/`
- **README Backend:** `backend/README.md`
- **Código Frontend:** Totalmente modularizado em `frontend/src/`

## 🎉 Conclusão

Agora você tem:
- ✅ Frontend React completo e funcional
- ✅ Backend Django com API REST completa
- ✅ Configuração de desenvolvimento pronta
- ✅ Dados de teste para desenvolvimento
- ✅ Documentação completa

**O sistema está pronto para desenvolvimento e integração!** 🚀

Para continuar o desenvolvimento, basta conectar os componentes React com as APIs Django usando o arquivo `api.js` já criado.
