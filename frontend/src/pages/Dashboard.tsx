import React from 'react';
import { useAuth } from '../hooks/useAuth';
import MainLayout from '../components/layout/MainLayout';

const Dashboard: React.FC = () => {
  const { user } = useAuth();

  return (
    <MainLayout>
      <div className="space-y-4">
        <h1 className="text-3xl font-bold">Welcome, {user?.full_name}!</h1>
        <p className="text-gray-600">Dashboard content coming soon...</p>
      </div>
    </MainLayout>
  );
};

export default Dashboard;
