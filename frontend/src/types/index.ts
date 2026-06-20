export interface QueryRequest {
  question: string;
}

export interface QueryResponseData {
  question: string;
  sql: string;
  data: Array<Record<string, any>>;
  insight: string;
}

export interface APIResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface HealthResponse {
  status: string;
  version: string;
  timestamp: string;
}

export interface StatusResponse {
  database: string;
  redis: string;
  overall: string;
}

export interface QueryHistoryItem {
  id: string;
  user_id: string;
  database_connection_id: string;
  natural_language_query: string;
  generated_sql: string;
  execution_time_ms?: number;
  row_count?: number;
  success: boolean;
  error_message?: string;
  created_at: string;
  updated_at: string;
}

export interface SavedQuery {
  id: string;
  user_id: string;
  name: string;
  description?: string;
  natural_language_query: string;
  generated_sql: string;
  tags?: string[];
  is_favorite: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserPreferences {
  id: string;
  user_id: string;
  theme: string;
  dashboard_settings: Record<string, any>;
  saved_filters: any[];
  preferred_chart_type: string;
  created_at: string;
  updated_at: string;
}

export interface Column {
  name: string;
  type: string;
  primary_key?: boolean;
  nullable?: boolean;
  foreign_key?: string;
}

export interface TableSchema {
  table_name: string;
  columns: Column[];
}
