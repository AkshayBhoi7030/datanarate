export interface SavedQuery {
  id: string;
  name: string;
  question: string;
  createdAt: string;
  isFavorite: boolean;
}

export interface QueryHistoryItem {
  id: string;
  question: string;
  sql: string;
  timestamp: string;
  success: boolean;
}
