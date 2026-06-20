
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Sparkles } from 'lucide-react';

interface InsightPanelProps {
  insight: string;
}

export function InsightPanel({ insight }: InsightPanelProps) {
  const renderInsight = () => {
    if (!insight) return null;

    const lines = insight.split('\n');
    return lines.map((line, idx) => {
      if (line.startsWith('### ')) {
        return (
          <h3 key={idx} className="text-lg font-bold text-gray-900 dark:text-gray-100 mt-4 mb-2 first:mt-0">
            {line.slice(4)}
          </h3>
        );
      } else if (line.startsWith('• ')) {
        return (
          <li key={idx} className="ml-4 text-gray-700 dark:text-gray-300 mb-1">
            {line.slice(2)}
          </li>
        );
      } else if (line.trim()) {
        return (
          <p key={idx} className="text-gray-700 dark:text-gray-300 mb-2">
            {line}
          </p>
        );
      }
      return null;
    });
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Sparkles className="text-yellow-500" size={20} />
          AI Insights
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-2 max-h-80 overflow-y-auto">
        {insight ? (
          <div className="space-y-1">
            {renderInsight()}
          </div>
        ) : (
          <p className="text-gray-500">No insights available yet</p>
        )}
      </CardContent>
    </Card>
  );
}
