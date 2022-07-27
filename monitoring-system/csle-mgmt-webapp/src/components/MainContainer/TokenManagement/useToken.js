import { useState } from 'react';

export default function useToken() {
    const getToken = () => {
        const tokenString = localStorage.getItem('token');
        const token = JSON.parse(tokenString)
        return token
    };

    const [token, setToken] = useState(getToken());

    const saveToken = userToken => {
        console.log("token set")
        console.log(userToken)
        localStorage.setItem('token', JSON.stringify(userToken));
        setToken(userToken.token);
    };

    return {
        setToken: saveToken,
        token
    }
}