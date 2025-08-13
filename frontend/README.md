# 💰 FinanceControl - Frontend

Uma aplicação completa de gestão financeira pessoal desenvolvida em React com design moderno e intuitivo.

## 🎨 Design

- **Cores**: Branco, preto, cinza e dourado
- **Estilo**: Simples, intuitivo, futurista e inovador
- **Responsivo**: Funciona perfeitamente em desktop, tablet e mobile
- **Tema Escuro**: Alternância completa entre tema claro e escuro

## 🚀 Funcionalidades

### 📊 Dashboard
- Visão geral do saldo com breakdown de receitas e despesas
- Ações rápidas para transações comuns
- Gráfico mensal de evolução financeira
- Lista de transações recentes

### 💳 Transações
- Gerenciamento completo de transações
- Formulário para adicionar receitas e despesas
- Filtros avançados (tipo, categoria, período)
- Estatísticas mensais em tempo real

### 📈 Relatórios
- Gráfico de despesas por categoria (donut chart)
- Evolução de receitas (bar chart)
- Comparação de orçamento por categoria
- Análise mensal comparativa

### 🎯 Metas
- Criação e acompanhamento de metas financeiras
- Barras de progresso visuais
- Categorização por prioridade
- Sugestões de economia mensal

### ⚙️ Configurações
- Perfil do usuário
- Preferências de notificação
- Controles de privacidade
- Configurações de tema e formatação

## 🛠️ Tecnologias

- **React 18** - Framework principal
- **React Router DOM** - Navegação entre páginas
- **CSS Modules** - Estilização modular
- **Context API** - Gerenciamento de estado (tema)

## 📁 Estrutura do Projeto

```
src/
├── components/
│   ├── Layout/           # Layout principal da aplicação
│   ├── UI/              # Componentes reutilizáveis (Card, Button)
│   ├── Dashboard/       # Componentes específicos do Dashboard
│   ├── Transactions/    # Componentes de transações
│   ├── Reports/         # Componentes de relatórios
│   └── Goals/           # Componentes de metas
├── pages/               # Páginas principais
├── contexts/            # Contextos React (ThemeContext)
└── styles/              # Estilos globais
```

## 🎯 Arquitetura

- **Componentes Modulares**: Cada funcionalidade é dividida em pequenos componentes reutilizáveis
- **Separação de Responsabilidades**: Lógica, apresentação e estilos bem organizados
- **Context API**: Gerenciamento de estado global para tema
- **CSS Custom Properties**: Sistema de cores consistente

## 🌙 Sistema de Temas

A aplicação possui alternância completa entre tema claro e escuro:

- **Botão no Header**: Clique no ícone 🌙/☀️ para alternar
- **Configurações**: Também pode ser alterado na página de configurações
- **Persistência**: Preferência salva no localStorage
- **Sistema**: Detecta preferência do sistema automaticamente

## 🚀 Como Executar

1. **Instalar dependências:**
   ```bash
   npm install
   ```

2. **Executar em desenvolvimento:**
   ```bash
   npm start
   ```

3. **Acessar a aplicação:**
   ```
   http://localhost:3000
   ```

## 📱 Responsividade

A aplicação é totalmente responsiva com breakpoints:

- **Desktop**: > 1024px
- **Tablet**: 768px - 1024px  
- **Mobile**: < 768px

## 🎨 Paleta de Cores

### Tema Claro
- **Primária**: #000000 (Preto)
- **Secundária**: #ffffff (Branco)
- **Accent**: #FFD700 (Dourado)
- **Cinza Claro**: #f5f5f5
- **Cinza Médio**: #9e9e9e
- **Cinza Escuro**: #424242

### Tema Escuro
- **Primária**: #ffffff (Branco)
- **Secundária**: #1a1a1a (Preto escuro)
- **Accent**: #FFD700 (Dourado)
- **Cinza Claro**: #2d2d2d
- **Cinza Médio**: #888888
- **Cinza Escuro**: #cccccc

## 🔄 Próximos Passos

Para integração com backend:

1. **API Integration**: Conectar com endpoints REST
2. **Estado Global**: Implementar Redux ou Zustand se necessário
3. **Autenticação**: Adicionar sistema de login/logout
4. **Validação**: Implementar validação de formulários
5. **Testes**: Adicionar testes unitários e de integração

## 📄 Licença

Este projeto foi desenvolvido para uso pessoal e educacional.
