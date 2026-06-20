import React from 'react';
import { cn } from '../../utils';

interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {}

export const Skeleton = ({ className, ...props }: SkeletonProps) => (
  <div
    className={cn(
      'animate-pulse rounded-lg bg-gray-200 dark:bg-gray-700',
      className
    )}
    {...props}
  />
);
