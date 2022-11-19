import { useState } from 'react';

/**
 * Utility functions for managing user sessions
 */
export default function useSession() {
    const getSessionData = () => {
        const sessionDataString = localStorage.getItem('csleSession');
        return JSON.parse(sessionDataString)
    };

    const [sessionData, setSessionData] = useState(getSessionData());

    const saveSessionData = sessionData => {
        localStorage.setItem('csleSession', JSON.stringify(sessionData));
        setSessionData(sessionData);
    };

    return {
        setSessionData: saveSessionData,
        sessionData
    }
}