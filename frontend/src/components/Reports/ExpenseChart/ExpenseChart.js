import React from 'react';
import Card from '../../UI/Card/Card';
import './ExpenseChart.css';

const ExpenseChart = ({ period }) => {
  const expenseData = [
    { category: 'Alimentação', amount: 1247.50, percentage: 38, color: '#ff6b6b' },
    { category: 'Transporte', amount: 850.00, percentage: 26, color: '#4ecdc4' },
    { category: 'Entretenimento', amount: 520.30, percentage: 16, color: '#45b7d1' },
    { category: 'Saúde', amount: 430.88, percentage: 13, color: '#96ceb4' },
    { category: 'Outros', amount: 199.00, percentage: 7, color: '#feca57' }
  ];

  const total = expenseData.reduce((sum, item) => sum + item.amount, 0);

  return (
    <Card className="expense-chart">
      <div className="chart-header">
        <h3 className="chart-title">Despesas por Categoria</h3>
        <span className="chart-total">R$ {total.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</span>
      </div>
      
      <div className="donut-chart">
        <svg viewBox="0 0 200 200" className="donut-svg">
          <circle
            cx="100"
            cy="100"
            r="80"
            fill="none"
            stroke="var(--color-gray-light)"
            strokeWidth="20"
          />
          {expenseData.map((item, index) => {
            const circumference = 2 * Math.PI * 80;
            const strokeDasharray = `${(item.percentage / 100) * circumference} ${circumference}`;
            const rotation = expenseData.slice(0, index).reduce((sum, prev) => sum + prev.percentage, 0) * 3.6;
            
            return (
              <circle
                key={item.category}
                cx="100"
                cy="100"
                r="80"
                fill="none"
                stroke={item.color}
                strokeWidth="20"
                strokeDasharray={strokeDasharray}
                strokeDashoffset="0"
                transform={`rotate(${rotation - 90} 100 100)`}
                className="donut-segment"
              />
            );
          })}
        </svg>
        
        <div className="donut-center">
          <span className="donut-label">Total</span>
          <span className="donut-value">R$ {total.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</span>
        </div>
      </div>
      
      <div className="chart-legend">
        {expenseData.map((item) => (
          <div key={item.category} className="legend-item">
            <div className="legend-color" style={{ backgroundColor: item.color }}></div>
            <div className="legend-info">
              <span className="legend-category">{item.category}</span>
              <span className="legend-amount">R$ {item.amount.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</span>
            </div>
            <span className="legend-percentage">{item.percentage}%</span>
          </div>
        ))}
      </div>
    </Card>
  );
};

export default ExpenseChart;
