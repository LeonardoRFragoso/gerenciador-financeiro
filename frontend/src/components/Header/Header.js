import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useTheme } from '../../contexts/ThemeContext';
import { useAuth } from '../../contexts/AuthContext';
import { useToast } from '../../contexts/ToastContext';
import MobileMenu from '../MobileMenu/MobileMenu';
import './Header.css';

const Header = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { isDarkMode, toggleTheme } = useTheme();
  const { user, logout } = useAuth();
  const { showSuccess } = useToast();
  const [showUserMenu, setShowUserMenu] = useState(false);
  
  const getPageTitle = () => {
    switch (location.pathname) {
      case '/': 
      case '/dashboard': return 'Dashboard';
      case '/transactions': return 'Transações';
      case '/reports': return 'Relatórios';
      case '/goals': return 'Metas';
      case '/settings': return 'Configurações';
      default: return 'Dashboard';
    }
  };

  const handleLogout = () => {
    logout();
    showSuccess('Logout realizado com sucesso!');
    navigate('/login');
  };

  const getUserInitials = () => {
    if (!user) return 'U';
    const firstName = user.first_name || '';
    const lastName = user.last_name || '';
    return (firstName.charAt(0) + lastName.charAt(0)).toUpperCase() || user.email.charAt(0).toUpperCase();
  };

  return (
    <header className="header">
      <div className="header-content">
        <div className="header-left">
          <MobileMenu />
          <div className="header-titles">
            <h1 className="page-title">{getPageTitle()}</h1>
            <p className="page-subtitle">Gerencie suas finanças de forma inteligente</p>
          </div>
        </div>
        
        <div className="header-right">
          <button className="header-btn">
            <span className="header-btn-icon">🔔</span>
          </button>
          <button 
            className="header-btn theme-toggle" 
            onClick={toggleTheme}
            title={isDarkMode ? 'Alternar para tema claro' : 'Alternar para tema escuro'}
          >
            <span className="header-btn-icon">
              {isDarkMode ? '☀️' : '🌙'}
            </span>
          </button>
          
          <div className="user-menu">
            <button 
              className="user-avatar"
              onClick={() => setShowUserMenu(!showUserMenu)}
              title={user ? `${user.first_name} ${user.last_name}` : 'Menu do usuário'}
            >
              <span className="avatar-initials">{getUserInitials()}</span>
            </button>
            
            {showUserMenu && (
              <div className="user-dropdown">
                <div className="user-info">
                  <div className="user-name">
                    {user ? `${user.first_name} ${user.last_name}` : 'Usuário'}
                  </div>
                  <div className="user-email">
                    {user?.email}
                  </div>
                </div>
                <div className="dropdown-divider"></div>
                <button 
                  className="dropdown-item"
                  onClick={() => {
                    setShowUserMenu(false);
                    navigate('/settings');
                  }}
                >
                  <span className="dropdown-icon">⚙️</span>
                  Configurações
                </button>
                <button 
                  className="dropdown-item logout"
                  onClick={handleLogout}
                >
                  <span className="dropdown-icon">🚪</span>
                  Sair
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
