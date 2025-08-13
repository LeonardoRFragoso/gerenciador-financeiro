import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import Logo from '../Logo/Logo';
import './Sidebar.css';

const Sidebar = () => {
  const location = useLocation();

  const menuItems = [
    { path: '/', label: 'Dashboard', icon: '📊' },
    { path: '/transactions', label: 'Transações', icon: '💳' },
    { path: '/reports', label: 'Relatórios', icon: '📈' },
    { path: '/goals', label: 'Metas', icon: '🎯' },
    { path: '/settings', label: 'Configurações', icon: '⚙️' }
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <Logo />
      </div>
      
      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`sidebar-link ${location.pathname === item.path ? 'active' : ''}`}
          >
            <span className="sidebar-icon">{item.icon}</span>
            <span className="sidebar-label">{item.label}</span>
          </Link>
        ))}
      </nav>
      
      <div className="sidebar-footer">
        <div className="sidebar-user">
          <div className="user-avatar">U</div>
          <div className="user-info">
            <div className="user-name">Usuário</div>
            <div className="user-email">user@email.com</div>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
