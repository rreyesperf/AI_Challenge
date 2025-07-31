import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import '@testing-library/jest-dom';
import { AuthProvider } from './utils/AuthContext';
import App from './App';

// Mock components to avoid dependency issues
jest.mock('./pages/Login', () => {
  return function Login() {
    return <div data-testid="login-page">Login Page</div>;
  };
});

jest.mock('./pages/Chat', () => {
  return function Chat() {
    return <div data-testid="chat-page">Chat Page</div>;
  };
});

const AppWrapper = ({ children }) => (
  <BrowserRouter>
    <AuthProvider>
      {children}
    </AuthProvider>
  </BrowserRouter>
);

describe('App Component', () => {
  test('renders without crashing', () => {
    render(
      <AppWrapper>
        <App />
      </AppWrapper>
    );
  });

  test('displays login page when not authenticated', () => {
    render(
      <AppWrapper>
        <App />
      </AppWrapper>
    );
    
    const loginPage = screen.getByTestId('login-page');
    expect(loginPage).toBeInTheDocument();
  });

  test('has proper routing structure', () => {
    render(
      <AppWrapper>
        <App />
      </AppWrapper>
    );
    
    // Should render the app container
    const appContainer = document.querySelector('.App');
    expect(appContainer).toBeTruthy();
  });
});
