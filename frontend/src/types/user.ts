export interface User {
    id: number;
    email: string;
    first_name: string;
    last_name: string;
    phone_number: string | null;
    college_id_url: string | null;
    role: string | null;
    created_at: string;
    updated_at: string | null;
    is_active: boolean;
    }

export interface UserResponse {
    message?: string;
    id: number;
    first_name: string;
    last_name: string;
    email: string;
    phone_number: string | null;
    is_active: boolean;
    created_at: string;
    updated_at: string | null;
    role: string | null;
    college_id_url: string | null;
    }

export interface RegisterRequest {
    first_name: string;
    last_name: string;
    email: string;
    phone_number?: string;
    password: string;
    }

export interface OTPRequest {
    phone_number: string;
    }

export interface OTPVerifyRequest {
    phone_number: string;
    otp_code: string;
    }