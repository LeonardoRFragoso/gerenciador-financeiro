import React from 'react';
import Card from '../../UI/Card/Card';
import './CategoryBreakdown.css';

const CategoryBreakdown = ({ period }) => {
  const categoryData = [
    { category: 'Alimentação', icon: '🍽️', budget: 1500, spent: 1247.50, trend: 'down' },
    { category: 'Transporte', icon: '🚗', budget: 800, spent: 850.00, trend: 'up' },
    { category: 'Entretenimento', icon: '🎬', budget: 600, spent: 520.30, trend: 'down' },
    { category: 'Saúde', icon: '🏥', budget: 500, spent: 430.88, trend: 'stable' },
    { category: 'Educação', icon: '📚', budget: 300, spent: 199.00, trend: 'down' }
  ];

  const getProgressColor = (spent, budget) => {
    const percentage = (spent / budget) * 100;
    if (percentage > 90) return '#ff6b6b';
    if (percentage > 70) return '#feca57';
    return 'var(--color-success)';
  };

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'up': return '📈';
      case 'down': return '📉';
      default: return '➡️';
    }
  };

  return (
    <Card className="category-breakdown">
      <div className="chart-header">
        <h3 className="chart-title">Orçamento por Categoria</h3>
        <span className="chart-subtitle">Comparação com metas definidas</span>
      </div>
      
      <div className="category-list">
        {categoryData.map((item) => {
          const percentage = (item.spent / item.budget) * 100;
          const remaining = item.budget - item.spent;
          
          return (
            <div key={item.category} className="category-item">
              <div className="category-header">
                <div className="category-info">
                  <span className="category-icon">{item.icon}</span>
                  <div className="category-details">
                    <span className="category-name">{item.category}</span>
                    <span className="category-trend">
                      {getTrendIcon(item.trend)} vs mês anterior
                    </span>
                  </div>
                </div>
                
                <div className="category-amounts">
                  <span className="amount-spent">
                    R$ {item.spent.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                  </span>
                  <span className="amount-budget">
                    / R$ {item.budget.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                  </span>
                </div>
              </div>
              
              <div className="category-progress">
                <div className="progress-bar">
                  <div 
                    className="progress-fill"
                    style={{ 
                      width: `${Math.min(percentage, 100)}%`,
                      backgroundColor: getProgressColor(item.spent, item.budget)
                    }}
                  ></div>
                </div>
                
                <div className="progress-info">
                  <span className={`progress-percentage ${percentage > 90 ? 'warning' : ''}`}>
                    {percentage.toFixed(0)}%
                  </span>
                  <span className={`progress-remaining ${remaining < 0 ? 'over-budget' : ''}`}>
                    {remaining >= 0 
                      ? `R$ ${remaining.toLocaleString('pt-BR', { minimumFractionDigits: 2 })} restante`
                      : `R$ ${Math.abs(remaining).toLocaleString('pt-BR', { minimumFractionDigits: 2 })} acima`
                    }
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
};

export default CategoryBreakdown;
