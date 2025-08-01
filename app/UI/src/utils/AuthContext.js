import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in (from localStorage)
    const savedUser = localStorage.getItem('chatUser');
    if (savedUser) {
      try {
        const userData = JSON.parse(savedUser);
        setUser(userData);
        setIsAuthenticated(true);
      } catch (error) {
        console.error('Error parsing saved user data:', error);
        localStorage.removeItem('chatUser');
      }
    }
    setLoading(false);
  }, []);

  const login = (username, password) => {
    // Get credentials from environment variables
    const validUsername = process.env.REACT_APP_AUTH_USERNAME;
    const validPassword = process.env.REACT_APP_AUTH_PASSWORD;
    
    // Check if environment variables are configured
    if (!validUsername || !validPassword) {
      return { success: false, error: 'Authentication not configured. Please contact administrator.' };
    }
    
    if (!username || !password) {
      return { success: false, error: 'Please enter both username and password' };
    }
    
    if (username === validUsername && password === validPassword) {
      const userData = {
        username,
        id: Date.now().toString(),
        loginTime: new Date().toISOString()
      };
      
      setUser(userData);
      setIsAuthenticated(true);
      localStorage.setItem('chatUser', JSON.stringify(userData));
      
      return { success: true };
    }
    
    return { success: false, error: 'Invalid username or password' };
  };

  const logout = () => {
    setUser(null);
    setIsAuthenticated(false);
    localStorage.removeItem('chatUser');
  };

  const value = {
    isAuthenticated,
    user,
    login,
    logout,
    loading
  };

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        background: 'linear-gradient(135deg, #dc2626, #ef4444)',
        color: 'white',
        fontSize: '18px'
      }}>
        Loading...
      </div>
    );
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
