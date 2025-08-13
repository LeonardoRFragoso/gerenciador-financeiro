import React, { useState } from 'react';
import Card from '../../UI/Card/Card';
import Button from '../../UI/Button/Button';
import { useToast } from '../../../contexts/ToastContext';
import TransactionForm from '../../Transactions/TransactionForm/TransactionForm';
import GoalForm from '../../Goals/GoalForm/GoalForm';
import './QuickActions.css';

const QuickActions = () => {
  const [showTransactionForm, setShowTransactionForm] = useState(false);
  const [showGoalForm, setShowGoalForm] = useState(false);
  const [transactionType, setTransactionType] = useState('expense');

  const handleAddIncome = () => {
    setTransactionType('income');
    setShowTransactionForm(true);
  };

  const handleAddExpense = () => {
    setTransactionType('expense');
    setShowTransactionForm(true);
  };

  const handleNewGoal = () => {
    setShowGoalForm(true);
  };

  const handleViewReports = () => {
    window.location.href = '/reports';
  };

  const actions = [
    { icon: '💰', label: 'Adicionar Receita', variant: 'accent', onClick: handleAddIncome },
    { icon: '💸', label: 'Registrar Gasto', variant: 'outline', onClick: handleAddExpense },
    { icon: '🎯', label: 'Nova Meta', variant: 'ghost', onClick: handleNewGoal },
    { icon: '📊', label: 'Ver Relatório', variant: 'ghost', onClick: handleViewReports }
  ];

  return (
    <>
      <Card className="quick-actions">
        <h3 className="quick-actions-title">Ações Rápidas</h3>
        
        <div className="quick-actions-grid">
          {actions.map((action, index) => (
            <Button
              key={index}
              variant={action.variant}
              size="small"
              icon={action.icon}
              className="quick-action-btn"
              onClick={action.onClick}
            >
              {action.label}
            </Button>
          ))}
        </div>
      
        <div className="quick-stats">
          <div className="quick-stat">
            <span className="quick-stat-value">12</span>
            <span className="quick-stat-label">Transações hoje</span>
          </div>
          <div className="quick-stat">
            <span className="quick-stat-value">3</span>
            <span className="quick-stat-label">Metas ativas</span>
          </div>
        </div>
      </Card>

      {showTransactionForm && (
        <TransactionForm
          type={transactionType}
          fixedType={true}
          onClose={() => setShowTransactionForm(false)}
          onTransactionAdded={() => {
            setShowTransactionForm(false);
            // Trigger page refresh to update dashboard data
            window.location.reload();
          }}
        />
      )}

      {showGoalForm && (
        <GoalForm
          onClose={() => setShowGoalForm(false)}
        />
      )}
    </>
  );
};

export default QuickActions;
