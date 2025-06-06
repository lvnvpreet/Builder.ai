import axios from 'axios';
import { useAppStore } from '@/store';
import type { BusinessData } from '@/types/generation';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
apiClient.interceptors.request.use((config) => {
  const token = useAppStore.getState().auth.token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle response errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle auth errors
    if (error.response?.status === 401) {
      useAppStore.getState().logout();
    }
    return Promise.reject(error);
  }
);

export const generationApi = {
  startGeneration: async (businessData: BusinessData) => {
    // Send data in the format expected by the backend
    const payload = {
      business_name: businessData.businessName,
      business_category: businessData.businessCategory,
      business_description: businessData.businessDescription,
      target_audience: businessData.targetAudience || "",
      // Additional backend fields if needed
      additional_requirements: businessData.additionalInfo || ""
    };
    
    console.log("Sending payload to backend:", payload);
    const response = await apiClient.post('/generate', payload);
    return response.data;
  },
  
  getGeneration: async (id: string) => {
    const response = await apiClient.get(`/generate/${id}`);
    return response.data;
  },
  
  cancelGeneration: async (id: string) => {
    const response = await apiClient.delete(`/generate/${id}`);
    return response.data;
  },
  
  getGenerationHistory: async () => {
    const response = await apiClient.get('/generate/history');
    return response.data;
  }
};

export const authApi = {
  login: async (email: string, password: string) => {
    const response = await apiClient.post('/auth/login', { email, password });
    return response.data;
  },
  
  signup: async (email: string, password: string, name?: string) => {
    const response = await apiClient.post('/auth/signup', { email, password, name });
    return response.data;
  },
  
  logout: async () => {
    const response = await apiClient.post('/auth/logout');
    return response.data;
  }
};

export default apiClient;
