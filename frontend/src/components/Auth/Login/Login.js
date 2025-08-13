import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Logo from '../../Logo/Logo';
import apiService from '../../../services/api';
import { useToast } from '../../../contexts/ToastContext';
import './Login.css';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [showPassword, setShowPassword] = useState(false);
  const [isFormValid, setIsFormValid] = useState(false);
  const [touchedFields, setTouchedFields] = useState({});
  
  const navigate = useNavigate();
  const { showSuccess, showError } = useToast();
  const emailInputRef = useRef(null);
  const passwordInputRef = useRef(null);

  // Focar no primeiro input ao montar o componente
  useEffect(() => {
    if (emailInputRef.current) {
      emailInputRef.current.focus();
    }
  }, []);

  // Validação em tempo real
  useEffect(() => {
    const emailValid = formData.email.trim() && /\S+@\S+\.\S+/.test(formData.email);
    const passwordValid = formData.password.trim() && formData.password.length >= 6;
    setIsFormValid(emailValid && passwordValid);
  }, [formData.email, formData.password]);

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

  const handleBlur = (e) => {
    const { name } = e.target;
    setTouchedFields(prev => ({
      ...prev,
      [name]: true
    }));
    validateField(name);
  };

  const validateField = (fieldName) => {
    const newErrors = { ...errors };

    switch (fieldName) {
      case 'email':
        if (!formData.email.trim()) {
          newErrors.email = 'Email é obrigatório';
        } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
          newErrors.email = 'Por favor, insira um email válido';
        } else {
          delete newErrors.email;
        }
        break;
      case 'password':
        if (!formData.password.trim()) {
          newErrors.password = 'Senha é obrigatória';
        } else if (formData.password.length < 6) {
          newErrors.password = 'Senha deve ter pelo menos 6 caracteres';
        } else {
          delete newErrors.password;
        }
        break;
      default:
        break;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.email.trim()) {
      newErrors.email = 'Email é obrigatório';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Por favor, insira um email válido';
    }

    if (!formData.password.trim()) {
      newErrors.password = 'Senha é obrigatória';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Senha deve ter pelo menos 6 caracteres';
    }

    setErrors(newErrors);
    setTouchedFields({ email: true, password: true });
    return Object.keys(newErrors).length === 0;
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !loading && isFormValid) {
      handleSubmit(e);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      // Focar no primeiro campo com erro
      if (errors.email && emailInputRef.current) {
        emailInputRef.current.focus();
      } else if (errors.password && passwordInputRef.current) {
        passwordInputRef.current.focus();
      }
      return;
    }

    setLoading(true);
    
    try {
      const response = await apiService.login(formData.email, formData.password);
      
      // Salvar tokens no localStorage
      localStorage.setItem('access_token', response.access);
      localStorage.setItem('refresh_token', response.refresh);
      
      // Feedback de sucesso com delay para melhor UX
      showSuccess('Login realizado com sucesso!');
      
      // Pequeno delay para mostrar o feedback antes de navegar
      setTimeout(() => {
        navigate('/dashboard', { replace: true });
      }, 1000);
      
    } catch (error) {
      console.error('Erro no login:', error);
      
      // Tratamento mais específico de erros
      if (error.status === 401 || error.message.includes('credenciais')) {
        setErrors({
          email: 'Email ou senha incorretos',
          password: 'Email ou senha incorretos'
        });
        showError('Email ou senha incorretos');
      } else if (error.status === 429) {
        showError('Muitas tentativas de login. Tente novamente em alguns minutos.');
      } else if (error.status >= 500) {
        showError('Erro interno do servidor. Tente novamente mais tarde.');
      } else {
        showError('Erro ao fazer login. Verifique sua conexão e tente novamente.');
      }
      
      // Focar no campo de email após erro
      if (emailInputRef.current) {
        emailInputRef.current.focus();
      }
    } finally {
      setLoading(false);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(prev => !prev);
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-card">
          <div className="login-header">
            <div className="logo-container">
              <Logo size="large" />
            </div>
            <h1 className="login-title">Bem-vindo de volta</h1>
            <p className="login-subtitle">Faça login para acessar sua conta</p>
          </div>

          <form onSubmit={handleSubmit} className="login-form" noValidate>
            <div className="form-group">
              <input
                ref={emailInputRef}
                type="email"
                name="email"
                placeholder="Seu email"
                value={formData.email}
                onChange={handleChange}
                onBlur={handleBlur}
                onKeyPress={handleKeyPress}
                className={`form-input ${errors.email ? 'error' : ''}`}
                disabled={loading}
                autoComplete="email"
                aria-invalid={errors.email ? 'true' : 'false'}
                aria-describedby={errors.email ? 'email-error' : undefined}
              />
              {errors.email && touchedFields.email && (
                <div id="email-error" className="error-message" role="alert">
                  {errors.email}
                </div>
              )}
            </div>

            <div className="form-group">
              <div style={{ position: 'relative' }}>
                <input
                  ref={passwordInputRef}
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  placeholder="Sua senha"
                  value={formData.password}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  onKeyPress={handleKeyPress}
                  className={`form-input ${errors.password ? 'error' : ''}`}
                  disabled={loading}
                  autoComplete="current-password"
                  aria-invalid={errors.password ? 'true' : 'false'}
                  aria-describedby={errors.password ? 'password-error' : undefined}
                  style={{ paddingRight: '3rem' }}
                />
                <button
                  type="button"
                  onClick={togglePasswordVisibility}
                  className="password-toggle"
                  aria-label={showPassword ? 'Ocultar senha' : 'Mostrar senha'}
                  tabIndex={loading ? -1 : 0}
                >
                  {showPassword ? '👁️' : '🔒'}
                </button>
              </div>
              {errors.password && touchedFields.password && (
                <div id="password-error" className="error-message" role="alert">
                  {errors.password}
                </div>
              )}
            </div>

            <button
              type="submit"
              className="login-button"
              disabled={loading || !isFormValid}
              aria-describedby="login-button-status"
            >
              {loading && <span className="loading-spinner" aria-hidden="true"></span>}
              {loading ? 'Entrando...' : 'Entrar'}
            </button>
            
            <div id="login-button-status" className="sr-only" aria-live="polite">
              {loading ? 'Processando login...' : ''}
            </div>

          </form>

          <div className="login-footer">
            <p>
              <Link 
                to="/forgot-password" 
                className="forgot-password-link"
                tabIndex={loading ? -1 : 0}
              >
                Esqueceu sua senha?
              </Link>
            </p>
            <p>
              Não tem uma conta?{' '}
              <Link 
                to="/register" 
                className="register-link"
                tabIndex={loading ? -1 : 0}
              >
                Criar conta
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;