import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import '@testing-library/jest-dom';
import Login from './pages/Login';
import { AuthProvider } from './utils/AuthContext';

const LoginWrapper = () => (
  <BrowserRouter>
    <AuthProvider>
      <Login />
    </AuthProvider>
  </BrowserRouter>
);

describe('Login Page', () => {
  test('renders login form', () => {
    render(<LoginWrapper />);
    
    expect(screen.getByText('Travel Chat Assistant')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter your username')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter your password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
  });

  test('shows error for empty credentials', async () => {
    render(<LoginWrapper />);
    
    const loginButton = screen.getByRole('button', { name: /sign in/i });
    fireEvent.click(loginButton);

    await waitFor(() => {
      expect(screen.getByText(/please enter both username and password/i)).toBeInTheDocument();
    });
  });

  test('allows user input', () => {
    render(<LoginWrapper />);
    
    const usernameInput = screen.getByPlaceholderText('Enter your username');
    const passwordInput = screen.getByPlaceholderText('Enter your password');

    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(passwordInput, { target: { value: 'testpass' } });

    expect(usernameInput.value).toBe('testuser');
    expect(passwordInput.value).toBe('testpass');
  });

  test('displays feature list', () => {
    render(<LoginWrapper />);
    
    expect(screen.getByText(/plan flights and hotels/i)).toBeInTheDocument();
    expect(screen.getByText(/discover local dining/i)).toBeInTheDocument();
    expect(screen.getByText(/arrange transportation/i)).toBeInTheDocument();
  });
});
