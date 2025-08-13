import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Card from '../../UI/Card/Card';
import Button from '../../UI/Button/Button';
import Input from '../../UI/Input/Input';
import Logo from '../../Logo/Logo';
import apiService from '../../../services/api';
import { useToast } from '../../../contexts/ToastContext';
import './Register.css';

const Register = () => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const navigate = useNavigate();
  const { showSuccess, showError } = useToast();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Limpar erro do campo quando usuário começar a digitar
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.first_name.trim()) {
      newErrors.first_name = 'Nome é obrigatório';
    }

    if (!formData.last_name.trim()) {
      newErrors.last_name = 'Sobrenome é obrigatório';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email é obrigatório';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email inválido';
    }

    if (!formData.password.trim()) {
      newErrors.password = 'Senha é obrigatória';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Senha deve ter pelo menos 8 caracteres';
    } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(formData.password)) {
      newErrors.password = 'Senha deve conter ao menos: 1 letra minúscula, 1 maiúscula e 1 número';
    }

    if (!formData.confirmPassword.trim()) {
      newErrors.confirmPassword = 'Confirmação de senha é obrigatória';
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Senhas não coincidem';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setLoading(true);
    try {
      const userData = {
        first_name: formData.first_name,
        last_name: formData.last_name,
        email: formData.email,
        password: formData.password
      };

      await apiService.register(userData);
      
      showSuccess('Conta criada com sucesso! Faça login para continuar.');
      navigate('/login');
    } catch (error) {
      console.error('Erro no registro:', error);
      if (error.message.includes('email')) {
        showError('Este email já está em uso');
      } else {
        showError('Erro ao criar conta. Tente novamente.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-page">
      <div className="register-container">
        <Card className="register-card">
          <div className="register-header">
            <Logo size="large" />
            <h1 className="register-title">Criar Conta</h1>
            <p className="register-subtitle">Comece a gerenciar suas finanças hoje</p>
          </div>

          <form onSubmit={handleSubmit} className="register-form">
            <div className="form-row">
              <div className="form-group">
                <Input
                  type="text"
                  name="first_name"
                  placeholder="Nome"
                  value={formData.first_name}
                  onChange={handleChange}
                  error={errors.first_name}
                  disabled={loading}
                  autoComplete="given-name"
                />
              </div>
              <div className="form-group">
                <Input
                  type="text"
                  name="last_name"
                  placeholder="Sobrenome"
                  value={formData.last_name}
                  onChange={handleChange}
                  error={errors.last_name}
                  disabled={loading}
                  autoComplete="family-name"
                />
              </div>
            </div>

            <div className="form-group">
              <Input
                type="email"
                name="email"
                placeholder="Seu email"
                value={formData.email}
                onChange={handleChange}
                error={errors.email}
                disabled={loading}
                autoComplete="email"
              />
            </div>

            <div className="form-group">
              <Input
                type="password"
                name="password"
                placeholder="Criar senha"
                value={formData.password}
                onChange={handleChange}
                error={errors.password}
                disabled={loading}
                autoComplete="new-password"
              />
            </div>

            <div className="form-group">
              <Input
                type="password"
                name="confirmPassword"
                placeholder="Confirmar senha"
                value={formData.confirmPassword}
                onChange={handleChange}
                error={errors.confirmPassword}
                disabled={loading}
                autoComplete="new-password"
              />
            </div>

            <Button
              type="submit"
              variant="accent"
              size="large"
              fullWidth
              loading={loading}
              disabled={loading}
            >
              {loading ? 'Criando conta...' : 'Criar Conta'}
            </Button>
          </form>

          <div className="register-footer">
            <p>
              Já tem uma conta?{' '}
              <Link to="/login" className="login-link">
                Fazer login
              </Link>
            </p>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default Register;
