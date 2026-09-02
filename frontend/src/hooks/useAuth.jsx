import React, { createContext, useState, useEffect, useContext } from 'react';

const AuthContext = createContext({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  logout: async () => {},
});

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const [services, setServices] = useState(null);

  const checkAuthStatus = async () => {
    try {
      const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
      const response = await fetch(`${baseUrl}/auth/google/status`, {
        credentials: 'include' // Important for sending the session cookie
      });
      
      if (response.ok) {
        const data = await response.json();
        if (data.connected && data.user) {
          setUser(data.user);
          setServices(data.services || null);
          setIsAuthenticated(true);
        } else {
          setUser(null);
          setServices(null);
          setIsAuthenticated(false);
        }
      }
    } catch (error) {
      console.error('Failed to fetch auth status:', error);
      setUser(null);
      setServices(null);
      setIsAuthenticated(false);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    checkAuthStatus();
    
    // Check if we just redirected back from Google (has query param)
    if (window.location.search.includes('google=connected')) {
      // Clear the query param from URL without refreshing
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, []);

  const logout = async () => {
    try {
      const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
      await fetch(`${baseUrl}/auth/google/disconnect`, {
        method: 'POST',
        credentials: 'include'
      });
      setUser(null);
      setServices(null);
      setIsAuthenticated(false);
    } catch (error) {
      console.error('Failed to disconnect:', error);
    }
  };

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, isLoading, services, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
