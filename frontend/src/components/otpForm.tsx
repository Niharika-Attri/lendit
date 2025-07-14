import React, { useState } from 'react';
import api from '../services/api';

interface OTPFormProps {
    onSuccess: () => void;
}

const OTPForm: React.FC<OTPFormProps> = ({ onSuccess }) => {
    const [phoneNumber, setPhoneNumber] = useState<string>('');
    const [otpCode, setOtpCode] = useState<string>('');
    const [otpSent, setOtpSent] = useState<boolean>(false);
    const [message, setMessage] = useState<string>('');

    const sendOtp = async (): Promise<void> => {
        try {
        const response = await api.post<{ message: string }>('/v1/otp/send', { phone_number: phoneNumber });
        setOtpSent(true);
        setMessage(response.data.message);
        } catch (error: any) {
        setMessage(error.response?.data?.detail || 'Failed to send OTP');
        }
    };

    const verifyOtp = async (): Promise<void> => {
        try {
        const response = await api.post<{ message: string }>(
            '/v1/otp/verify',
            { phone_number: phoneNumber, otp_code: otpCode }
        );
        setMessage(response.data.message);
        setOtpSent(false);
        onSuccess();
        } catch (error: any) {
        setMessage(error.response?.data?.detail || 'Failed to verify OTP');
        }
    };

    return (
        <div className="w-full mt-6">
        <h3 className="text-lg font-semibold text-white mb-4">Verify Phone Number</h3>
        <div className="flex flex-col gap-4">
            <div className="flex flex-col">
            <label className="text-white text-sm font-medium mb-1">Phone Number</label>
            <input
                type="text"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
                placeholder="+1234567890"
                className="h-10 px-4 rounded-lg bg-white/10 text-white placeholder:text-white/50 border border-white/20 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
                onClick={sendOtp}
                disabled={otpSent}
                className="mt-2 h-10 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-700 transition-colors disabled:bg-blue-400"
            >
                Send OTP
            </button>
            </div>
            {otpSent && (
            <div className="flex flex-col">
                <label className="text-white text-sm font-medium mb-1">OTP Code</label>
                <input
                type="text"
                value={otpCode}
                onChange={(e) => setOtpCode(e.target.value)}
                placeholder="123456"
                className="h-10 px-4 rounded-lg bg-white/10 text-white placeholder:text-white/50 border border-white/20 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                onClick={verifyOtp}
                className="mt-2 h-10 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-700 transition-colors"
                >
                Verify OTP
                </button>
            </div>
            )}
            {message && <p className="mt-4 text-red-400 text-center">{message}</p>}
        </div>
        </div>
    );
};

export default OTPForm;