import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || (process.env.NODE_ENV === 'development' ? '' : 'http://127.0.0.1:5000'),
  timeout: 120000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.status, error.message);
    return Promise.reject(error);
  }
);

export const chatAPI = {
  // Send message to chat endpoint
  sendMessage: async (message, conversationHistory = []) => {
    try {
      const response = await api.post('/api/ai/chat', {
        message,
        conversation_history: conversationHistory,
      });
      
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Chat API Error:', error);
      
      let errorMessage = 'Failed to send message';
      
      if (error.code === 'ECONNABORTED') {
        errorMessage = 'Request timed out. Please try again.';
      } else if (error.response) {
        errorMessage = error.response.data?.error || `Server error: ${error.response.status}`;
      } else if (error.request) {
        errorMessage = 'Unable to connect to server. Please check your connection.';
      }
      
      return {
        success: false,
        error: errorMessage
      };
    }
  },

  // Check API health
  checkHealth: async () => {
    try {
      console.log('Attempting health check to:', process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000');
      const response = await api.get('/api/health');
      console.log('Health check successful:', response.data);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Health Check Error Details:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status,
        config: error.config
      });
      return {
        success: false,
        error: 'Health check failed'
      };
    }
  },

  // Check AI service health
  checkAIHealth: async () => {
    try {
      const response = await api.get('/api/ai/health');
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('AI Health Check Error:', error);
      return {
        success: false,
        error: 'AI health check failed'
      };
    }
  }
};

export default api;
