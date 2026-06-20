import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Send, Save, DollarSign, ShoppingCart, Users, Package } from 'lucide-react';
import toast from 'react-hot-toast';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Skeleton } from '../components/ui/skeleton';
import { SQLPanel } from '../components/SQLPanel';
import { ResultsTable } from '../components/ResultsTable';
import { ChartEngine } from '../components/ChartEngine';
import { InsightPanel } from '../components/InsightPanel';
import { KPICard } from '../components/KPICard';
import { ExportButtons } from '../components/ExportButtons';
import { SavedQueriesSidebar } from '../components/SavedQueriesSidebar';
import { queryAPI, savedQueriesAPI, historyAPI, dashboardAPI } from '../services/api';
import { QueryRequest, QueryResponseData, SavedQuery } from '../types';

export function Dashboard() {
  const location = useLocation();
  const queryClient = useQueryClient();
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState<QueryResponseData | null>(null);
  const [saveQueryName, setSaveQueryName] = useState('');
  const [showSaveModal, setShowSaveModal] = useState(false);

  useEffect(() => {
    if (location.state?.question) {
      setQuestion(location.state.question);
    }
  }, [location.state]);

  const { data: savedQueriesData } = useQuery({
    queryKey: ['savedQueries'],
    queryFn: () => savedQueriesAPI.getSavedQueries(),
  });

  const savedQueries: SavedQuery[] = savedQueriesData?.data || [];

  const { data: dashboardStatsData } = useQuery({
    queryKey: ['dashboardStats'],
    queryFn: () => dashboardAPI.getStats(),
  });

  const mutation = useMutation({
    mutationFn: (request: QueryRequest) => queryAPI.sendQuery(request),
    onSuccess: async (data) => {
      if (data.data) {
        setResponse(data.data);
        await historyAPI.createHistory({
          natural_language_query: question,
          generated_sql: data.data.sql,
          database_connection_id: "550e8400-e29b-41d4-a716-446655440001",
          execution_time_ms: 100,
          row_count: data.data.data.length,
          success: true,
        });
        queryClient.invalidateQueries({ queryKey: ['history'] });
        toast.success('Query completed!');
      }
    },
    onError: (error: any) => {
      // Extract detailed error message
      const errorMessage = error?.response?.data?.detail ||
        error?.message ||
        'Something went wrong. Please try again.';
      toast.error(errorMessage, {
        duration: 5000,
      });
    }
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;
    mutation.mutate({ question });
  };

  const handleLoadQuery = (savedQuestion: string) => {
    setQuestion(savedQuestion);
  };

  const handleSaveQuery = async () => {
    if (!saveQueryName.trim() || !response) return;
    try {
      await savedQueriesAPI.createSavedQuery({
        name: saveQueryName,
        natural_language_query: question,
        generated_sql: response.sql,
        is_favorite: false,
      });
      queryClient.invalidateQueries({ queryKey: ['savedQueries'] });
      setShowSaveModal(false);
      setSaveQueryName('');
      toast.success('Query saved!');
    } catch (error) {
      toast.error('Failed to save query');
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
      <div className="lg:col-span-3 space-y-8">
        <div className="text-center space-y-4 mb-8">
          <h1 className="text-4xl font-bold">Ask Your Data Questions</h1>
          <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Type your question in plain English, and AI will generate SQL, execute it, and give you insights.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <KPICard
            title="Total Revenue"
            value={`$${dashboardStatsData?.data?.total_revenue?.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) || '0.00'}`}
            icon={<DollarSign size={24} />}
            trend="up"
            trendValue="+12.5%"
            color="green"
          />
          <KPICard
            title="Total Orders"
            value={dashboardStatsData?.data?.total_orders?.toLocaleString() || '0'}
            icon={<ShoppingCart size={24} />}
            trend="up"
            trendValue="+8.2%"
            color="blue"
          />
          <KPICard
            title="Total Customers"
            value={dashboardStatsData?.data?.total_customers?.toLocaleString() || '0'}
            icon={<Users size={24} />}
            trend="neutral"
            trendValue="0.0%"
            color="purple"
          />
          <KPICard
            title="Total Products"
            value={dashboardStatsData?.data?.total_products?.toLocaleString() || '0'}
            icon={<Package size={24} />}
            trend="down"
            trendValue="-2.1%"
            color="red"
          />
        </div>

        <form onSubmit={handleSubmit} className="flex gap-3 max-w-3xl mx-auto">
          <Input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="What is your question?"
            className="text-lg"
            disabled={mutation.isPending}
          />
          <Button type="submit" size="lg" disabled={mutation.isPending}>
            {mutation.isPending ? 'Thinking...' : 'Ask'}
            <Send className="ml-2" size={18} />
          </Button>
        </form>

        {mutation.isPending && (
          <div className="space-y-4 mt-8">
            <Skeleton className="h-24 w-full" />
            <Skeleton className="h-48 w-full" />
          </div>
        )}

        {response && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold">Query Results</h2>
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setShowSaveModal(true)}
                >
                  <Save className="mr-2" size={16} />
                  Save
                </Button>
                <ExportButtons
                  data={response.data}
                  question={response.question}
                  sql={response.sql}
                  insight={response.insight}
                  filename={question.toLowerCase().replace(/\s+/g, '-')}
                />
              </div>
            </div>
            <SQLPanel sql={response.sql} />
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 space-y-6">
                <ResultsTable data={response.data} />
              </div>
              <div className="space-y-6">
                <ChartEngine data={response.data} />
                <InsightPanel insight={response.insight} />
              </div>
            </div>
          </div>
        )}

        {showSaveModal && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div className="bg-white dark:bg-gray-900 rounded-xl p-6 w-96 shadow-xl">
              <h3 className="text-lg font-semibold mb-4">Save Query</h3>
              <Input
                value={saveQueryName}
                onChange={(e) => setSaveQueryName(e.target.value)}
                placeholder="Query name..."
                className="mb-4"
              />
              <div className="flex justify-end gap-2">
                <Button variant="ghost" onClick={() => setShowSaveModal(false)}>
                  Cancel
                </Button>
                <Button onClick={handleSaveQuery}>Save</Button>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="lg:col-span-1">
        <SavedQueriesSidebar
          savedQueries={savedQueries}
          onLoadQuery={handleLoadQuery}
          onDeleteQuery={async (id) => {
            await savedQueriesAPI.deleteSavedQuery(id);
            queryClient.invalidateQueries({ queryKey: ['savedQueries'] });
            toast.success('Query deleted!');
          }}
          onToggleFavorite={async (id) => {
            await savedQueriesAPI.toggleFavorite(id);
            queryClient.invalidateQueries({ queryKey: ['savedQueries'] });
          }}
        />
      </div>
    </div>
  );
}
