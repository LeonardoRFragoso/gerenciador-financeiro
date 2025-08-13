import React from 'react';
import './Card.css';

const Card = ({ children, className = '', hover = true, ...props }) => {
  return (
    <div 
      className={`ui-card ${hover ? 'ui-card-hover' : ''} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

export default Card;
