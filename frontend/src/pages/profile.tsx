import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCurrentUser } from '../services/auth';
import api from '../services/api';
import Header from '../components/header';
import UploadWidget from '../components/uploadIdWidget';
import type { UserResponse, User } from '../types/user';
import type { JWTPayload } from '../types/auth';

const Profile: React.FC = () => {
    const [user, setUser] = useState<User | null>(null);
    const [message, setMessage] = useState<string>('');
    const navigate = useNavigate();

    useEffect(() => {
        const currentUser: JWTPayload | null = getCurrentUser();
        if (!currentUser) {
            navigate('/login');
            return;
        }

        api.get<UserResponse>(`/v1/users/${currentUser.id}`)
            .then(response => setUser(response.data))
            .catch(error => setMessage(error.response?.data?.detail || 'Failed to fetch user'));
    }, [navigate]);

    if (!user) return <div>Loading...</div>;

    return (
        <div>
            <Header />
            <h2>Profile</h2>
            <p>Name: {user.first_name} {user.last_name}</p>
            <p>Email: {user.email}</p>
            <p>Phone: {user.phone_number || 'Not set'}</p>
            {user.college_id_url && <img src={user.college_id_url} alt="College ID" style={{ maxWidth: '200px' }} />}
            <UploadWidget userId={user.id} token={localStorage.getItem('token') || ''} />
            {message && <p>{message}</p>}
        </div>
        );
};

export default Profile;