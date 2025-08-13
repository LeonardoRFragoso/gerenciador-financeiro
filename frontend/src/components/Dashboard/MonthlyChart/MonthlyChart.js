import React from 'react';
import Card from '../../UI/Card/Card';
import './MonthlyChart.css';

const MonthlyChart = () => {
  const monthlyData = [
    { month: 'Jan', income: 8500, expense: 3200 },
    { month: 'Fev', income: 7800, expense: 2900 },
    { month: 'Mar', income: 9200, expense: 3500 },
    { month: 'Abr', income: 8100, expense: 3100 },
    { month: 'Mai', income: 8900, expense: 3300 },
    { month: 'Jun', income: 8500, expense: 3247 }
  ];

  const maxValue = Math.max(...monthlyData.map(d => Math.max(d.income, d.expense)));

  return (
    <Card className="monthly-chart">
      <div className="chart-header">
        <h3 className="chart-title">Visão Mensal</h3>
        <div className="chart-legend">
          <div className="legend-item">
            <span className="legend-color income"></span>
            <span className="legend-label">Receitas</span>
          </div>
          <div className="legend-item">
            <span className="legend-color expense"></span>
            <span className="legend-label">Despesas</span>
          </div>
        </div>
      </div>
      
      <div className="chart-container">
        {monthlyData.map((data, index) => (
          <div key={index} className="chart-bar-group">
            <div className="chart-bars">
              <div 
                className="chart-bar income"
                style={{ height: `${(data.income / maxValue) * 100}%` }}
                title={`Receita: R$ ${data.income.toLocaleString()}`}
              ></div>
              <div 
                className="chart-bar expense"
                style={{ height: `${(data.expense / maxValue) * 100}%` }}
                title={`Despesa: R$ ${data.expense.toLocaleString()}`}
              ></div>
            </div>
            <span className="chart-label">{data.month}</span>
          </div>
        ))}
      </div>
    </Card>
  );
};

export default MonthlyChart;
