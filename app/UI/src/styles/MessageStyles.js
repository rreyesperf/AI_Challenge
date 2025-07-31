import styled from 'styled-components';

export const MessageContainer = styled.div`
  display: flex;
  gap: 12px;
  align-items: flex-start;
  justify-content: ${props => props.$isUser ? 'flex-end' : 'flex-start'};
  margin-bottom: ${props => props.$isWelcome ? '8px' : '16px'};

  @media (max-width: 768px) {
    gap: 8px;
    margin-bottom: 12px;
  }
`;

export const MessageAvatar = styled.div`
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: ${props => {
    if (props.$isUser) return 'linear-gradient(135deg, #dc2626, #ef4444)';
    if (props.$isError) return 'linear-gradient(135deg, #ef4444, #f87171)';
    return 'linear-gradient(135deg, #6b7280, #9ca3af)';
  }};
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

  svg {
    width: 18px;
    height: 18px;
  }

  @media (max-width: 768px) {
    width: 32px;
    height: 32px;

    svg {
      width: 16px;
      height: 16px;
    }
  }
`;

export const MessageBubble = styled.div`
  max-width: 70%;
  min-width: 120px;
  background: ${props => {
    if (props.$isError) return '#fef2f2';
    if (props.$isWelcome) return 'linear-gradient(135deg, #dc2626, #ef4444)';
    if (props.$isUser) return 'linear-gradient(135deg, #dc2626, #ef4444)';
    return 'linear-gradient(135deg, #4b5563, #6b7280)'; // Dark gradient for AI messages with white text
  }};
  border-radius: ${props => {
    if (props.$isUser) return '18px 18px 4px 18px';
    return '18px 18px 18px 4px';
  }};
  padding: 16px 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  border: ${props => props.$isError ? '1px solid #fecaca' : 'none'};
  word-wrap: break-word;
  overflow-wrap: break-word;

  @media (max-width: 768px) {
    max-width: 85%;
    padding: 12px 16px;
    border-radius: ${props => {
      if (props.$isUser) return '16px 16px 4px 16px';
      return '16px 16px 16px 4px';
    }};
  }
`;

export const MessageContent = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

export const MessageText = styled.div`
  font-size: 15px;
  line-height: 1.5;
  color: ${props => {
    if (props.$isError) return '#dc2626';
    if (props.$isUser) return 'white';
    if (props.$isWelcome) return 'white';
    return 'white'; // Changed from '#1f2937' to 'white' for better readability
  }};
  white-space: pre-wrap;

  @media (max-width: 768px) {
    font-size: 14px;
  }
`;

export const MessageMeta = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 4px;
`;

export const MessageTime = styled.span`
  font-size: 11px;
  opacity: 0.7;
  color: ${props => props.$isUser ? 'rgba(255, 255, 255, 0.8)' : 'rgba(255, 255, 255, 0.8)'};
`;

export const MessageProvider = styled.span`
  font-size: 11px;
  opacity: 0.7;
  color: ${props => props.$isUser ? 'rgba(255, 255, 255, 0.8)' : 'rgba(255, 255, 255, 0.8)'};
  
  &::before {
    content: '•';
    margin-right: 4px;
  }
`;

export const ErrorIcon = styled.div`
  color: #dc2626;
  margin-right: 4px;
  
  svg {
    width: 14px;
    height: 14px;
  }
`;
