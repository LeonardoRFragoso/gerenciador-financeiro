import React, { useState } from 'react';
import Card from '../../UI/Card/Card';
import Button from '../../UI/Button/Button';
import './GoalForm.css';

const GoalForm = ({ onClose }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    targetAmount: '',
    currentAmount: '0',
    deadline: '',
    category: 'emergency',
    priority: 'medium'
  });

  const categories = [
    { value: 'emergency', label: '🚨 Emergência', icon: '🚨' },
    { value: 'travel', label: '✈️ Viagem', icon: '✈️' },
    { value: 'technology', label: '💻 Tecnologia', icon: '💻' },
    { value: 'education', label: '📚 Educação', icon: '📚' },
    { value: 'home', label: '🏠 Casa', icon: '🏠' },
    { value: 'car', label: '🚗 Veículo', icon: '🚗' },
    { value: 'health', label: '🏥 Saúde', icon: '🏥' },
    { value: 'investment', label: '📈 Investimento', icon: '📈' }
  ];

  const priorities = [
    { value: 'high', label: 'Alta', color: '#ff6b6b' },
    { value: 'medium', label: 'Média', color: '#feca57' },
    { value: 'low', label: 'Baixa', color: 'var(--color-success)' }
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    // Here you would typically send the data to your backend
    console.log('Goal data:', formData);
    onClose();
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div className="goal-form-overlay">
      <div className="goal-form-container">
        <Card className="goal-form">
          <div className="form-header">
            <h3 className="form-title">Nova Meta Financeira</h3>
            <button className="form-close" onClick={onClose}>×</button>
          </div>
          
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label">Título da Meta</label>
              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleChange}
                className="form-input"
                placeholder="Ex: Reserva de emergência, Viagem..."
                required
              />
            </div>
            
            <div className="form-group">
              <label className="form-label">Descrição</label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleChange}
                className="form-textarea"
                placeholder="Descreva sua meta em detalhes..."
                rows="3"
                required
              />
            </div>
            
            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Valor Alvo</label>
                <input
                  type="number"
                  name="targetAmount"
                  value={formData.targetAmount}
                  onChange={handleChange}
                  className="form-input"
                  placeholder="0,00"
                  step="0.01"
                  min="0"
                  required
                />
              </div>
              
              <div className="form-group">
                <label className="form-label">Valor Atual</label>
                <input
                  type="number"
                  name="currentAmount"
                  value={formData.currentAmount}
                  onChange={handleChange}
                  className="form-input"
                  placeholder="0,00"
                  step="0.01"
                  min="0"
                />
              </div>
            </div>
            
            <div className="form-group">
              <label className="form-label">Prazo</label>
              <input
                type="date"
                name="deadline"
                value={formData.deadline}
                onChange={handleChange}
                className="form-input"
                min={new Date().toISOString().split('T')[0]}
                required
              />
            </div>
            
            <div className="form-group">
              <label className="form-label">Categoria</label>
              <div className="category-grid">
                {categories.map(category => (
                  <button
                    key={category.value}
                    type="button"
                    className={`category-btn ${formData.category === category.value ? 'active' : ''}`}
                    onClick={() => setFormData(prev => ({ ...prev, category: category.value }))}
                  >
                    <span className="category-icon">{category.icon}</span>
                    <span className="category-label">{category.label.split(' ')[1]}</span>
                  </button>
                ))}
              </div>
            </div>
            
            <div className="form-group">
              <label className="form-label">Prioridade</label>
              <div className="priority-selector">
                {priorities.map(priority => (
                  <button
                    key={priority.value}
                    type="button"
                    className={`priority-btn ${formData.priority === priority.value ? 'active' : ''}`}
                    onClick={() => setFormData(prev => ({ ...prev, priority: priority.value }))}
                  >
                    <span 
                      className="priority-indicator"
                      style={{ backgroundColor: priority.color }}
                    ></span>
                    {priority.label}
                  </button>
                ))}
              </div>
            </div>
            
            <div className="form-actions">
              <Button type="button" variant="outline" onClick={onClose}>
                Cancelar
              </Button>
              <Button type="submit" variant="accent">
                Criar Meta
              </Button>
            </div>
          </form>
        </Card>
      </div>
    </div>
  );
};

export default GoalForm;
