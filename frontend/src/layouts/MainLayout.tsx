import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Settings,
  Database,
  History,
  Sun,
  Moon,
  Sparkles,
} from 'lucide-react';
import { useTheme } from '../hooks/useTheme';
import { cn } from '../utils';

interface NavItem {
  path: string;
  label: string;
  icon: React.ElementType;
}

const navItems: NavItem[] = [
  {
    path: '/',
    label: 'Dashboard',
    icon: LayoutDashboard,
  },
  {
    path: '/designer',
    label: 'Database Designer',
    icon: Sparkles,
  },
  {
    path: '/schema',
    label: 'Schema Explorer',
    icon: Database,
  },
  {
    path: '/history',
    label: 'History',
    icon: History,
  },
  {
    path: '/settings',
    label: 'Settings',
    icon: Settings,
  },
];

export function MainLayout({ children }: { children: React.ReactNode }) {
  const location = useLocation();
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100">
      <header className="sticky top-0 z-50 border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
        <div className="flex h-16 items-center px-6">
          <Link to="/" className="flex items-center gap-2 font-bold text-xl">
            <div className="h-8 w-8 rounded-lg bg-blue-600 flex items-center justify-center text-white">
              DN
            </div>
            DataNarrate
          </Link>
          <div className="ml-auto flex items-center gap-4">
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
              aria-label="Toggle theme"
            >
              {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
            </button>
          </div>
        </div>
      </header>
      <div className="flex min-h-[calc(100vh-4rem)]">
        <aside className="hidden md:flex w-64 flex-col border-r border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-4">
          <nav className="space-y-1">
            {navItems.map((item) => {
              const isActive = location.pathname === item.path;
              const Icon = item.icon;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={cn(
                    'flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400'
                      : 'text-gray-600 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-800'
                  )}
                >
                  <Icon size={18} />
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </aside>
        <main className="flex-1 p-6 md:p-8">{children}</main>
      </div>
    </div>
  );
}
