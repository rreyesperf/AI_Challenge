import React from 'react';
import { motion } from 'framer-motion';
import { FiMessageCircle } from 'react-icons/fi';
import { MessageContainer, MessageAvatar } from '../styles/MessageStyles';
import styled from 'styled-components';

const TypingContainer = styled.div`
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 16px 20px;
  background: white;
  border-radius: 18px 18px 18px 4px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  
  .typing-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #dc2626;
    animation: typingAnimation 1.4s infinite ease-in-out;
    
    &:nth-child(1) { animation-delay: 0ms; }
    &:nth-child(2) { animation-delay: 200ms; }
    &:nth-child(3) { animation-delay: 400ms; }
  }
  
  @keyframes typingAnimation {
    0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
    30% { transform: translateY(-10px); opacity: 1; }
  }
`;

const TypingIndicator = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={{ duration: 0.2 }}
    >
      <MessageContainer $isUser={false}>
        <MessageAvatar>
          <FiMessageCircle />
        </MessageAvatar>
        
        <TypingContainer className="typing-indicator">
          <div className="typing-dot"></div>
          <div className="typing-dot"></div>
          <div className="typing-dot"></div>
        </TypingContainer>
      </MessageContainer>
    </motion.div>
  );
};

export default TypingIndicator;
