import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Trash2, Clock, RefreshCw } from 'lucide-react';
import toast from 'react-hot-toast';
import { Button } from '../components/ui/button';
import { QueryHistoryItem } from '../types';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { historyAPI } from '../services/api';

export function History() {
  const queryClient = useQueryClient();
  const [searchTerm, setSearchTerm] = useState('');

  const { data: historyData } = useQuery({
    queryKey: ['history'],
    queryFn: () => historyAPI.getHistory(),
  });

  const queryHistory = historyData?.data || [];

  const filteredHistory = queryHistory.filter(item =>
    item.natural_language_query.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const deleteHistoryItem = async (id: string) => {
    historyAPI.deleteHistory(id).then(() => {
      queryClient.invalidateQueries({ queryKey: ['history'] });
      toast.success('History item deleted!');
    });
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Query History</h1>
      </div>

      <input
        type="text"
        placeholder="Search history..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="w-full px-4 py-2 rounded-lg border border-gray-300 bg-white dark:border-gray-600 dark:bg-gray-800"
      />

      {filteredHistory.length === 0 ? (
        <div className="text-center py-12">
          <Clock className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">No queries yet!</h3>
          <p className="text-gray-500 dark:text-gray-400 mb-4">
            Go to the Dashboard and ask your first question!
          </p>
          <Link to="/">
            <Button>Go to Dashboard</Button>
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredHistory.map((item) => (
            <div key={item.id} className="p-4 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <p className="font-medium text-gray-900 dark:text-gray-100">{item.natural_language_query}</p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    {new Date(item.created_at).toLocaleString()}
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <Link to="/" state={{ question: item.natural_language_query }}>
                    <Button variant="ghost" size="sm">
                      <RefreshCw className="mr-1" size={14} />
                      Rerun
                    </Button>
                  </Link>
                  <Button variant="ghost" size="sm" onClick={() => deleteHistoryItem(item.id)}>
                    <Trash2 className="text-red-500" size={14} />
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
