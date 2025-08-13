import React, { useState, useEffect } from 'react';
import Card from '../../UI/Card/Card';
import Button from '../../UI/Button/Button';
import apiService from '../../../services/api';
import { useToast } from '../../../contexts/ToastContext';
import './TransactionList.css';

const TransactionList = ({ filters, refreshTrigger }) => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const { showError } = useToast();

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        setLoading(true);
        const params = {
          page: 1,
          page_size: 20,
          ordering: '-date'
        };

        // Apply filters
        if (filters.type && filters.type !== 'all') {
          params.type = filters.type;
        }
        if (filters.category && filters.category !== 'all') {
          params.category = filters.category;
        }

        const data = await apiService.getTransactions(params);
        setTransactions(data.results || []);
        setHasMore(!!data.next);
        setPage(1);
      } catch (error) {
        console.error('Erro ao carregar transações:', error);
        showError('Erro ao carregar transações');
      } finally {
        setLoading(false);
      }
    };

    fetchTransactions();
  }, [filters, refreshTrigger, showError]);

  const loadMore = async () => {
    try {
      const params = {
        page: page + 1,
        page_size: 20,
        ordering: '-date'
      };

      if (filters.type && filters.type !== 'all') {
        params.type = filters.type;
      }
      if (filters.category && filters.category !== 'all') {
        params.category = filters.category;
      }

      const data = await apiService.getTransactions(params);
      setTransactions(prev => [...prev, ...(data.results || [])]);
      setHasMore(!!data.next);
      setPage(prev => prev + 1);
    } catch (error) {
      console.error('Erro ao carregar mais transações:', error);
      showError('Erro ao carregar mais transações');
    }
  };

  const getCategoryIcon = (category) => {
    const icons = {
      'Trabalho': '💼',
      'Alimentação': '🍽️',
      'Transporte': '🚗',
      'Entretenimento': '🎬',
      'Saúde': '🏥',
      'Educação': '📚',
      'Investimentos': '📈',
      'Moradia': '🏠'
    };
    return icons[category] || '💰';
  };

  const getTypeIcon = (type) => {
    return type === 'income' ? '📈' : '📉';
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(Math.abs(value || 0));
  };

  if (loading) {
    return (
      <Card className="transaction-list">
        <div className="list-header">
          <h3 className="list-title">Todas as Transações</h3>
        </div>
        <div className="transactions-loading">
          <div className="loading-spinner"></div>
          <span>Carregando transações...</span>
        </div>
      </Card>
    );
  }

  return (
    <Card className="transaction-list">
      <div className="list-header">
        <h3 className="list-title">Todas as Transações</h3>
        <span className="list-count">{transactions.length} transações</span>
      </div>
      
      <div className="transactions">
        {transactions.length === 0 ? (
          <div className="no-transactions">
            <div className="no-transactions-icon">📊</div>
            <h4>Nenhuma transação encontrada</h4>
            <p>Adicione sua primeira transação para começar a controlar suas finanças</p>
          </div>
        ) : (
          <>
            {transactions.map((transaction) => (
              <div key={transaction.id} className="transaction-row">
                <div className="transaction-main">
                  <div className="transaction-icons">
                    <span className="category-icon">
                      {getCategoryIcon(transaction.category?.name || 'Outros')}
                    </span>
                    <span className={`type-icon ${transaction.type}`}>
                      {getTypeIcon(transaction.type)}
                    </span>
                  </div>
                  
                  <div className="transaction-details">
                    <div className="transaction-description">{transaction.description}</div>
                    <div className="transaction-meta">
                      <span className="transaction-category">
                        {transaction.category?.name || 'Sem categoria'}
                      </span>
                      <span className="transaction-separator">•</span>
                      <span className="transaction-date">
                        {new Date(transaction.date).toLocaleDateString('pt-BR')}
                      </span>
                      {transaction.payment_method && (
                        <>
                          <span className="transaction-separator">•</span>
                          <span className="transaction-payment">
                            {transaction.payment_method.replace('_', ' ')}
                          </span>
                        </>
                      )}
                    </div>
                  </div>
                </div>
                
                <div className="transaction-amount-section">
                  <div className={`transaction-amount ${transaction.type}`}>
                    {transaction.type === 'income' ? '+' : '-'}{formatCurrency(transaction.amount)}
                  </div>
                </div>
              </div>
            ))}
            
            {hasMore && (
              <div className="load-more-container">
                <Button 
                  variant="outline" 
                  onClick={loadMore}
                  className="load-more-btn"
                >
                  Carregar mais transações
                </Button>
              </div>
            )}
          </>
        )}
      </div>
    </Card>
  );
};

export default TransactionList;
