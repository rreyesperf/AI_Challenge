import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiUser, FiLock, FiMessageCircle } from 'react-icons/fi';
import { useAuth } from '../utils/AuthContext';
import {
  LoginContainer,
  LoginCard,
  Logo,
  Title,
  Subtitle,
  Form,
  InputGroup,
  InputIcon,
  Input,
  LoginButton,
  ErrorMessage,
  Features,
  Feature
} from '../styles/LoginStyles';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    // Simulate login delay for better UX
    setTimeout(() => {
      const result = login(username, password);
      
      if (result.success) {
        navigate('/chat');
      } else {
        setError(result.error);
      }
      setIsLoading(false);
    }, 800);
  };

  return (
    <LoginContainer>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <LoginCard>
          <Logo>
            <FiMessageCircle size={48} />
          </Logo>
          
          <Title>Travel Chat Assistant</Title>
          <Subtitle>Your AI-powered travel planning companion</Subtitle>

          <Form onSubmit={handleSubmit}>
            <InputGroup>
              <InputIcon>
                <FiUser />
              </InputIcon>
              <Input
                type="text"
                placeholder="Enter your username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </InputGroup>

            <InputGroup>
              <InputIcon>
                <FiLock />
              </InputIcon>
              <Input
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </InputGroup>

            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="shake"
              >
                <ErrorMessage>{error}</ErrorMessage>
              </motion.div>
            )}

            <LoginButton type="submit" disabled={isLoading}>
              {isLoading ? (
                <div className="loading-dots">
                  <div className="loading-dot"></div>
                  <div className="loading-dot"></div>
                  <div className="loading-dot"></div>
                </div>
              ) : (
                'Sign In'
              )}
            </LoginButton>
          </Form>

          <Features>
            <Feature>
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3, duration: 0.5 }}
              >
                ✈️ Plan flights and hotels
              </motion.div>
            </Feature>
            <Feature>
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5, duration: 0.5 }}
              >
                🍽️ Discover local dining
              </motion.div>
            </Feature>
            <Feature>
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.7, duration: 0.5 }}
              >
                🚗 Arrange transportation
              </motion.div>
            </Feature>
          </Features>
        </LoginCard>
      </motion.div>
    </LoginContainer>
  );
};

export default Login;
