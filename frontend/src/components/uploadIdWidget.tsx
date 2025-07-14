import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { type UserResponse } from '../types/user';

interface UploadWidgetProps {
    userId: number;
    token: string;
}

interface CloudinaryResult {
    event: string;
    info: { secure_url: string };
}

const UploadWidget: React.FC<UploadWidgetProps> = ({ userId, token }) => {
    const [collegeIdUrl, setCollegeIdUrl] = useState<string | null>(null);
    const [phoneNumber, setPhoneNumber] = useState<string>('');
    const [otpCode, setOtpCode] = useState<string>('');
    const [otpSent, setOtpSent] = useState<boolean>(false);
    const [message, setMessage] = useState<string>('');

    const sendOtp = async (): Promise<void> => {
        try {
        const response = await axios.post<{ message: string }>('/api/v1/otp/send', { phone_number: phoneNumber });
        setOtpSent(true);
        setMessage(response.data.message);
        } catch (error: any) {
        setMessage(error.response?.data?.detail || 'Failed to send OTP');
        }
    };

    const verifyOtp = async (): Promise<void> => {
        try {
        const response = await axios.post<{ message: string }>(
            '/api/v1/otp/verify',
            { phone_number: phoneNumber, otp_code: otpCode }
        );
        setMessage(response.data.message);
        setOtpSent(false);
        } catch (error: any) {
        setMessage(error.response?.data?.detail || 'Failed to verify OTP');
        }
    };

    useEffect(() => {
        if (!window.cloudinary) {
        console.error('Cloudinary script not loaded');
        return;
        }

        const myWidget = window.cloudinary.createUploadWidget(
        {
            cloudName: 'djopmrv4e',
            uploadPreset: 'lendit_upload',
            folder: 'lendit/college_ids',
            publicId: `user_${userId}`,
            sources: ['local'],
            multiple: false,
            resourceType: 'image',
            clientAllowedFormats: ['jpg', 'png', 'jpeg'],
        },
        (error: any, result: CloudinaryResult) => {
            if (!error && result && result.event === 'success') {
            setCollegeIdUrl(result.info.secure_url);
            axios
                .put<UserResponse>(
                `/api/v1/users/${userId}`,
                { college_id_url: result.info.secure_url },
                {
                    headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'application/json',
                    },
                }
                )
                .then(response => console.log('User updated:', response.data))
                .catch(error => console.error('Error updating user:', error.response?.data || error.message));
            } else if (error) {
            console.error('Upload error:', error);
            }
        }
        );

        const button = document.getElementById('upload_widget');
        if (button) {
        button.addEventListener('click', () => myWidget.open(), false);
        }

        return () => {
        if (button) {
            button.removeEventListener('click', myWidget.open);
        }
        };
    }, [userId, token]);

    return (
        <div>
        <h3>Update Profile</h3>
        <div>
            <label>Phone Number:</label>
            <input
            type="text"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            placeholder="+1234567890"
            />
            <button onClick={sendOtp} disabled={otpSent}>Send OTP</button>
        </div>
        {otpSent && (
            <div>
            <label>OTP Code:</label>
            <input
                type="text"
                value={otpCode}
                onChange={(e) => setOtpCode(e.target.value)}
                placeholder="123456"
            />
            <button onClick={verifyOtp}>Verify OTP</button>
            </div>
        )}
        <div>
            <button id="upload_widget" className="cloudinary-button">
            Upload College ID
            </button>
            {collegeIdUrl && <img src={collegeIdUrl} alt="College ID" style={{ maxWidth: '200px' }} />}
        </div>
        {message && <p>{message}</p>}
        </div>
    );
};

export default UploadWidget;