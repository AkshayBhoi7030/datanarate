import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card';
import { Sun, Moon, Settings as SettingsIcon } from 'lucide-react';
import { Button } from '../components/ui/button';
import { useTheme } from '../hooks/useTheme';
import { UserPreferences as UserPreferencesType } from '../types';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { preferencesAPI } from '../services/api';

export function Settings() {
  const { theme, toggleTheme } = useTheme();
  const queryClient = useQueryClient();
  const [localPrefs, setLocalPrefs] = useState({
    theme: 'light',
    defaultChartType: 'bar',
    showInsightsByDefault: true,
  });

  // Fetch preferences from API
  const { data: prefsData } = useQuery({
    queryKey: ['preferences'],
    queryFn: () => preferencesAPI.getPreferences(),
  });

  const updatePrefsMutation = useMutation({
    mutationFn: (newPrefs: Partial<UserPreferencesType>) => preferencesAPI.updatePreferences(newPrefs),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['preferences'] });
    },
  });

  // Update local prefs when API data comes in
  useEffect(() => {
    if (prefsData?.data) {
      setLocalPrefs({
        theme: prefsData.data.theme,
        defaultChartType: prefsData.data.preferred_chart_type,
        showInsightsByDefault: true, // Fallback
      });
    }
  }, [prefsData]);

  const handleUpdateTheme = (newTheme: string) => {
    setLocalPrefs(prev => ({ ...prev, theme: newTheme }));
    updatePrefsMutation.mutate({ theme: newTheme });
    if ((theme === 'dark' && newTheme === 'light') || (theme === 'light' && newTheme === 'dark')) {
      toggleTheme();
    }
  };

  const handleUpdateChartType = (chartType: string) => {
    setLocalPrefs(prev => ({ ...prev, defaultChartType: chartType }));
    updatePrefsMutation.mutate({ preferred_chart_type: chartType });
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="flex items-center gap-2 mb-6">
        <SettingsIcon size={24} />
        <h1 className="text-3xl font-bold">Settings</h1>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Theme</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-700 dark:text-gray-300">
                Current theme: <span className="font-semibold">{localPrefs.theme}</span>
              </p>
            </div>
            <Button
              variant="outline"
              onClick={() => handleUpdateTheme(localPrefs.theme === 'dark' ? 'light' : 'dark')}
            >
              {localPrefs.theme === 'dark' ? <Sun size={18} className="mr-2" /> : <Moon size={18} className="mr-2" />}
              Toggle Theme
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Chart Preferences</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Default Chart Type
              </label>
              <select
                value={localPrefs.defaultChartType}
                onChange={(e) => handleUpdateChartType(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg dark:bg-gray-800 dark:border-gray-600"
              >
                <option value="bar">Bar Chart</option>
                <option value="line">Line Chart</option>
                <option value="pie">Pie Chart</option>
                <option value="doughnut">Doughnut Chart</option>
              </select>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>About</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2 text-gray-700 dark:text-gray-300">
            <p>DataNarrate - AI-Powered Data Analytics</p>
            <p>Version: 1.0.0</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
