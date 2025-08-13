import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import Logo from '../Logo/Logo';
import './MobileMenu.css';

const MobileMenu = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const menuItems = [
    { path: '/', label: 'Dashboard', icon: '📊' },
    { path: '/transactions', label: 'Transações', icon: '💳' },
    { path: '/reports', label: 'Relatórios', icon: '📈' },
    { path: '/goals', label: 'Metas', icon: '🎯' },
    { path: '/settings', label: 'Configurações', icon: '⚙️' }
  ];

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const closeMenu = () => {
    setIsOpen(false);
  };

  return (
    <>
      <button 
        className="mobile-menu-trigger"
        onClick={toggleMenu}
        aria-label="Abrir menu"
      >
        <span className={`hamburger ${isOpen ? 'open' : ''}`}>
          <span></span>
          <span></span>
          <span></span>
        </span>
      </button>

      <div className={`mobile-menu-overlay ${isOpen ? 'open' : ''}`} onClick={closeMenu}></div>
      
      <aside className={`mobile-menu ${isOpen ? 'open' : ''}`}>
        <div className="mobile-menu-header">
          <Logo />
          <button 
            className="mobile-menu-close"
            onClick={closeMenu}
            aria-label="Fechar menu"
          >
            ×
          </button>
        </div>
        
        <nav className="mobile-menu-nav">
          {menuItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`mobile-menu-link ${location.pathname === item.path ? 'active' : ''}`}
              onClick={closeMenu}
            >
              <span className="mobile-menu-icon">{item.icon}</span>
              <span className="mobile-menu-label">{item.label}</span>
            </Link>
          ))}
        </nav>
        
        <div className="mobile-menu-footer">
          <div className="mobile-user">
            <div className="mobile-user-avatar">U</div>
            <div className="mobile-user-info">
              <div className="mobile-user-name">Usuário</div>
              <div className="mobile-user-email">user@email.com</div>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
};

export default MobileMenu;
