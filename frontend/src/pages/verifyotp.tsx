import type React from "react";
import OTPForm from "../components/otpForm";
import { useNavigate } from "react-router-dom";

const VerifyOtp: React.FC = () => {
    const navigate = useNavigate()
    const handleOTPSuccess = () => {
        navigate('/login')
    }

    return(
        <OTPForm onSuccess={handleOTPSuccess} />
    )
}

export default VerifyOtp