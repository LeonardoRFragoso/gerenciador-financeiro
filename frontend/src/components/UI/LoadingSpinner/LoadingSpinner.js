import React from 'react';
import './LoadingSpinner.css';

const LoadingSpinner = ({ size = 'medium', color = 'accent' }) => {
  return (
    <div className={`loading-spinner ${size} ${color}`}>
      <div className="spinner"></div>
    </div>
  );
};

export default LoadingSpinner;
