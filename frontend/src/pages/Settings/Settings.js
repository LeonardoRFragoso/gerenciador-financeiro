import React, { useState } from 'react';
import Card from '../../components/UI/Card/Card';
import Button from '../../components/UI/Button/Button';
import { useTheme } from '../../contexts/ThemeContext';
import './Settings.css';

const Settings = () => {
  const { isDarkMode, toggleTheme } = useTheme();
  
  const [settings, setSettings] = useState({
    profile: {
      name: 'Leonardo Fragoso',
      email: 'leonardo.fragoso@email.com',
      currency: 'BRL',
      language: 'pt-BR'
    },
    notifications: {
      emailNotifications: true,
      pushNotifications: true,
      budgetAlerts: true,
      goalReminders: true,
      monthlyReports: true
    },
    privacy: {
      dataSharing: false,
      analytics: true,
      marketing: false
    },
    preferences: {
      theme: isDarkMode ? 'dark' : 'light',
      dateFormat: 'dd/mm/yyyy',
      numberFormat: 'pt-BR',
      startOfWeek: 'monday'
    }
  });

  const handleInputChange = (section, field, value) => {
    setSettings(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value
      }
    }));
  };

  const handleSave = () => {
    // Here you would typically send the data to your backend
    console.log('Settings saved:', settings);
    // Show success message
  };

  return (
    <div className="settings-page">
      <div className="settings-header">
        <div className="header-content">
          <h2 className="settings-subtitle">Configurações da Conta</h2>
          <p className="settings-description">
            Personalize sua experiência e gerencie suas preferências
          </p>
        </div>
        
        <Button variant="accent" onClick={handleSave}>
          Salvar Alterações
        </Button>
      </div>
      
      <div className="settings-content">
        {/* Profile Settings */}
        <Card className="settings-section">
          <div className="section-header">
            <h3 className="section-title">👤 Perfil</h3>
            <p className="section-description">Informações básicas da sua conta</p>
          </div>
          
          <div className="settings-grid">
            <div className="setting-item">
              <label className="setting-label">Nome Completo</label>
              <input
                type="text"
                value={settings.profile.name}
                onChange={(e) => handleInputChange('profile', 'name', e.target.value)}
                className="setting-input"
              />
            </div>
            
            <div className="setting-item">
              <label className="setting-label">Email</label>
              <input
                type="email"
                value={settings.profile.email}
                onChange={(e) => handleInputChange('profile', 'email', e.target.value)}
                className="setting-input"
              />
            </div>
            
            <div className="setting-item">
              <label className="setting-label">Moeda</label>
              <select
                value={settings.profile.currency}
                onChange={(e) => handleInputChange('profile', 'currency', e.target.value)}
                className="setting-select"
              >
                <option value="BRL">Real Brasileiro (R$)</option>
                <option value="USD">Dólar Americano ($)</option>
                <option value="EUR">Euro (€)</option>
              </select>
            </div>
            
            <div className="setting-item">
              <label className="setting-label">Idioma</label>
              <select
                value={settings.profile.language}
                onChange={(e) => handleInputChange('profile', 'language', e.target.value)}
                className="setting-select"
              >
                <option value="pt-BR">Português (Brasil)</option>
                <option value="en-US">English (US)</option>
                <option value="es-ES">Español</option>
              </select>
            </div>
          </div>
        </Card>

        {/* Notification Settings */}
        <Card className="settings-section">
          <div className="section-header">
            <h3 className="section-title">🔔 Notificações</h3>
            <p className="section-description">Configure como você quer ser notificado</p>
          </div>
          
          <div className="settings-list">
            <div className="setting-toggle">
              <div className="toggle-info">
                <span className="toggle-title">Notificações por Email</span>
                <span className="toggle-description">Receba atualizações importantes por email</span>
              </div>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={settings.notifications.emailNotifications}
                  onChange={(e) => handleInputChange('notifications', 'emailNotifications', e.target.checked)}
                />
                <span className="toggle-slider"></span>
              </label>
            </div>
            
            <div className="setting-toggle">
              <div className="toggle-info">
                <span className="toggle-title">Notificações Push</span>
                <span className="toggle-description">Receba notificações no navegador</span>
              </div>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={settings.notifications.pushNotifications}
                  onChange={(e) => handleInputChange('notifications', 'pushNotifications', e.target.checked)}
                />
                <span className="toggle-slider"></span>
              </label>
            </div>
            
            <div className="setting-toggle">
              <div className="toggle-info">
                <span className="toggle-title">Alertas de Orçamento</span>
                <span className="toggle-description">Seja avisado quando ultrapassar limites</span>
              </div>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={settings.notifications.budgetAlerts}
                  onChange={(e) => handleInputChange('notifications', 'budgetAlerts', e.target.checked)}
                />
                <span className="toggle-slider"></span>
              </label>
            </div>
            
            <div className="setting-toggle">
              <div className="toggle-info">
                <span className="toggle-title">Lembretes de Metas</span>
                <span className="toggle-description">Receba lembretes sobre suas metas financeiras</span>
              </div>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={settings.notifications.goalReminders}
                  onChange={(e) => handleInputChange('notifications', 'goalReminders', e.target.checked)}
                />
                <span className="toggle-slider"></span>
              </label>
            </div>
            
            <div className="setting-toggle">
              <div className="toggle-info">
                <span className="toggle-title">Relatórios Mensais</span>
                <span className="toggle-description">Receba um resumo mensal das suas finanças</span>
              </div>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={settings.notifications.monthlyReports}
                  onChange={(e) => handleInputChange('notifications', 'monthlyReports', e.target.checked)}
                />
                <span className="toggle-slider"></span>
              </label>
            </div>
          </div>
        </Card>

        {/* Privacy Settings */}
        <Card className="settings-section">
          <div className="section-header">
            <h3 className="section-title">🔒 Privacidade</h3>
            <p className="section-description">Controle como seus dados são utilizados</p>
          </div>
          
          <div className="settings-list">
            <div className="setting-toggle">
              <div className="toggle-info">
                <span className="toggle-title">Compartilhamento de Dados</span>
                <span className="toggle-description">Permitir compartilhamento de dados anônimos</span>
              </div>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={settings.privacy.dataSharing}
                  onChange={(e) => handleInputChange('privacy', 'dataSharing', e.target.checked)}
                />
                <span className="toggle-slider"></span>
              </label>
            </div>
            
            <div className="setting-toggle">
              <div className="toggle-info">
                <span className="toggle-title">Analytics</span>
                <span className="toggle-description">Ajude-nos a melhorar o produto com dados de uso</span>
              </div>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={settings.privacy.analytics}
                  onChange={(e) => handleInputChange('privacy', 'analytics', e.target.checked)}
                />
                <span className="toggle-slider"></span>
              </label>
            </div>
            
            <div className="setting-toggle">
              <div className="toggle-info">
                <span className="toggle-title">Marketing</span>
                <span className="toggle-description">Receber comunicações promocionais</span>
              </div>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={settings.privacy.marketing}
                  onChange={(e) => handleInputChange('privacy', 'marketing', e.target.checked)}
                />
                <span className="toggle-slider"></span>
              </label>
            </div>
          </div>
        </Card>

        {/* Preferences */}
        <Card className="settings-section">
          <div className="section-header">
            <h3 className="section-title">⚙️ Preferências</h3>
            <p className="section-description">Personalize a interface e formatação</p>
          </div>
          
          <div className="settings-grid">
            <div className="setting-item">
              <label className="setting-label">Tema</label>
              <select
                value={isDarkMode ? 'dark' : 'light'}
                onChange={(e) => {
                  const newTheme = e.target.value;
                  if ((newTheme === 'dark' && !isDarkMode) || (newTheme === 'light' && isDarkMode)) {
                    toggleTheme();
                  }
                  handleInputChange('preferences', 'theme', newTheme);
                }}
                className="setting-select"
              >
                <option value="light">Claro</option>
                <option value="dark">Escuro</option>
              </select>
            </div>
            
            <div className="setting-item">
              <label className="setting-label">Formato de Data</label>
              <select
                value={settings.preferences.dateFormat}
                onChange={(e) => handleInputChange('preferences', 'dateFormat', e.target.value)}
                className="setting-select"
              >
                <option value="dd/mm/yyyy">DD/MM/AAAA</option>
                <option value="mm/dd/yyyy">MM/DD/AAAA</option>
                <option value="yyyy-mm-dd">AAAA-MM-DD</option>
              </select>
            </div>
            
            <div className="setting-item">
              <label className="setting-label">Início da Semana</label>
              <select
                value={settings.preferences.startOfWeek}
                onChange={(e) => handleInputChange('preferences', 'startOfWeek', e.target.value)}
                className="setting-select"
              >
                <option value="sunday">Domingo</option>
                <option value="monday">Segunda-feira</option>
              </select>
            </div>
          </div>
        </Card>

        {/* Danger Zone */}
        <Card className="settings-section danger-zone">
          <div className="section-header">
            <h3 className="section-title">⚠️ Zona de Perigo</h3>
            <p className="section-description">Ações irreversíveis - use com cuidado</p>
          </div>
          
          <div className="danger-actions">
            <Button variant="outline" className="danger-btn">
              Exportar Dados
            </Button>
            <Button variant="outline" className="danger-btn">
              Limpar Histórico
            </Button>
            <Button variant="outline" className="danger-btn delete">
              Excluir Conta
            </Button>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default Settings;
