import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { getCurrentUser, logout } from '../services/auth';
import { type JWTPayload } from '../types/auth';

const Header: React.FC = () => {
    const user: JWTPayload | null = getCurrentUser();
    const navigate = useNavigate();

    const handleLogout = (): void => {
        logout();
        navigate('/login');
    };

    return (
        <nav className='flex w-screen justify-end py-3 px-5 gap-2 bg-gradient-to-b from-sky-600 to-transparent'>
        <Link className='px-3' to="/">Home</Link>
        {user ? (
            <>
            <Link className='px-3' to="/profile">Profile</Link>
            <Link className='px-3' to="/dashboard">Dashboard</Link>
            <button onClick={handleLogout}>Logout</button>
            </>
        ) : (
            <>
            <Link className='px-3' to="/register">Register</Link>
            <Link className='px-3' to="/login">Login</Link>
            </>
        )}
        </nav>
    );
};

export default Header;