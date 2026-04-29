import axios from 'axios';

const api = axios.create({
  baseURL: '/api/v1',
});

// Request interceptor for API calls
api.interceptors.request.use(
  async (config) => {
    const token = localStorage.getItem('study_ai_token');
    config.headers['Accept'] = 'application/json';
    config.headers['Content-Type'] = 'application/json';
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    Promise.reject(error);
  }
);

// Response interceptor for API calls
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('study_ai_token');
      localStorage.removeItem('study_ai_user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
