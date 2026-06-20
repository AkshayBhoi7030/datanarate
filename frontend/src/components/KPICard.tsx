import React from 'react';
import { Card, CardContent } from '../components/ui/card';
import { cn } from '../utils';

interface KPICardProps {
  title: string;
  value: string | number;
  icon?: React.ReactNode;
  trend?: 'up' | 'down' | 'neutral';
  trendValue?: string;
  color?: 'blue' | 'green' | 'yellow' | 'purple' | 'red';
}

const colorStyles = {
  blue: 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400',
  green: 'bg-green-50 text-green-600 dark:bg-green-900/20 dark:text-green-400',
  yellow: 'bg-yellow-50 text-yellow-600 dark:bg-yellow-900/20 dark:text-yellow-400',
  purple: 'bg-purple-50 text-purple-600 dark:bg-purple-900/20 dark:text-purple-400',
  red: 'bg-red-50 text-red-600 dark:bg-red-900/20 dark:text-red-400',
};

export function KPICard({ title, value, icon, trend, trendValue, color = 'blue' }: KPICardProps) {
  return (
    <Card className="h-full">
      <CardContent className="p-6">
        <div className="flex items-start justify-between">
          <div>
            <p className="text-sm font-medium text-gray-500 dark:text-gray-400">{title}</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-gray-100 mt-2">{value}</p>
            {trend && trendValue && (
              <div
                className={cn(
                  'mt-2 inline-flex items-center text-sm',
                  trend === 'up' ? 'text-green-600 dark:text-green-400' :
                  trend === 'down' ? 'text-red-600 dark:text-red-400' : 'text-gray-600 dark:text-gray-400'
                )}
              >
                {trendValue}
              </div>
            )}
          </div>
          {icon && (
            <div className={cn('p-3 rounded-lg', colorStyles[color])}>{icon}</div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
