import React, { useState, useEffect } from 'react';
import Card from '../../UI/Card/Card';
import apiService from '../../../services/api';
import { useToast } from '../../../contexts/ToastContext';
import './BalanceCard.css';

const BalanceCard = () => {
  const [summary, setSummary] = useState({
    total_balance: 0,
    total_income: 0,
    total_expenses: 0,
    balance_change: 0
  });
  const [loading, setLoading] = useState(true);
  const { showError } = useToast();

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
  }, [showError]);

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value || 0);
  };

  const getBalanceChangeIcon = () => {
    if (summary.balance_change > 0) return '↗';
    if (summary.balance_change < 0) return '↘';
    return '→';
  };

  const getBalanceChangeClass = () => {
    if (summary.balance_change > 0) return 'positive';
    if (summary.balance_change < 0) return 'negative';
    return 'neutral';
  };

  const calculatePercentage = (value, total) => {
    if (!total) return 0;
    return Math.abs((value / total) * 100);
  };

  if (loading) {
    return (
      <Card className="balance-card">
        <div className="balance-loading">
          <div className="loading-spinner"></div>
          <span>Carregando dados...</span>
        </div>
      </Card>
    );
  }

  return (
    <Card className="balance-card">
      <div className="balance-header">
        <h3 className="balance-title">Saldo Total</h3>
        <span className="balance-period">Este mês</span>
      </div>
      
      <div className="balance-amount">
        <span className="balance-currency">R$</span>
        <span className="balance-value">
          {formatCurrency(summary.total_balance).replace('R$', '').trim()}
        </span>
      </div>
      
      <div className="balance-change">
        <span className={`balance-change-icon ${getBalanceChangeClass()}`}>
          {getBalanceChangeIcon()}
        </span>
        <span className="balance-change-text">
          {summary.balance_change > 0 ? '+' : ''}{summary.balance_change.toFixed(1)}% em relação ao mês anterior
        </span>
      </div>
      
      <div className="balance-breakdown">
        <div className="balance-item">
          <div className="balance-item-info">
            <span className="balance-item-label">Receitas</span>
            <span className="balance-item-amount positive">
              {formatCurrency(summary.total_income)}
            </span>
          </div>
          <div className="balance-item-bar">
            <div 
              className="balance-item-progress positive" 
              style={{
                width: `${calculatePercentage(summary.total_income, summary.total_income + Math.abs(summary.total_expenses))}%`
              }}
            ></div>
          </div>
        </div>
        
        <div className="balance-item">
          <div className="balance-item-info">
            <span className="balance-item-label">Despesas</span>
            <span className="balance-item-amount negative">
              {formatCurrency(summary.total_expenses)}
            </span>
          </div>
          <div className="balance-item-bar">
            <div 
              className="balance-item-progress negative" 
              style={{
                width: `${calculatePercentage(summary.total_expenses, summary.total_income + Math.abs(summary.total_expenses))}%`
              }}
            ></div>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default BalanceCard;
