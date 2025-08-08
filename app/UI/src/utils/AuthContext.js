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

  // Security utility functions
  const sanitizeInput = (input) => {
    if (typeof input !== 'string') return '';
    
    // Remove potentially dangerous characters while preserving valid password chars
    // Allow alphanumeric, spaces, and common password special characters
    return input.replace(/[<>'"&]/g, '').replace(/[\x00-\x1F\x7F-\x9F]/g, '');
  };

  const secureCompare = (input, expected) => {
    // Normalize both strings to handle encoding issues
    const normalizedInput = String(input || '').normalize('NFC');
    const normalizedExpected = String(expected || '').normalize('NFC');
    
    // Use constant-time comparison to prevent timing attacks
    if (normalizedInput.length !== normalizedExpected.length) {
      return false;
    }
    
    let result = 0;
    for (let i = 0; i < normalizedInput.length; i++) {
      result |= normalizedInput.charCodeAt(i) ^ normalizedExpected.charCodeAt(i);
    }
    
    return result === 0;
  };

  const login = (username, password) => {
    try {
      // Get credentials from environment variables
      const validUsername = process.env.REACT_APP_AUTH_USERNAME;
      const validPassword = process.env.REACT_APP_AUTH_PASSWORD;
      console.log(validUsername);
      console.log(validPassword);
      // Debug logging (remove in production)
      if (process.env.REACT_APP_DEBUG_MODE === 'true') {
        console.log('Auth Debug - Environment variables loaded:', {
          hasUsername: !!validUsername,
          hasPassword: !!validPassword,
          usernameLength: validUsername?.length || 0,
          passwordLength: validPassword?.length || 0
        });
      }
      
      // Check if environment variables are configured
      if (!validUsername || !validPassword) {
        return { success: false, error: 'Authentication not configured. Please contact administrator.' };
      }
      
      // Validate input presence
      if (!username || !password) {
        return { success: false, error: 'Please enter both username and password' };
      }
      
      // Sanitize inputs to prevent injection attacks
      const sanitizedUsername = sanitizeInput(username.trim());
      const sanitizedPassword = sanitizeInput(password);
      
      // Debug logging
      if (process.env.REACT_APP_DEBUG_MODE === 'true') {
        console.log('Auth Debug - Input processing:', {
          originalUsername: username,
          sanitizedUsername: sanitizedUsername,
          originalPasswordLength: password.length,
          sanitizedPasswordLength: sanitizedPassword.length,
          passwordChanged: password !== sanitizedPassword
        });
      }
      
      // Additional validation
      if (sanitizedUsername.length === 0 || sanitizedPassword.length === 0) {
        return { success: false, error: 'Invalid characters in credentials' };
      }
      
      // Rate limiting check (simple implementation)
      const now = Date.now();
      const lastAttempt = localStorage.getItem('lastLoginAttempt');
      if (lastAttempt && (now - parseInt(lastAttempt)) < 1000) {
        return { success: false, error: 'Please wait before trying again' };
      }
      localStorage.setItem('lastLoginAttempt', now.toString());
      
      // Secure comparison
      const usernameValid = secureCompare(sanitizedUsername, validUsername);
      const passwordValid = secureCompare(sanitizedPassword, validPassword);
      
      // Debug logging
      if (process.env.REACT_APP_DEBUG_MODE === 'true') {
        console.log('Auth Debug - Comparison results:', {
          usernameValid,
          passwordValid,
          inputUsernameLength: sanitizedUsername.length,
          expectedUsernameLength: validUsername.length,
          inputPasswordLength: sanitizedPassword.length,
          expectedPasswordLength: validPassword.length
        });
      }
      
      if (usernameValid && passwordValid) {
        // Clear failed attempts on success
        localStorage.removeItem('lastLoginAttempt');
        
        const userData = {
          username: sanitizedUsername, // Store sanitized version
          id: Date.now().toString(),
          loginTime: new Date().toISOString()
        };
        
        setUser(userData);
        setIsAuthenticated(true);
        localStorage.setItem('chatUser', JSON.stringify(userData));
        
        return { success: true };
      }
      
      return { success: false, error: 'Invalid username or password' };
      
    } catch (error) {
      console.error('Authentication error:', error);
      return { success: false, error: 'Authentication failed. Please try again.' };
    }
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
