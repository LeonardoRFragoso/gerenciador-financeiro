import React, { useState, useEffect } from 'react';
import Card from '../../UI/Card/Card';
import Button from '../../UI/Button/Button';
import apiService from '../../../services/api';
import { useToast } from '../../../contexts/ToastContext';
import './RecentTransactions.css';

const RecentTransactions = () => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const { showError } = useToast();

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        setLoading(true);
        const data = await apiService.getTransactions({ 
          ordering: '-date',
          page_size: 5 
        });
        setTransactions(data.results || []);
      } catch (error) {
        console.error('Erro ao carregar transações:', error);
        showError('Erro ao carregar transações recentes');
      } finally {
        setLoading(false);
      }
    };

    fetchTransactions();
  }, [showError]);

  const getCategoryIcon = (category) => {
    const icons = {
      'Trabalho': '💼',
      'Alimentação': '🍽️',
      'Transporte': '🚗',
      'Entretenimento': '🎬',
      'Saúde': '🏥',
      'Educação': '📚'
    };
    return icons[category] || '💰';
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(Math.abs(value || 0));
  };

  const handleViewAll = () => {
    window.location.href = '/transactions';
  };

  if (loading) {
    return (
      <Card className="recent-transactions">
        <div className="transactions-header">
          <h3 className="transactions-title">Transações Recentes</h3>
        </div>
        <div className="transactions-loading">
          <div className="loading-spinner"></div>
          <span>Carregando transações...</span>
        </div>
      </Card>
    );
  }

  return (
    <Card className="recent-transactions">
      <div className="transactions-header">
        <h3 className="transactions-title">Transações Recentes</h3>
        <Button variant="ghost" size="small" onClick={handleViewAll}>
          Ver todas
        </Button>
      </div>
      
      <div className="transactions-list">
        {transactions.length === 0 ? (
          <div className="no-transactions">
            <span>Nenhuma transação encontrada</span>
            <p>Adicione sua primeira transação usando as ações rápidas acima</p>
          </div>
        ) : (
          transactions.map((transaction) => (
            <div key={transaction.id} className="transaction-item">
              <div className="transaction-icon">
                {getCategoryIcon(transaction.category?.name || 'Outros')}
              </div>
              
              <div className="transaction-info">
                <div className="transaction-description">{transaction.description}</div>
                <div className="transaction-category">
                  {transaction.category?.name || 'Sem categoria'}
                </div>
              </div>
              
              <div className="transaction-amount-container">
                <div className={`transaction-amount ${transaction.type}`}>
                  {transaction.type === 'income' ? '+' : '-'}{formatCurrency(transaction.amount)}
                </div>
                <div className="transaction-date">
                  {new Date(transaction.date).toLocaleDateString('pt-BR')}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </Card>
  );
};

export default RecentTransactions;
