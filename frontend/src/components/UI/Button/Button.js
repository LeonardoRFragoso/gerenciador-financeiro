import React from 'react';
import './Button.css';

const Button = ({ 
  children, 
  variant = 'primary', 
  size = 'medium', 
  icon, 
  onClick, 
  disabled = false,
  className = '',
  fullWidth = false,
  loading = false,
  type = 'button',
  ...props 
}) => {
  const buttonClasses = [
    'ui-btn',
    `ui-btn-${variant}`,
    `ui-btn-${size}`,
    fullWidth ? 'ui-btn-full-width' : '',
    loading ? 'ui-btn-loading' : '',
    className
  ].filter(Boolean).join(' ');

  return (
    <button
      type={type}
      className={buttonClasses}
      onClick={onClick}
      disabled={disabled || loading}
      {...props}
    >
      {icon && <span className="ui-btn-icon">{icon}</span>}
      {children}
    </button>
  );
};

export default Button;
