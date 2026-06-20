import axios from 'axios';
import {
  QueryRequest,
  QueryResponseData,
  APIResponse,
  HealthResponse,
  StatusResponse,
  QueryHistoryItem,
  SavedQuery,
  UserPreferences,
  TableSchema,
} from '../types';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const queryAPI = {
  sendQuery: async (request: QueryRequest): Promise<APIResponse<QueryResponseData>> => {
    const response = await api.post('/query', request);
    return response.data;
  },
};

export const historyAPI = {
  getHistory: async (): Promise<APIResponse<QueryHistoryItem[]>> => {
    const response = await api.get('/history');
    return response.data;
  },
  createHistory: async (data: any): Promise<APIResponse<QueryHistoryItem>> => {
    const response = await api.post('/history', data);
    return response.data;
  },
  deleteHistory: async (id: string): Promise<APIResponse<any>> => {
    const response = await api.delete(`/history/${id}`);
    return response.data;
  },
};

export const savedQueriesAPI = {
  getSavedQueries: async (): Promise<APIResponse<SavedQuery[]>> => {
    const response = await api.get('/saved-queries');
    return response.data;
  },
  createSavedQuery: async (data: Omit<SavedQuery, 'id' | 'user_id' | 'created_at' | 'updated_at'>): Promise<APIResponse<SavedQuery>> => {
    const response = await api.post('/saved-queries', data);
    return response.data;
  },
  updateSavedQuery: async (id: string, data: Partial<Omit<SavedQuery, 'id' | 'user_id' | 'created_at' | 'updated_at'>>): Promise<APIResponse<SavedQuery>> => {
    const response = await api.put(`/saved-queries/${id}`, data);
    return response.data;
  },
  deleteSavedQuery: async (id: string): Promise<APIResponse<any>> => {
    const response = await api.delete(`/saved-queries/${id}`);
    return response.data;
  },
  toggleFavorite: async (id: string): Promise<APIResponse<SavedQuery>> => {
    const response = await api.patch(`/saved-queries/${id}/favorite`);
    return response.data;
  },
};

export const exportAPI = {
  exportCSV: async (data: Array<Record<string, any>>, filename: string): Promise<void> => {
    const response = await api.post('/exports/csv', { data, filename }, { responseType: 'blob' });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
  },
  exportExcel: async (data: Array<Record<string, any>>, filename: string): Promise<void> => {
    const response = await api.post('/exports/excel', { data, filename }, { responseType: 'blob' });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
  },
  exportPDF: async (data: { data: Array<Record<string, any>>, question: string, sql: string, insight: string, filename: string }): Promise<void> => {
    const response = await api.post('/exports/pdf', data, { responseType: 'blob' });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', data.filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
  },
};

export const preferencesAPI = {
  getPreferences: async (): Promise<APIResponse<UserPreferences>> => {
    const response = await api.get('/preferences');
    return response.data;
  },
  updatePreferences: async (data: Partial<UserPreferences>): Promise<APIResponse<UserPreferences>> => {
    const response = await api.put('/preferences', data);
    return response.data;
  },
};

export const schemaAPI = {
  getSchema: async (): Promise<APIResponse<TableSchema[]>> => {
    const response = await api.get('/schema');
    return response.data;
  },
};

export const dashboardAPI = {
  getStats: async (): Promise<APIResponse<{ total_revenue: number; total_orders: number; total_customers: number; total_products: number }>> => {
    const response = await api.get('/dashboard/stats');
    return response.data;
  },
};

export const healthAPI = {
  getHealth: async (): Promise<APIResponse<HealthResponse>> => {
    const healthBaseUrl = import.meta.env.VITE_API_BASE_URL ? import.meta.env.VITE_API_BASE_URL.replace('/api/v1', '') : '';
    const response = await axios.get(`${healthBaseUrl}/health`);
    return response.data;
  },

  getStatus: async (): Promise<APIResponse<StatusResponse>> => {
    const healthBaseUrl = import.meta.env.VITE_API_BASE_URL ? import.meta.env.VITE_API_BASE_URL.replace('/api/v1', '') : '';
    const response = await axios.get(`${healthBaseUrl}/status`);
    return response.data;
  },
};
