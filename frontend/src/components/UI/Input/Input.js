import React from 'react';
import './Input.css';

const Input = ({ 
  type = 'text', 
  name, 
  placeholder, 
  value, 
  onChange, 
  error, 
  disabled = false,
  autoComplete,
  className = '',
  ...props 
}) => {
  return (
    <div className={`input-wrapper ${className}`}>
      <input
        type={type}
        name={name}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        disabled={disabled}
        autoComplete={autoComplete}
        className={`input ${error ? 'input-error' : ''} ${disabled ? 'input-disabled' : ''}`}
        {...props}
      />
      {error && <span className="input-error-message">{error}</span>}
    </div>
  );
};

export default Input;
