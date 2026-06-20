import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Database, Table, Key, Link2 } from 'lucide-react';
import { schemaAPI } from '../services/api';

export function SchemaExplorer() {
  const [selectedTable, setSelectedTable] = useState<string | null>(null);

  const { data: schemaData, isLoading } = useQuery({
    queryKey: ['schema'],
    queryFn: () => schemaAPI.getSchema(),
  });

  const tables = schemaData?.data || [];

  if (isLoading) {
    return (
      <div className="max-w-6xl mx-auto space-y-6">
        <h1 className="text-3xl font-bold mb-6">Schema Explorer</h1>
        <div className="space-y-4">
          <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
          <div className="h-32 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
        </div>
      </div>
    );
  }

  const selectedTableData = selectedTable
    ? tables.find(t => t.table_name === selectedTable)
    : null;

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="flex items-center gap-2 mb-6">
        <Database size={28} />
        <h1 className="text-3xl font-bold">Schema Explorer</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <div className="p-4 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
            <h2 className="font-semibold text-lg mb-4 flex items-center gap-2">
              <Table size={18} />
              Tables
            </h2>
            <div className="space-y-2">
              {tables.map((table) => (
                <button
                  key={table.table_name}
                  onClick={() => setSelectedTable(table.table_name)}
                  className={`w-full text-left px-3 py-2 rounded-lg transition-colors ${selectedTable === table.table_name
                    ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400'
                    : 'hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-300'
                    }`}
                >
                  {table.table_name}
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="lg:col-span-2">
          {selectedTableData ? (
            <div className="p-4 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
              <h2 className="text-2xl font-bold mb-6">{selectedTableData.table_name}</h2>
              <div className="overflow-x-auto">
                <table className="w-full border-collapse">
                  <thead>
                    <tr className="border-b border-gray-200 dark:border-gray-700">
                      <th className="text-left py-3 px-4 font-semibold">Column</th>
                      <th className="text-left py-3 px-4 font-semibold">Type</th>
                      <th className="text-left py-3 px-4 font-semibold">Constraints</th>
                    </tr>
                  </thead>
                  <tbody>
                    {selectedTableData.columns.map((col) => (
                      <tr key={col.name} className="border-b border-gray-100 dark:border-gray-800">
                        <td className="py-3 px-4 font-mono text-sm">{col.name}</td>
                        <td className="py-3 px-4 text-sm text-gray-600 dark:text-gray-400">{col.type}</td>
                        <td className="py-3 px-4">
                          <div className="flex flex-wrap gap-2">
                            {col.primary_key && (
                              <span className="flex items-center gap-1 text-xs bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300 px-2 py-1 rounded-full">
                                <Key size={12} />
                                Primary Key
                              </span>
                            )}
                            {col.foreign_key && (
                              <span className="flex items-center gap-1 text-xs bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300 px-2 py-1 rounded-full">
                                <Link2 size={12} />
                                {col.foreign_key}
                              </span>
                            )}
                            {!col.nullable && !col.primary_key && (
                              <span className="text-xs bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300 px-2 py-1 rounded-full">
                                Not Null
                              </span>
                            )}
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          ) : (
            <div className="p-8 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 text-center">
              <Table className="mx-auto h-16 w-16 text-gray-400 mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">Select a table</h3>
              <p className="text-gray-500 dark:text-gray-400">Choose a table from the left to view its schema</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
