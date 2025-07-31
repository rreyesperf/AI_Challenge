import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiSend, FiLogOut, FiUser, FiMessageCircle, FiWifi, FiWifiOff } from 'react-icons/fi';
import { useAuth } from '../utils/AuthContext';
import { chatAPI } from '../utils/api';
import ChatMessage from '../components/ChatMessage';
import TypingIndicator from '../components/TypingIndicator';
import {
  ChatContainer,
  Header,
  HeaderContent,
  Logo,
  UserInfo,
  LogoutButton,
  ConnectionStatus,
  MessagesContainer,
  MessagesList,
  InputContainer,
  MessageInput,
  SendButton,
  ErrorBanner
} from '../styles/ChatStyles';

const Chat = () => {
  const { user, logout } = useAuth();
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isConnected, setIsConnected] = useState(true);
  const [error, setError] = useState('');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  // Check API health on component mount
  useEffect(() => {
    checkConnection();
    
    // Add welcome message
    const welcomeMsg = {
      id: 'welcome',
      text: `Hello ${user?.username}! 👋 I'm your travel assistant. I can help you plan trips, find flights, hotels, restaurants, and transportation. What would you like to explore today?`,
      sender: 'assistant',
      timestamp: new Date().toISOString(),
      isWelcome: true
    };
    setMessages([welcomeMsg]);
  }, [user]);

  const checkConnection = async () => {
    try {
      const result = await chatAPI.checkHealth();
      setIsConnected(result.success);
      if (!result.success) {
        setError('Unable to connect to chat service');
      }
    } catch (error) {
      setIsConnected(false);
      setError('Connection failed');
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!inputMessage.trim() || isTyping) return;

    const userMessage = {
      id: Date.now().toString(),
      text: inputMessage.trim(),
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    // Add user message immediately
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);
    setError('');

    try {
      // Prepare conversation history (last 10 messages for context)
      const conversationHistory = messages
        .filter(msg => !msg.isWelcome)
        .slice(-10)
        .map(msg => ({
          role: msg.sender === 'user' ? 'user' : 'assistant',
          content: msg.text
        }));

      const result = await chatAPI.sendMessage(userMessage.text, conversationHistory);
      
      if (result.success) {
        const assistantMessage = {
          id: (Date.now() + 1).toString(),
          text: result.data.response || 'I received your message but have no response.',
          sender: 'assistant',
          timestamp: new Date().toISOString(),
          provider: result.data.provider,
          conversationType: result.data.conversation_type
        };

        setMessages(prev => [...prev, assistantMessage]);
        setIsConnected(true);
      } else {
        throw new Error(result.error);
      }
    } catch (error) {
      console.error('Chat error:', error);
      
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        text: error.message || 'Sorry, I encountered an error. Please try again.',
        sender: 'assistant',
        timestamp: new Date().toISOString(),
        isError: true
      };

      setMessages(prev => [...prev, errorMessage]);
      setError('Failed to send message');
      setIsConnected(false);
    } finally {
      setIsTyping(false);
    }
  };

  const handleLogout = () => {
    logout();
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };

  return (
    <ChatContainer>
      <Header>
        <HeaderContent>
          <Logo>
            <FiMessageCircle />
            <span>Travel Chat</span>
          </Logo>
          
          <UserInfo>
            <ConnectionStatus $connected={isConnected}>
              {isConnected ? <FiWifi /> : <FiWifiOff />}
              <span className="desktop-only">
                {isConnected ? 'Connected' : 'Disconnected'}
              </span>
            </ConnectionStatus>
            
            <div className="user-details">
              <FiUser />
              <span className="desktop-only">{user?.username}</span>
            </div>
            
            <LogoutButton onClick={handleLogout} title="Logout">
              <FiLogOut />
              <span className="desktop-only">Logout</span>
            </LogoutButton>
          </UserInfo>
        </HeaderContent>
      </Header>

      {error && (
        <ErrorBanner>
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            {error}
          </motion.div>
        </ErrorBanner>
      )}

      <MessagesContainer>
        <MessagesList>
          <AnimatePresence>
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
          </AnimatePresence>
          
          {isTyping && <TypingIndicator />}
          
          <div ref={messagesEndRef} />
        </MessagesList>
      </MessagesContainer>

      <InputContainer>
        <form onSubmit={handleSendMessage}>
          <MessageInput
            ref={inputRef}
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me about your travel plans..."
            disabled={isTyping || !isConnected}
            maxLength={1000}
          />
          <SendButton 
            type="submit" 
            disabled={!inputMessage.trim() || isTyping || !isConnected}
            title="Send message"
          >
            <FiSend />
          </SendButton>
        </form>
      </InputContainer>
    </ChatContainer>
  );
};

export default Chat;
