import React, { useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus, vs } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Copy, Check, ChevronDown, ChevronUp } from 'lucide-react';
import { Button } from './ui/button';
import { useTheme } from '../hooks/useTheme';
import { copyToClipboard } from '../utils';

interface SQLPanelProps {
  sql: string;
}

export function SQLPanel({ sql }: SQLPanelProps) {
  const { theme } = useTheme();
  const [collapsed, setCollapsed] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    copyToClipboard(sql);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 bg-gray-50 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
        <h3 className="font-semibold text-gray-900 dark:text-gray-100">Generated SQL</h3>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" onClick={handleCopy}>
            {copied ? <Check size={16} className="text-green-500" /> : <Copy size={16} />}
            {copied ? 'Copied' : 'Copy'}
          </Button>
          <button
            onClick={() => setCollapsed(!collapsed)}
            className="p-1 rounded hover:bg-gray-200 dark:hover:bg-gray-700"
          >
            {collapsed ? <ChevronDown size={18} /> : <ChevronUp size={18} />}
          </button>
        </div>
      </div>
      {!collapsed && (
        <div className="overflow-x-auto">
          <SyntaxHighlighter
            language="sql"
            style={theme === 'dark' ? vscDarkPlus : vs}
            customStyle={{ margin: 0, fontSize: '0.875rem' }}
          >
            {sql}
          </SyntaxHighlighter>
        </div>
      )}
    </div>
  );
}
