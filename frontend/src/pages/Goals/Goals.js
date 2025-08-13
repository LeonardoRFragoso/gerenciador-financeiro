import React, { useState, useEffect } from 'react';
import Card from '../../components/UI/Card/Card';
import Button from '../../components/UI/Button/Button';
import GoalCard from '../../components/Goals/GoalCard/GoalCard';
import GoalForm from '../../components/Goals/GoalForm/GoalForm';
import apiService from '../../services/api';
import { useToast } from '../../contexts/ToastContext';
import './Goals.css';

const Goals = () => {
  const [showForm, setShowForm] = useState(false);
  const [goals, setGoals] = useState([]);
  const [summary, setSummary] = useState({
    total_goals: 0,
    active_goals: 0,
    completed_goals: 0,
    total_target_amount: 0,
    total_current_amount: 0,
    average_progress: 0
  });
  const [loading, setLoading] = useState(true);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const { showError } = useToast();

  useEffect(() => {
    const fetchGoalsData = async () => {
      try {
        setLoading(true);
        const [goalsData, summaryData] = await Promise.all([
          apiService.getGoals({ ordering: '-priority,target_date' }),
          apiService.getGoalSummary()
        ]);
        
        setGoals(goalsData.results || []);
        setSummary(summaryData);
      } catch (error) {
        console.error('Erro ao carregar metas:', error);
        showError('Erro ao carregar dados das metas');
      } finally {
        setLoading(false);
      }
    };

    fetchGoalsData();
  }, [showError, refreshTrigger]);

  const handleGoalAdded = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value || 0);
  };

  const calculateMonthlyTarget = () => {
    if (goals.length === 0) return 0;
    
    const now = new Date();
    let totalMonthlyNeeded = 0;
    
    goals.forEach(goal => {
      const targetDate = new Date(goal.target_date);
      const monthsRemaining = Math.max(1, Math.ceil((targetDate - now) / (1000 * 60 * 60 * 24 * 30)));
      const remainingAmount = Math.max(0, goal.target_amount - goal.current_amount);
      totalMonthlyNeeded += remainingAmount / monthsRemaining;
    });
    
    return totalMonthlyNeeded;
  };

  return (
    <div className="goals-page">
      <div className="goals-header">
        <div className="goals-stats">
          {loading ? (
            <>
              <Card className="stat-card loading">
                <div className="loading-spinner"></div>
                <span>Carregando...</span>
              </Card>
              <Card className="stat-card loading">
                <div className="loading-spinner"></div>
                <span>Carregando...</span>
              </Card>
              <Card className="stat-card loading">
                <div className="loading-spinner"></div>
                <span>Carregando...</span>
              </Card>
              <Card className="stat-card loading">
                <div className="loading-spinner"></div>
                <span>Carregando...</span>
              </Card>
            </>
          ) : (
            <>
              <Card className="stat-card">
                <div className="stat-icon">🎯</div>
                <div className="stat-content">
                  <span className="stat-value">{summary.active_goals}</span>
                  <span className="stat-label">Metas Ativas</span>
                </div>
              </Card>
              
              <Card className="stat-card">
                <div className="stat-icon">✅</div>
                <div className="stat-content">
                  <span className="stat-value">{summary.completed_goals}</span>
                  <span className="stat-label">Concluídas</span>
                </div>
              </Card>
              
              <Card className="stat-card">
                <div className="stat-icon">💰</div>
                <div className="stat-content">
                  <span className="stat-value">{formatCurrency(summary.total_current_amount)}</span>
                  <span className="stat-label">Total Economizado</span>
                </div>
              </Card>
              
              <Card className="stat-card">
                <div className="stat-icon">📊</div>
                <div className="stat-content">
                  <span className="stat-value">{summary.average_progress.toFixed(0)}%</span>
                  <span className="stat-label">Progresso Geral</span>
                </div>
              </Card>
            </>
          )}
        </div>
        
        <Button 
          variant="accent" 
          icon="+" 
          onClick={() => setShowForm(true)}
        >
          Nova Meta
        </Button>
      </div>
      
      <div className="goals-content">
        <div className="goals-grid">
          {loading ? (
            <div className="goals-loading">
              <div className="loading-spinner"></div>
              <span>Carregando metas...</span>
            </div>
          ) : goals.length === 0 ? (
            <div className="no-goals">
              <div className="no-goals-icon">🎯</div>
              <h3>Nenhuma meta encontrada</h3>
              <p>Crie sua primeira meta financeira para começar a economizar com propósito</p>
              <Button 
                variant="accent" 
                onClick={() => setShowForm(true)}
              >
                Criar Primeira Meta
              </Button>
            </div>
          ) : (
            goals.map((goal) => (
              <GoalCard key={goal.id} goal={goal} onGoalUpdated={handleGoalAdded} />
            ))
          )}
        </div>
        
        {!loading && goals.length > 0 && (
          <div className="goals-sidebar">
            <Card className="progress-summary">
              <h3 className="summary-title">Resumo do Progresso</h3>
              
              <div className="overall-progress">
                <div className="progress-header">
                  <span className="progress-label">Progresso Geral</span>
                  <span className="progress-percentage">
                    {summary.average_progress.toFixed(1)}%
                  </span>
                </div>
                <div className="progress-bar">
                  <div 
                    className="progress-fill"
                    style={{ width: `${summary.average_progress}%` }}
                  ></div>
                </div>
                <div className="progress-amounts">
                  <span>{formatCurrency(summary.total_current_amount)}</span>
                  <span>{formatCurrency(summary.total_target_amount)}</span>
                </div>
              </div>
              
              <div className="monthly-target">
                <h4 className="target-title">Meta Mensal Sugerida</h4>
                <div className="target-amount">{formatCurrency(calculateMonthlyTarget())}</div>
                <p className="target-description">
                  Para atingir todas as suas metas nos prazos estabelecidos
                </p>
              </div>
            </Card>
            
            <Card className="tips-card">
              <h3 className="tips-title">💡 Dicas para suas Metas</h3>
              <ul className="tips-list">
                <li>Automatize transferências mensais para suas metas</li>
                <li>Revise seus objetivos a cada 3 meses</li>
                <li>Comemore pequenas conquistas no caminho</li>
                <li>Ajuste prazos se necessário - flexibilidade é importante</li>
              </ul>
            </Card>
          </div>
        )}
      </div>
      
      {showForm && (
        <GoalForm 
          onClose={() => setShowForm(false)} 
          onGoalAdded={handleGoalAdded}
        />
      )}
    </div>
  );
};

export default Goals;
