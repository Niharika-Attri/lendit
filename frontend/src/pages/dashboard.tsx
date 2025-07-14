import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCurrentUser } from '../services/auth';
import Header from '../components/header';

const Dashboard: React.FC = () => {
    const navigate = useNavigate();

    useEffect(() => {
        if (!getCurrentUser()) {
            navigate('/login');
        }
    }, [navigate]);

    return (
        <div>
            <Header />
            <h2>Dashboard</h2>
            <p>Welcome to your Lendit dashboard!</p>
        </div>
    );
};

export default Dashboard;