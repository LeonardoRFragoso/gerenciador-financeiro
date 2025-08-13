import React, { useState, useEffect } from 'react';
import Card from '../../components/UI/Card/Card';
import Button from '../../components/UI/Button/Button';
import TransactionForm from '../../components/Transactions/TransactionForm/TransactionForm';
import TransactionList from '../../components/Transactions/TransactionList/TransactionList';
import TransactionFilters from '../../components/Transactions/TransactionFilters/TransactionFilters';
import apiService from '../../services/api';
import { useToast } from '../../contexts/ToastContext';
import './Transactions.css';

const Transactions = () => {
  const [showForm, setShowForm] = useState(false);
  const [summary, setSummary] = useState({
    total_income: 0,
    total_expenses: 0,
    total_balance: 0
  });
  const [loading, setLoading] = useState(true);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const { showError } = useToast();
  const [filters, setFilters] = useState({
    type: 'all',
    category: 'all',
    dateRange: 'month'
  });

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        setLoading(true);
        const data = await apiService.getTransactionSummary();
        setSummary(data);
      } catch (error) {
        console.error('Erro ao carregar resumo:', error);
        showError('Erro ao carregar dados financeiros');
      } finally {
        setLoading(false);
      }
    };

    fetchSummary();
  }, [showError, refreshTrigger]);

  const handleTransactionAdded = () => {
    // Trigger refresh of summary and transaction list
    setRefreshTrigger(prev => prev + 1);
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value || 0);
  };

  return (
    <div className="transactions-page">
      <div className="transactions-header">
        <div className="transactions-stats">
          {loading ? (
            <>
              <Card className="stat-card loading">
                <div className="loading-spinner"></div>
                <span>Carregando...</span>
              </Card>
              <Card className="stat-card loading">
                <div className="loading-spinner"></div>
                <span>Carregando...</span>
              </Card>
              <Card className="stat-card loading">
                <div className="loading-spinner"></div>
                <span>Carregando...</span>
              </Card>
            </>
          ) : (
            <>
              <Card className="stat-card income">
                <div className="stat-icon">📈</div>
                <div className="stat-info">
                  <span className="stat-value">+{formatCurrency(summary.total_income)}</span>
                  <span className="stat-label">Receitas do mês</span>
                </div>
              </Card>
              
              <Card className="stat-card expense">
                <div className="stat-icon">📉</div>
                <div className="stat-info">
                  <span className="stat-value">-{formatCurrency(Math.abs(summary.total_expenses))}</span>
                  <span className="stat-label">Despesas do mês</span>
                </div>
              </Card>
              
              <Card className="stat-card balance">
                <div className="stat-icon">💰</div>
                <div className="stat-info">
                  <span className="stat-value">{formatCurrency(summary.total_balance)}</span>
                  <span className="stat-label">Saldo líquido</span>
                </div>
              </Card>
            </>
          )}
        </div>
        
        <Button 
          variant="accent" 
          icon="+" 
          onClick={() => setShowForm(true)}
        >
          Nova Transação
        </Button>
      </div>
      
      <div className="transactions-content">
        <div className="transactions-filters">
          <TransactionFilters filters={filters} onFiltersChange={setFilters} />
        </div>
        
        <div className="transactions-list">
          <TransactionList filters={filters} refreshTrigger={refreshTrigger} />
        </div>
      </div>
      
      {showForm && (
        <TransactionForm 
          onClose={() => setShowForm(false)} 
          onTransactionAdded={handleTransactionAdded}
        />
      )}
    </div>
  );
};

export default Transactions;
