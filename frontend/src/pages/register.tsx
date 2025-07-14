import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import OTPForm from '../components/otpForm';
import type { RegisterRequest, UserResponse } from '../types/user';

const Register: React.FC = () => {
    const [formData, setFormData] = useState<RegisterRequest>({
        first_name: '',
        last_name: '',
        email: '',
        phone_number: '',
        password: '',
    });
    const [message, setMessage] = useState<string>('');
    const [showOTP, setShowOTP] = useState<boolean>(false);
    const navigate = useNavigate();

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>): void => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent): Promise<void> => {
        e.preventDefault();
        try {
        await api.post<UserResponse>('/v1/users', formData);
        setMessage('Registration successful, please verify phone number');
        setShowOTP(true);
        } catch (error: any) {
            setMessage(error.response?.data?.detail || 'Registration failed');
        }
    };

    const handleOTPSuccess = (): void => {
        navigate('/login');
    };

    return (
        <div className="w-screen h-screen overflow-x-hidden flex justify-center items-center bg-indigo-950">
            <div className="w-[400px] border border-white/20 rounded-2xl flex flex-col p-6 justify-center items-center bg-indigo-900/50 backdrop-blur-sm">
                <h1 className="text-2xl font-bold text-white mb-4">Welcome to Lendit</h1>
                <h2 className="text-xl font-semibold text-white mb-6">Register</h2>
                <form onSubmit={handleSubmit} className="flex flex-col w-full gap-4">
                <div className="flex flex-col">
                    <label className="text-white text-sm font-medium mb-1">First Name</label>
                    <input
                    type="text"
                    name="first_name"
                    value={formData.first_name}
                    onChange={handleInputChange}
                    required
                    className="h-10 px-4 rounded-lg bg-white/10 text-white placeholder:text-white/50 border border-white/20 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="First Name"
                    />
                </div>
                <div className="flex flex-col">
                    <label className="text-white text-sm font-medium mb-1">Last Name</label>
                    <input
                    type="text"
                    name="last_name"
                    value={formData.last_name}
                    onChange={handleInputChange}
                    required
                    className="h-10 px-4 rounded-lg bg-white/10 text-white placeholder:text-white/50 border border-white/20 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Last Name"
                    />
                </div>
                <div className="flex flex-col">
                    <label className="text-white text-sm font-medium mb-1">Email</label>
                    <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                    className="h-10 px-4 rounded-lg bg-white/10 text-white placeholder:text-white/50 border border-white/20 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Email"
                    />
                </div>
                <div className="flex flex-col">
                    <label className="text-white text-sm font-medium mb-1">Phone Number</label>
                    <input
                    type="text"
                    name="phone_number"
                    value={formData.phone_number}
                    onChange={handleInputChange}
                    className="h-10 px-4 rounded-lg bg-white/10 text-white placeholder:text-white/50 border border-white/20 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="+1234567890"
                    />
                </div>
                <div className="flex flex-col">
                    <label className="text-white text-sm font-medium mb-1">Password</label>
                    <input
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleInputChange}
                    required
                    className="h-10 px-4 rounded-lg bg-white/10 text-white placeholder:text-white/50 border border-white/20 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Password"
                    />
                </div>
                <button
                    type="submit"
                    className="mt-4 h-10 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-700 transition-colors"
                >
                    Register
                </button>
                </form>
                {showOTP && <OTPForm onSuccess={handleOTPSuccess} />}
                {message && <p className="mt-4 text-red-400 text-center">{message}</p>}
            </div>
        </div>
    );
};

export default Register;