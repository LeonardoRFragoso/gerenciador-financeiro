import React from 'react';
import Card from '../../UI/Card/Card';
import Button from '../../UI/Button/Button';
import './GoalCard.css';

const GoalCard = ({ goal }) => {
  const progress = (goal.currentAmount / goal.targetAmount) * 100;
  const remaining = goal.targetAmount - goal.currentAmount;
  const daysLeft = Math.ceil((new Date(goal.deadline) - new Date()) / (1000 * 60 * 60 * 24));
  
  const getCategoryIcon = (category) => {
    const icons = {
      emergency: '🚨',
      travel: '✈️',
      technology: '💻',
      education: '📚',
      home: '🏠',
      car: '🚗',
      health: '🏥',
      investment: '📈'
    };
    return icons[category] || '🎯';
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return '#ff6b6b';
      case 'medium': return '#feca57';
      case 'low': return 'var(--color-success)';
      default: return 'var(--color-gray-medium)';
    }
  };

  const getStatusColor = () => {
    if (progress >= 100) return 'var(--color-success)';
    if (progress >= 75) return 'var(--color-accent)';
    if (progress >= 50) return '#4ecdc4';
    return '#ff6b6b';
  };

  return (
    <Card className="goal-card">
      <div className="goal-header">
        <div className="goal-info">
          <span className="goal-icon">{getCategoryIcon(goal.category)}</span>
          <div className="goal-details">
            <h3 className="goal-title">{goal.title}</h3>
            <p className="goal-description">{goal.description}</p>
          </div>
        </div>
        
        <div className="goal-priority">
          <span 
            className="priority-indicator"
            style={{ backgroundColor: getPriorityColor(goal.priority) }}
          ></span>
        </div>
      </div>
      
      <div className="goal-progress">
        <div className="progress-header">
          <span className="progress-label">Progresso</span>
          <span className="progress-percentage">{progress.toFixed(1)}%</span>
        </div>
        
        <div className="progress-bar">
          <div 
            className="progress-fill"
            style={{ 
              width: `${Math.min(progress, 100)}%`,
              backgroundColor: getStatusColor()
            }}
          ></div>
        </div>
        
        <div className="progress-amounts">
          <span className="current-amount">
            R$ {goal.currentAmount.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
          </span>
          <span className="target-amount">
            R$ {goal.targetAmount.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
          </span>
        </div>
      </div>
      
      <div className="goal-stats">
        <div className="stat-item">
          <span className="stat-icon">💰</span>
          <div className="stat-info">
            <span className="stat-value">R$ {remaining.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</span>
            <span className="stat-label">Restante</span>
          </div>
        </div>
        
        <div className="stat-item">
          <span className="stat-icon">📅</span>
          <div className="stat-info">
            <span className="stat-value">{daysLeft > 0 ? `${daysLeft} dias` : 'Vencido'}</span>
            <span className="stat-label">Prazo</span>
          </div>
        </div>
      </div>
      
      <div className="goal-actions">
        <Button variant="outline" size="small">
          Editar
        </Button>
        <Button variant="accent" size="small" icon="+">
          Adicionar Valor
        </Button>
      </div>
      
      {progress >= 100 && (
        <div className="goal-completed">
          <span className="completed-icon">🎉</span>
          <span className="completed-text">Meta Concluída!</span>
        </div>
      )}
    </Card>
  );
};

export default GoalCard;
