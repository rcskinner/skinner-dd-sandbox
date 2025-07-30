import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface SimpleSpan {
  name: string;
  type: string;
}

export const getTraces = async (): Promise<SimpleSpan[]> => {
  try {
    const response = await api.get('/');
    // The backend returns spans in the response.data.spans array
    return response.data.spans || [];
  } catch (error) {
    console.error('Error fetching traces:', error);
    throw error;
  }
};

export const triggerError = async (): Promise<void> => {
  try {
    await api.get('/error');
  } catch (error) {
    console.error('Error triggering error endpoint:', error);
    throw error;
  }
}; 