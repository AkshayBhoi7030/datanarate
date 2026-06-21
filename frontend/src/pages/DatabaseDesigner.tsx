import React, { useState } from 'react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Layout, Database, Sparkles, FileCode, BarChart3, CheckCircle, Download, Copy, Eraser } from 'lucide-react';
import { toast } from 'react-hot-toast';
import axios from 'axios';

export function DatabaseDesigner() {
  const [businessDescription, setBusinessDescription] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [results, setResults] = useState<any>(null);
  const [selectedDatabase, setSelectedDatabase] = useState('all');

  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

  const handleGenerate = async () => {
    if (!businessDescription.trim()) {
      toast.error('Please enter a business description');
      return;
    }

    setIsGenerating(true);
    try {
      const response = await axios.post(`${apiBaseUrl}/designer/generate`, {
        description: businessDescription,
        database_type: selectedDatabase
      });

      if (response.data.success) {
        setResults(response.data.data);
        toast.success('Database design generated!');
      }
    } catch (error) {
      console.error('Error:', error);
      toast.error('Failed to generate database design');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setBusinessDescription('');
    setSelectedDatabase('all');
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast.success('Copied to clipboard!');
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-2">AI Database Designer</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Describe your business in natural language and get a complete database design
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Sparkles className="h-5 w-5" />
            Business Description
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <textarea
            value={businessDescription}
            onChange={(e) => setBusinessDescription(e.target.value)}
            placeholder="e.g., Create a database for an online food delivery platform"
            className="w-full h-32 p-3 border rounded-md bg-white dark:bg-gray-900 border-gray-200 dark:border-gray-800 text-gray-900 dark:text-gray-100"
          />
          <div className="flex items-center gap-4">
            <div className="flex flex-col gap-1 flex-1">
              <label className="text-sm font-medium">Target Database</label>
              <select
                value={selectedDatabase}
                onChange={(e) => setSelectedDatabase(e.target.value)}
                className="p-2 border rounded-md bg-white dark:bg-gray-900 border-gray-200 dark:border-gray-800 text-gray-900 dark:text-gray-100"
              >
                <option value="all">All Databases (SQLite, MySQL, PostgreSQL, Oracle, SQL Server)</option>
                <option value="sqlite">SQLite</option>
                <option value="mysql">MySQL</option>
                <option value="postgresql">PostgreSQL</option>
                <option value="oracle">Oracle</option>
                <option value="sqlserver">SQL Server</option>
              </select>
            </div>
          </div>
          <div className="flex gap-2">
            <Button
              onClick={handleGenerate}
              disabled={isGenerating}
              className="flex-1"
            >
              {isGenerating ? 'Generating...' : 'Generate Database Design'}
            </Button>
            {results && (
              <Button variant="secondary" onClick={handleReset}>
                <Eraser className="h-4 w-4 mr-1" />
                Reset
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      {results && (
        <div className="space-y-6">
          <div className="flex items-center gap-4">
            <Card className="flex-1">
              <CardContent className="p-6">
                <div className="text-center">
                  <CheckCircle className="h-8 w-8 text-green-500 mx-auto mb-2" />
                  <div className="text-2xl font-bold">{results.qualityScore}/100</div>
                  <div className="text-sm text-gray-500">Database Quality Score</div>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Database className="h-5 w-5" />
                  Schema
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {results.schema.map((table: any, idx: number) => (
                    <li key={idx} className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <div className="font-medium">{table.table}</div>
                      <div className="text-sm text-gray-500">{table.columns.join(', ')}</div>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle className="flex items-center gap-2">
                  <FileCode className="h-5 w-5" />
                  SQL Schema
                </CardTitle>
                <Button size="sm" onClick={() => copyToClipboard(results.sql)}>
                  <Copy className="h-4 w-4 mr-1" />
                  Copy
                </Button>
              </CardHeader>
              <CardContent>
                <pre className="bg-gray-900 text-green-400 p-4 rounded-lg text-sm overflow-x-auto">
                  {results.sql}
                </pre>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="h-5 w-5" />
                  Analytics Queries
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {results.analytics.map((query: string, idx: number) => (
                    <li key={idx} className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <pre className="text-sm">{query}</pre>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Layout className="h-5 w-5" />
                  Dashboard KPIs
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {results.kpis.map((kpi: string, idx: number) => (
                    <li key={idx} className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg flex items-center justify-between">
                      <span>{kpi}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </div>

          <div className="flex gap-2">
            <Button>
              <Download className="h-4 w-4 mr-2" />
              Download SQL
            </Button>
            <Button variant="secondary">
              <Download className="h-4 w-4 mr-2" />
              Download Sample Data
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
