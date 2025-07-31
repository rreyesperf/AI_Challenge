import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import '@testing-library/jest-dom';
import TypingIndicator from './components/TypingIndicator';

// Mock framer-motion
jest.mock('framer-motion', () => ({
  motion: {
    div: ({ children, ...props }) => <div {...props}>{children}</div>
  }
}));

const TypingIndicatorWrapper = ({ ...props }) => (
  <BrowserRouter>
    <TypingIndicator {...props} />
  </BrowserRouter>
);

describe('TypingIndicator Component', () => {
  test('renders typing indicator', () => {
    render(<TypingIndicatorWrapper />);
    
    // Look for the typing indicator by class or content
    const typingElement = document.querySelector('.typing-indicator');
    expect(typingElement).toBeInTheDocument();
  });

  test('displays typing dots', () => {
    render(<TypingIndicatorWrapper />);
    
    const dots = document.querySelectorAll('.typing-dot');
    expect(dots).toHaveLength(3);
  });

  test('has correct container structure', () => {
    render(<TypingIndicatorWrapper />);
    
    const typingElement = document.querySelector('.typing-indicator');
    expect(typingElement).toBeInTheDocument();
    
    // Check that it contains the expected number of dots
    const dots = typingElement.querySelectorAll('.typing-dot');
    expect(dots).toHaveLength(3);
  });
});
