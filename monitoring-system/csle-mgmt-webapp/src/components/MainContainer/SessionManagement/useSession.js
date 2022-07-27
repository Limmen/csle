import { useState } from 'react';

export default function useSession() {
    const getSessionData = () => {
        const sessionDataString = localStorage.getItem('csleSession');
        return JSON.parse(sessionDataString)
    };

    const [sessionData, setSessionData] = useState(getSessionData());

    const saveSessionData = sessionData => {
        localStorage.setItem('csleSession', JSON.stringify(sessionData));
        setToken(sessionData);
    };

    return {
        setToken: saveSessionData,
        sessionData
    }
}