import { chatAPI } from './utils/api';

// Mock axios
jest.mock('axios', () => ({
  create: jest.fn(() => ({
    post: jest.fn(),
    get: jest.fn(),
    interceptors: {
      request: { use: jest.fn() },
      response: { use: jest.fn() }
    }
  }))
}));

describe('Chat API', () => {
  test('sendMessage returns success response', async () => {
    const mockResponse = {
      data: {
        success: true,
        response: 'Test response',
        provider: 'ollama'
      }
    };

    // Mock the axios instance
    const axios = require('axios');
    const mockAxiosInstance = axios.create();
    mockAxiosInstance.post.mockResolvedValue(mockResponse);

    const result = await chatAPI.sendMessage('Test message');
    
    expect(result.success).toBe(true);
    expect(result.data.response).toBe('Test response');
  });

  test('sendMessage handles errors', async () => {
    const axios = require('axios');
    const mockAxiosInstance = axios.create();
    mockAxiosInstance.post.mockRejectedValue(new Error('Network error'));

    const result = await chatAPI.sendMessage('Test message');
    
    expect(result.success).toBe(false);
    expect(result.error).toBeDefined();
  });

  test('checkHealth returns status', async () => {
    const mockResponse = {
      data: {
        status: 'healthy',
        services: { enhanced_chat: true }
      }
    };

    const axios = require('axios');
    const mockAxiosInstance = axios.create();
    mockAxiosInstance.get.mockResolvedValue(mockResponse);

    const result = await chatAPI.checkHealth();
    
    expect(result.success).toBe(true);
    expect(result.data.status).toBe('healthy');
  });
});
