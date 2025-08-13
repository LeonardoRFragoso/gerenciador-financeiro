import React, { useState } from 'react';
import Card from '../../components/UI/Card/Card';
import Button from '../../components/UI/Button/Button';
import ExpenseChart from '../../components/Reports/ExpenseChart/ExpenseChart';
import IncomeChart from '../../components/Reports/IncomeChart/IncomeChart';
import CategoryBreakdown from '../../components/Reports/CategoryBreakdown/CategoryBreakdown';
import MonthlyComparison from '../../components/Reports/MonthlyComparison/MonthlyComparison';
import './Reports.css';

const Reports = () => {
  const [selectedPeriod, setSelectedPeriod] = useState('month');

  const periods = [
    { value: 'week', label: 'Esta Semana' },
    { value: 'month', label: 'Este Mês' },
    { value: 'quarter', label: 'Trimestre' },
    { value: 'year', label: 'Este Ano' }
  ];

  return (
    <div className="reports-page">
      <div className="reports-header">
        <div className="reports-controls">
          <h2 className="reports-subtitle">Análise Financeira</h2>
          <div className="period-selector">
            {periods.map(period => (
              <button
                key={period.value}
                className={`period-btn ${selectedPeriod === period.value ? 'active' : ''}`}
                onClick={() => setSelectedPeriod(period.value)}
              >
                {period.label}
              </button>
            ))}
          </div>
        </div>
        
        <div className="reports-actions">
          <Button variant="outline" icon="📊">Exportar PDF</Button>
          <Button variant="accent" icon="📈">Gerar Relatório</Button>
        </div>
      </div>
      
      <div className="reports-grid">
        <div className="reports-summary">
          <Card className="summary-card positive">
            <div className="summary-icon">📈</div>
            <div className="summary-content">
              <span className="summary-value">R$ 8.500,00</span>
              <span className="summary-label">Total de Receitas</span>
              <span className="summary-change positive">+15% vs mês anterior</span>
            </div>
          </Card>
          
          <Card className="summary-card negative">
            <div className="summary-icon">📉</div>
            <div className="summary-content">
              <span className="summary-value">R$ 3.247,68</span>
              <span className="summary-label">Total de Despesas</span>
              <span className="summary-change negative">+8% vs mês anterior</span>
            </div>
          </Card>
          
          <Card className="summary-card balance">
            <div className="summary-icon">💰</div>
            <div className="summary-content">
              <span className="summary-value">R$ 5.252,32</span>
              <span className="summary-label">Saldo Líquido</span>
              <span className="summary-change positive">+23% vs mês anterior</span>
            </div>
          </Card>
        </div>
        
        <div className="reports-charts">
          <div className="chart-section">
            <ExpenseChart period={selectedPeriod} />
          </div>
          
          <div className="chart-section">
            <IncomeChart period={selectedPeriod} />
          </div>
          
          <div className="chart-section">
            <CategoryBreakdown period={selectedPeriod} />
          </div>
          
          <div className="chart-section">
            <MonthlyComparison period={selectedPeriod} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Reports;
