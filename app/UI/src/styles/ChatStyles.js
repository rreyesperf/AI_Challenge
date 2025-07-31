import styled from 'styled-components';

export const ChatContainer = styled.div`
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
`;

export const Header = styled.header`
  background: linear-gradient(135deg, #dc2626, #ef4444);
  color: white;
  padding: 16px 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  z-index: 10;
  position: relative;

  @media (max-width: 768px) {
    padding: 12px 16px;
  }
`;

export const HeaderContent = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
`;

export const Logo = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 20px;
  font-weight: 700;

  svg {
    width: 28px;
    height: 28px;
  }

  @media (max-width: 768px) {
    font-size: 18px;
    
    svg {
      width: 24px;
      height: 24px;
    }
  }
`;

export const UserInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 16px;

  .user-details {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    color: rgba(255, 255, 255, 0.9);

    svg {
      width: 16px;
      height: 16px;
    }
  }

  @media (max-width: 768px) {
    gap: 12px;
  }
`;

export const ConnectionStatus = styled.div`
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: ${props => props.$connected ? 'rgba(255, 255, 255, 0.9)' : '#fca5a5'};

  svg {
    width: 16px;
    height: 16px;
  }
`;

export const LogoutButton = styled.button`
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-1px);
  }

  svg {
    width: 16px;
    height: 16px;
  }

  @media (max-width: 768px) {
    padding: 8px;
  }
`;

export const ErrorBanner = styled.div`
  background: #fef2f2;
  border-bottom: 1px solid #fecaca;
  color: #dc2626;
  padding: 12px 24px;
  text-align: center;
  font-size: 14px;

  @media (max-width: 768px) {
    padding: 10px 16px;
  }
`;

export const MessagesContainer = styled.div`
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
`;

export const MessagesList = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;

  @media (max-width: 768px) {
    padding: 16px;
    gap: 12px;
  }
`;

export const InputContainer = styled.div`
  background: white;
  border-top: 1px solid #e5e7eb;
  padding: 20px 24px;

  form {
    display: flex;
    gap: 12px;
    max-width: 1200px;
    margin: 0 auto;
    align-items: flex-end;
  }

  @media (max-width: 768px) {
    padding: 16px;
    
    form {
      gap: 8px;
    }
  }
`;

export const MessageInput = styled.textarea`
  flex: 1;
  min-height: 44px;
  max-height: 120px;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 16px;
  font-family: inherit;
  resize: none;
  transition: all 0.2s ease;
  background: #f9fafb;

  &:focus {
    outline: none;
    border-color: #dc2626;
    background: white;
    box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
  }

  &::placeholder {
    color: #9ca3af;
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  @media (max-width: 768px) {
    font-size: 16px; /* Prevent zoom on iOS */
  }
`;

export const SendButton = styled.button`
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #dc2626, #ef4444);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  flex-shrink: 0;

  &:hover:not(:disabled) {
    background: linear-gradient(135deg, #b91c1c, #dc2626);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
  }

  &:active {
    transform: translateY(0);
  }

  &:disabled {
    opacity: 0.4;
    cursor: not-allowed;
    transform: none;
  }

  svg {
    width: 18px;
    height: 18px;
  }
`;

export const WelcomeMessage = styled.div`
  text-align: center;
  padding: 40px 20px;
  color: #6b7280;

  h2 {
    color: #dc2626;
    margin-bottom: 12px;
    font-size: 24px;
  }

  p {
    font-size: 16px;
    line-height: 1.6;
    max-width: 600px;
    margin: 0 auto;
  }

  @media (max-width: 768px) {
    padding: 24px 16px;

    h2 {
      font-size: 20px;
      margin-bottom: 8px;
    }

    p {
      font-size: 14px;
    }
  }
`;
