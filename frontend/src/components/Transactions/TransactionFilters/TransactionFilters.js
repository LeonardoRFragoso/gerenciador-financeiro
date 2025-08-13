import React from 'react';
import Card from '../../UI/Card/Card';
import Button from '../../UI/Button/Button';
import './TransactionFilters.css';

const TransactionFilters = ({ filters, onFiltersChange }) => {
  const handleFilterChange = (key, value) => {
    onFiltersChange(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const clearFilters = () => {
    onFiltersChange({
      type: 'all',
      category: 'all',
      dateRange: 'month'
    });
  };

  return (
    <Card className="transaction-filters">
      <div className="filters-header">
        <h3 className="filters-title">Filtros</h3>
        <Button variant="ghost" size="small" onClick={clearFilters}>
          Limpar
        </Button>
      </div>
      
      <div className="filter-group">
        <label className="filter-label">Tipo</label>
        <div className="filter-options">
          <button
            className={`filter-btn ${filters.type === 'all' ? 'active' : ''}`}
            onClick={() => handleFilterChange('type', 'all')}
          >
            Todos
          </button>
          <button
            className={`filter-btn ${filters.type === 'income' ? 'active' : ''}`}
            onClick={() => handleFilterChange('type', 'income')}
          >
            📈 Receitas
          </button>
          <button
            className={`filter-btn ${filters.type === 'expense' ? 'active' : ''}`}
            onClick={() => handleFilterChange('type', 'expense')}
          >
            📉 Despesas
          </button>
        </div>
      </div>
      
      <div className="filter-group">
        <label className="filter-label">Período</label>
        <select
          value={filters.dateRange}
          onChange={(e) => handleFilterChange('dateRange', e.target.value)}
          className="filter-select"
        >
          <option value="week">Esta semana</option>
          <option value="month">Este mês</option>
          <option value="quarter">Este trimestre</option>
          <option value="year">Este ano</option>
          <option value="all">Todos os períodos</option>
        </select>
      </div>
      
      <div className="filter-group">
        <label className="filter-label">Categoria</label>
        <select
          value={filters.category}
          onChange={(e) => handleFilterChange('category', e.target.value)}
          className="filter-select"
        >
          <option value="all">Todas as categorias</option>
          <option value="Trabalho">💼 Trabalho</option>
          <option value="Alimentação">🍽️ Alimentação</option>
          <option value="Transporte">🚗 Transporte</option>
          <option value="Entretenimento">🎬 Entretenimento</option>
          <option value="Saúde">🏥 Saúde</option>
          <option value="Educação">📚 Educação</option>
          <option value="Moradia">🏠 Moradia</option>
          <option value="Investimentos">📈 Investimentos</option>
        </select>
      </div>
      
      <div className="filter-summary">
        <div className="summary-item">
          <span className="summary-label">Transações encontradas</span>
          <span className="summary-value">8</span>
        </div>
        <div className="summary-item">
          <span className="summary-label">Total do período</span>
          <span className="summary-value positive">+R$ 5.252,32</span>
        </div>
      </div>
    </Card>
  );
};

export default TransactionFilters;
