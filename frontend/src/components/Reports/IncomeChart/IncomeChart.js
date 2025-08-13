import React from 'react';
import Card from '../../UI/Card/Card';
import './IncomeChart.css';

const IncomeChart = ({ period }) => {
  const incomeData = [
    { month: 'Jan', amount: 8500 },
    { month: 'Fev', amount: 7800 },
    { month: 'Mar', amount: 9200 },
    { month: 'Abr', amount: 8100 },
    { month: 'Mai', amount: 8900 },
    { month: 'Jun', amount: 8500 }
  ];

  const maxAmount = Math.max(...incomeData.map(d => d.amount));
  const totalIncome = incomeData.reduce((sum, item) => sum + item.amount, 0);
  const avgIncome = totalIncome / incomeData.length;

  return (
    <Card className="income-chart">
      <div className="chart-header">
        <h3 className="chart-title">Evolução de Receitas</h3>
        <div className="chart-stats">
          <span className="chart-stat">
            <span className="stat-label">Média:</span>
            <span className="stat-value">R$ {avgIncome.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</span>
          </span>
        </div>
      </div>
      
      <div className="line-chart">
        <div className="chart-grid">
          {[0, 25, 50, 75, 100].map(percentage => (
            <div key={percentage} className="grid-line" style={{ bottom: `${percentage}%` }}>
              <span className="grid-label">
                R$ {((maxAmount * percentage) / 100).toLocaleString('pt-BR', { maximumFractionDigits: 0 })}
              </span>
            </div>
          ))}
        </div>
        
        <div className="chart-bars">
          {incomeData.map((item, index) => {
            const height = (item.amount / maxAmount) * 100;
            return (
              <div key={item.month} className="bar-container">
                <div 
                  className="income-bar"
                  style={{ height: `${height}%` }}
                  title={`${item.month}: R$ ${item.amount.toLocaleString('pt-BR')}`}
                >
                  <div className="bar-value">
                    R$ {(item.amount / 1000).toFixed(1)}k
                  </div>
                </div>
                <span className="bar-label">{item.month}</span>
              </div>
            );
          })}
        </div>
      </div>
      
      <div className="chart-summary">
        <div className="summary-item">
          <span className="summary-icon">📈</span>
          <div className="summary-info">
            <span className="summary-title">Crescimento</span>
            <span className="summary-desc">+12% vs período anterior</span>
          </div>
        </div>
        <div className="summary-item">
          <span className="summary-icon">🎯</span>
          <div className="summary-info">
            <span className="summary-title">Meta Mensal</span>
            <span className="summary-desc">R$ 9.000 (94% atingido)</span>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default IncomeChart;
