export interface LoginResponse {
    access_token: string;
    token_type: string;
}

export interface JWTPayload {
    id: number;
    email: string;
    exp: number;
}