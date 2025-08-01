import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatMessage from './components/ChatMessage';

const mockUserMessage = {
  id: '1',
  text: 'Hello, I need help planning a trip',
  sender: 'user',
  timestamp: '2025-07-31T12:00:00.000Z'
};

const mockAssistantMessage = {
  id: '2',
  text: 'I would be happy to help you plan your trip! Where would you like to go?',
  sender: 'assistant',
  timestamp: '2025-07-31T12:01:00.000Z',
  provider: 'ollama'
};

const mockErrorMessage = {
  id: '3',
  text: 'Sorry, I encountered an error',
  sender: 'assistant',
  timestamp: '2025-07-31T12:02:00.000Z',
  isError: true
};

describe('ChatMessage Component', () => {
  test('renders user message correctly', () => {
    render(<ChatMessage message={mockUserMessage} />);
    
    expect(screen.getByText('Hello, I need help planning a trip')).toBeInTheDocument();
    expect(screen.getByText('12:00 PM')).toBeInTheDocument();
  });

  test('renders assistant message correctly', () => {
    render(<ChatMessage message={mockAssistantMessage} />);
    
    expect(screen.getByText(/I would be happy to help you plan your trip/)).toBeInTheDocument();
    expect(screen.getByText('12:01 PM')).toBeInTheDocument();
    expect(screen.getByText('via ollama')).toBeInTheDocument();
  });

  test('renders error message correctly', () => {
    render(<ChatMessage message={mockErrorMessage} />);
    
    expect(screen.getByText('Sorry, I encountered an error')).toBeInTheDocument();
    expect(screen.getByText('12:02 PM')).toBeInTheDocument();
  });

  test('handles multiline text', () => {
    const multilineMessage = {
      ...mockUserMessage,
      text: 'Line 1\nLine 2\nLine 3'
    };

    render(<ChatMessage message={multilineMessage} />);
    
    expect(screen.getByText(/Line 1/)).toBeInTheDocument();
    expect(screen.getByText(/Line 2/)).toBeInTheDocument();
    expect(screen.getByText(/Line 3/)).toBeInTheDocument();
  });
});
