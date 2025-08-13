import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Card from '../../UI/Card/Card';
import Button from '../../UI/Button/Button';
import Input from '../../UI/Input/Input';
import Logo from '../../Logo/Logo';
import apiService from '../../../services/api';
import { useToast } from '../../../contexts/ToastContext';
import './ForgotPassword.css';

const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);
  const [error, setError] = useState('');
  const { showSuccess, showError } = useToast();

  const handleChange = (e) => {
    setEmail(e.target.value);
    if (error) {
      setError('');
    }
  };

  const validateEmail = () => {
    if (!email.trim()) {
      setError('Email é obrigatório');
      return false;
    }
    if (!/\S+@\S+\.\S+/.test(email)) {
      setError('Email inválido');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateEmail()) {
      return;
    }

    setLoading(true);
    try {
      await apiService.forgotPassword(email);
      setSent(true);
      showSuccess('Email de recuperação enviado com sucesso!');
    } catch (error) {
      console.error('Erro ao enviar email de recuperação:', error);
      if (error.message.includes('não encontrado')) {
        showError('Email não encontrado em nossa base de dados');
      } else {
        showError('Erro ao enviar email de recuperação. Tente novamente.');
      }
    } finally {
      setLoading(false);
    }
  };

  if (sent) {
    return (
      <div className="forgot-password-page">
        <div className="forgot-password-container">
          <Card className="forgot-password-card">
            <div className="forgot-password-header">
              <Logo size="large" />
              <div className="success-icon">📧</div>
              <h1 className="forgot-password-title">Email Enviado!</h1>
              <p className="forgot-password-subtitle">
                Enviamos um link de recuperação para <strong>{email}</strong>
              </p>
            </div>

            <div className="forgot-password-content">
              <p className="instructions">
                Verifique sua caixa de entrada e siga as instruções no email para redefinir sua senha.
              </p>
              <p className="note">
                Não recebeu o email? Verifique sua pasta de spam ou tente novamente em alguns minutos.
              </p>
            </div>

            <div className="forgot-password-actions">
              <Button
                variant="outline"
                onClick={() => {
                  setSent(false);
                  setEmail('');
                }}
              >
                Enviar Novamente
              </Button>
              <Link to="/login">
                <Button variant="accent">
                  Voltar ao Login
                </Button>
              </Link>
            </div>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="forgot-password-page">
      <div className="forgot-password-container">
        <Card className="forgot-password-card">
          <div className="forgot-password-header">
            <Logo size="large" />
            <h1 className="forgot-password-title">Esqueceu sua senha?</h1>
            <p className="forgot-password-subtitle">
              Digite seu email e enviaremos um link para redefinir sua senha
            </p>
          </div>

          <form onSubmit={handleSubmit} className="forgot-password-form">
            <div className="form-group">
              <Input
                type="email"
                name="email"
                placeholder="Seu email"
                value={email}
                onChange={handleChange}
                error={error}
                disabled={loading}
                autoComplete="email"
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
              {loading ? 'Enviando...' : 'Enviar Link de Recuperação'}
            </Button>
          </form>

          <div className="forgot-password-footer">
            <p>
              Lembrou sua senha?{' '}
              <Link to="/login" className="login-link">
                Voltar ao login
              </Link>
            </p>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default ForgotPassword;
