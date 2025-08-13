import React from 'react';
import BalanceCard from '../../components/Dashboard/BalanceCard/BalanceCard';
import QuickActions from '../../components/Dashboard/QuickActions/QuickActions';
import RecentTransactions from '../../components/Dashboard/RecentTransactions/RecentTransactions';
import MonthlyChart from '../../components/Dashboard/MonthlyChart/MonthlyChart';
import './Dashboard.css';

const Dashboard = () => {
  return (
    <div className="dashboard">
      <div className="dashboard-grid">
        <div className="dashboard-balance">
          <BalanceCard />
        </div>
        
        <div className="dashboard-actions">
          <QuickActions />
        </div>
        
        <div className="dashboard-chart">
          <MonthlyChart />
        </div>
        
        <div className="dashboard-transactions">
          <RecentTransactions />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
