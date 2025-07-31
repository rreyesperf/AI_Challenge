import React from 'react';
import { motion } from 'framer-motion';
import { FiUser, FiMessageCircle, FiAlertCircle } from 'react-icons/fi';
import {
  MessageContainer,
  MessageBubble,
  MessageContent,
  MessageText,
  MessageMeta,
  MessageTime,
  MessageProvider,
  MessageAvatar
} from '../styles/MessageStyles';

const ChatMessage = ({ message }) => {
  const isUser = message.sender === 'user';
  const isError = message.isError;
  const isWelcome = message.isWelcome;

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const formatText = (text) => {
    // Split text into paragraphs and preserve line breaks
    return text.split('\n').map((paragraph, index) => (
      <React.Fragment key={index}>
        {paragraph}
        {index < text.split('\n').length - 1 && <br />}
      </React.Fragment>
    ));
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="message-enter"
    >
      <MessageContainer $isUser={isUser} $isWelcome={isWelcome}>
        {!isUser && (
          <MessageAvatar $isError={isError}>
            {isError ? <FiAlertCircle /> : <FiMessageCircle />}
          </MessageAvatar>
        )}
        
        <MessageBubble $isUser={isUser} $isError={isError} $isWelcome={isWelcome}>
          <MessageContent>
            <MessageText $isUser={isUser} $isError={isError}>
              {formatText(message.text)}
            </MessageText>
            
            <MessageMeta>
              <MessageTime>{formatTime(message.timestamp)}</MessageTime>
              {message.provider && !isUser && (
                <MessageProvider>
                  via {message.provider}
                </MessageProvider>
              )}
              {message.conversationType && message.conversationType !== 'regular' && (
                <MessageProvider>
                  {message.conversationType}
                </MessageProvider>
              )}
            </MessageMeta>
          </MessageContent>
        </MessageBubble>
        
        {isUser && (
          <MessageAvatar $isUser={true}>
            <FiUser />
          </MessageAvatar>
        )}
      </MessageContainer>
    </motion.div>
  );
};

export default ChatMessage;
