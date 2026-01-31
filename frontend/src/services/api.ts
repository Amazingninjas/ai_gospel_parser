import axios, { AxiosError } from 'axios';
import type { InternalAxiosRequestConfig } from 'axios';

// Get API URL from environment variable
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Retry configuration
const MAX_RETRIES = 3;
const RETRY_DELAY = 1000; // 1 second
const RETRY_STATUS_CODES = [408, 429, 500, 502, 503, 504];

// Sleep utility for retries
const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

// Create axios instance with default config
const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout
});

// Add retry count to request config
interface RetryConfig extends InternalAxiosRequestConfig {
  _retryCount?: number;
}

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling and retries
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const config = error.config as RetryConfig;

    // Handle 401 Unauthorized
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
      return Promise.reject(error);
    }

    // Retry logic for specific status codes
    const shouldRetry =
      config &&
      RETRY_STATUS_CODES.includes(error.response?.status || 0) &&
      (!config._retryCount || config._retryCount < MAX_RETRIES);

    if (shouldRetry) {
      config._retryCount = (config._retryCount || 0) + 1;
      const delay = RETRY_DELAY * Math.pow(2, config._retryCount - 1); // Exponential backoff

      console.log(`Retrying request (${config._retryCount}/${MAX_RETRIES}) after ${delay}ms...`);
      await sleep(delay);

      return api.request(config);
    }

    return Promise.reject(error);
  }
);

/**
 * Format error message from API response
 */
export const formatErrorMessage = (error: unknown): string => {
  if (axios.isAxiosError(error)) {
    // API returned an error response
    if (error.response?.data?.detail) {
      return typeof error.response.data.detail === 'string'
        ? error.response.data.detail
        : 'An error occurred';
    }

    // Network errors
    if (error.code === 'ECONNABORTED') {
      return 'Request timeout. Please try again.';
    }
    if (error.code === 'ERR_NETWORK') {
      return 'Network error. Please check your connection.';
    }

    // HTTP status errors
    if (error.response?.status) {
      const statusMessages: Record<number, string> = {
        400: 'Invalid request',
        401: 'Please log in to continue',
        403: 'Access denied',
        404: 'Resource not found',
        408: 'Request timeout',
        429: 'Too many requests. Please try again later.',
        500: 'Server error. Please try again.',
        502: 'Bad gateway. Please try again.',
        503: 'Service unavailable. Please try again later.',
        504: 'Gateway timeout. Please try again.',
      };
      return statusMessages[error.response.status] || 'An error occurred';
    }
  }

  return 'An unexpected error occurred';
};

export default api;
