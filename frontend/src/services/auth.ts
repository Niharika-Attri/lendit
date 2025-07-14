import api from './api';
import type { LoginResponse, JWTPayload } from '../types/auth';
import type { RegisterRequest, UserResponse } from '../types/user';

export const login = async (email: string, password: string): Promise<LoginResponse> => {
    const response = await api.post<LoginResponse>('/v1/auth/login', new URLSearchParams({ username: email, password }));
    localStorage.setItem('token', response.data.access_token);
    return response.data;
};

export const register = async (userData: RegisterRequest): Promise<UserResponse> => {
    const response = await api.post<UserResponse>('/v1/users', userData);
    return response.data;
};

export const logout = (): void => {
    localStorage.removeItem('token');
};

export const getCurrentUser = (): JWTPayload | null => {
    const token = localStorage.getItem('token');
    if (!token) return null;
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        return payload as JWTPayload;
    } catch (error) {
        return null;
    }
};