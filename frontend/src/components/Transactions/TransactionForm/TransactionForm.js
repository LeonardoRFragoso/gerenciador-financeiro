import React, { useState, useEffect } from 'react';
import Card from '../../UI/Card/Card';
import Button from '../../UI/Button/Button';
import { useToast } from '../../../contexts/ToastContext';
import apiService from '../../../services/api';
import './TransactionForm.css';

const TransactionForm = ({ onClose, type = 'expense', fixedType = false, onTransactionAdded }) => {
  const { showSuccess, showError } = useToast();
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [categories, setCategories] = useState({ income: [], expense: [] });
  const [formData, setFormData] = useState({
    type: type,
    description: '',
    amount: '',
    category: '',
    payment_method: 'debit_card',
    date: new Date().toISOString().split('T')[0],
    notes: ''
  });

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const data = await apiService.getCategoriesByType();
        setCategories({
          income: data.income || [],
          expense: data.expense || []
        });
      } catch (error) {
        console.error('Erro ao carregar categorias:', error);
        // Fallback para categorias padrão se API falhar
        setCategories({
          income: [
            { id: 'salary', name: 'Salário' },
            { id: 'freelance', name: 'Freelance' },
            { id: 'investments', name: 'Investimentos' },
            { id: 'others', name: 'Outros' }
          ],
          expense: [
            { id: 'food', name: 'Alimentação' },
            { id: 'transport', name: 'Transporte' },
            { id: 'housing', name: 'Moradia' },
            { id: 'health', name: 'Saúde' },
            { id: 'entertainment', name: 'Entretenimento' },
            { id: 'education', name: 'Educação' },
            { id: 'others', name: 'Outros' }
          ]
        });
      }
    };

    fetchCategories();
  }, []);

  const validateForm = () => {
    const newErrors = {};

    if (!formData.description.trim()) {
      newErrors.description = 'Descrição é obrigatória';
    }

    if (!formData.amount || parseFloat(formData.amount) <= 0) {
      newErrors.amount = 'Valor deve ser maior que zero';
    }

    if (!formData.category) {
      newErrors.category = 'Categoria é obrigatória';
    }

    if (!formData.date) {
      newErrors.date = 'Data é obrigatória';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      showError('Por favor, corrija os erros no formulário');
      return;
    }

    setIsLoading(true);
    
    try {
      const transactionData = {
        description: formData.description.trim(),
        amount: parseFloat(formData.amount),
        type: formData.type,
        category: formData.category,
        payment_method: formData.payment_method,
        date: formData.date,
        notes: formData.notes.trim()
      };

      const response = await apiService.createTransaction(transactionData);
      
      const transactionType = formData.type === 'income' ? 'receita' : 'despesa';
      const formattedAmount = new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
      }).format(parseFloat(formData.amount));
      
      showSuccess(`${transactionType} de ${formattedAmount} adicionada com sucesso!`);
      
      // Notificar componente pai para atualizar a lista
      if (onTransactionAdded) {
        onTransactionAdded(response);
      }
      
      onClose();
    } catch (error) {
      console.error('Erro ao salvar transação:', error);
      showError(error.message || 'Erro ao salvar transação. Tente novamente.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  return (
    <div className="transaction-form-overlay">
      <div className="transaction-form-container">
        <Card className="transaction-form">
          <div className="form-header">
            <h3 className="form-title">
              {fixedType 
                ? (formData.type === 'income' ? 'Nova Receita' : 'Nova Despesa')
                : 'Nova Transação'
              }
            </h3>
            <button className="form-close" onClick={onClose}>×</button>
          </div>
          
          <form onSubmit={handleSubmit}>
            {!fixedType && (
              <div className="form-group">
                <label className="form-label">Tipo</label>
                <div className="type-selector">
                  <button
                    type="button"
                    className={`type-btn ${formData.type === 'income' ? 'active' : ''}`}
                    onClick={() => setFormData(prev => ({ ...prev, type: 'income', category: '' }))}
                  >
                    📈 Receita
                  </button>
                  <button
                    type="button"
                    className={`type-btn ${formData.type === 'expense' ? 'active' : ''}`}
                    onClick={() => setFormData(prev => ({ ...prev, type: 'expense', category: '' }))}
                  >
                    📉 Despesa
                  </button>
                </div>
              </div>
            )}
            
            <div className="form-group">
              <label className="form-label">Descrição</label>
              <input
                type="text"
                name="description"
                value={formData.description}
                onChange={handleChange}
                className={`form-input ${errors.description ? 'error' : ''}`}
                placeholder="Ex: Supermercado, Salário..."
                required
              />
              {errors.description && <span className="form-error">{errors.description}</span>}
            </div>
            
            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Valor</label>
                <input
                  type="number"
                  name="amount"
                  value={formData.amount}
                  onChange={handleChange}
                  className={`form-input ${errors.amount ? 'error' : ''}`}
                  placeholder="0,00"
                  step="0.01"
                  min="0"
                  required
                />
                {errors.amount && <span className="form-error">{errors.amount}</span>}
              </div>
              
              <div className="form-group">
                <label className="form-label">Data</label>
                <input
                  type="date"
                  name="date"
                  value={formData.date}
                  onChange={handleChange}
                  className={`form-input ${errors.date ? 'error' : ''}`}
                  required
                />
                {errors.date && <span className="form-error">{errors.date}</span>}
              </div>
            </div>
            
            <div className="form-group">
              <label className="form-label">Categoria</label>
              <select
                name="category"
                value={formData.category}
                onChange={handleChange}
                className={`form-input ${errors.category ? 'error' : ''}`}
                required
              >
                <option value="">Selecione uma categoria</option>
                {categories[formData.type].map(category => (
                  <option key={category.id || category.name} value={category.id || category.name}>
                    {category.name}
                  </option>
                ))}
              </select>
              {errors.category && <span className="form-error">{errors.category}</span>}
            </div>

            <div className="form-group">
              <label className="form-label">Método de Pagamento</label>
              <select
                name="payment_method"
                value={formData.payment_method}
                onChange={handleChange}
                className="form-input"
              >
                <option value="cash">Dinheiro</option>
                <option value="debit_card">Cartão de Débito</option>
                <option value="credit_card">Cartão de Crédito</option>
                <option value="bank_transfer">Transferência Bancária</option>
                <option value="pix">PIX</option>
                <option value="check">Cheque</option>
                <option value="other">Outros</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Observações (opcional)</label>
              <textarea
                name="notes"
                value={formData.notes}
                onChange={handleChange}
                className="form-input"
                placeholder="Adicione observações sobre esta transação..."
                rows="3"
              />
            </div>
            
            <div className="form-actions">
              <Button type="button" variant="outline" onClick={onClose}>
                Cancelar
              </Button>
              <Button type="submit" variant="accent" disabled={isLoading}>
                {isLoading ? 'Salvando...' : 'Salvar Transação'}
              </Button>
            </div>
          </form>
        </Card>
      </div>
    </div>
  );
};

export default TransactionForm;
