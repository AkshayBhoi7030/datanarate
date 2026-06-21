import { createBrowserRouter } from 'react-router-dom';
import { MainLayout } from '../layouts/MainLayout';
import { Dashboard } from '../pages/Dashboard';
import { SchemaExplorer } from '../pages/SchemaExplorer';
import { History } from '../pages/History';
import { Settings } from '../pages/Settings';
import { DatabaseDesigner } from '../pages/DatabaseDesigner';

export const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <MainLayout>
        <Dashboard />
      </MainLayout>
    ),
  },
  {
    path: '/designer',
    element: (
      <MainLayout>
        <DatabaseDesigner />
      </MainLayout>
    ),
  },
  {
    path: '/schema',
    element: (
      <MainLayout>
        <SchemaExplorer />
      </MainLayout>
    ),
  },
  {
    path: '/history',
    element: (
      <MainLayout>
        <History />
      </MainLayout>
    ),
  },
  {
    path: '/settings',
    element: (
      <MainLayout>
        <Settings />
      </MainLayout>
    ),
  },
]);
