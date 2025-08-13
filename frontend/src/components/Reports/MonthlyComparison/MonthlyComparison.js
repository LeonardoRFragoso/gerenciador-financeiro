import React from 'react';
import Card from '../../UI/Card/Card';
import './MonthlyComparison.css';

const MonthlyComparison = ({ period }) => {
  const comparisonData = [
    { metric: 'Receitas', current: 8500, previous: 7600, icon: '📈', type: 'income' },
    { metric: 'Despesas', current: 3247.68, previous: 2890.50, icon: '📉', type: 'expense' },
    { metric: 'Investimentos', current: 1200, previous: 800, icon: '💎', type: 'investment' },
    { metric: 'Economia', current: 4052.32, previous: 3909.50, icon: '💰', type: 'savings' }
  ];

  const getChangePercentage = (current, previous) => {
    return ((current - previous) / previous) * 100;
  };

  const getChangeColor = (change, type) => {
    if (type === 'expense') {
      return change > 0 ? '#ff6b6b' : 'var(--color-success)';
    }
    return change > 0 ? 'var(--color-success)' : '#ff6b6b';
  };

  return (
    <Card className="monthly-comparison">
      <div className="chart-header">
        <h3 className="chart-title">Comparação Mensal</h3>
        <span className="chart-subtitle">Este mês vs mês anterior</span>
      </div>
      
      <div className="comparison-grid">
        {comparisonData.map((item) => {
          const change = getChangePercentage(item.current, item.previous);
          const changeColor = getChangeColor(change, item.type);
          const isPositive = change > 0;
          
          return (
            <div key={item.metric} className="comparison-item">
              <div className="comparison-header">
                <span className="comparison-icon">{item.icon}</span>
                <span className="comparison-metric">{item.metric}</span>
              </div>
              
              <div className="comparison-values">
                <div className="value-current">
                  <span className="value-label">Atual</span>
                  <span className="value-amount">
                    R$ {item.current.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                  </span>
                </div>
                
                <div className="value-previous">
                  <span className="value-label">Anterior</span>
                  <span className="value-amount">
                    R$ {item.previous.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                  </span>
                </div>
              </div>
              
              <div className="comparison-change">
                <span 
                  className="change-indicator"
                  style={{ color: changeColor }}
                >
                  {isPositive ? '↗' : '↘'} {Math.abs(change).toFixed(1)}%
                </span>
                <span className="change-amount" style={{ color: changeColor }}>
                  {isPositive ? '+' : ''}R$ {(item.current - item.previous).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                </span>
              </div>
              
              <div className="comparison-bar">
                <div className="bar-background">
                  <div 
                    className="bar-fill"
                    style={{ 
                      width: `${(item.current / Math.max(item.current, item.previous)) * 100}%`,
                      backgroundColor: changeColor
                    }}
                  ></div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
      
      <div className="comparison-summary">
        <div className="summary-highlight">
          <span className="highlight-icon">🎯</span>
          <div className="highlight-content">
            <span className="highlight-title">Destaque do Mês</span>
            <span className="highlight-desc">Investimentos cresceram 50% - excelente progresso!</span>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default MonthlyComparison;
