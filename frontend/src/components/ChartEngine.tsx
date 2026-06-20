
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Bar, Line, Pie, Scatter } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

interface ChartEngineProps {
  data: Array<Record<string, any>>;
}

const colors = [
  '#3b82f6',
  '#10b981',
  '#f59e0b',
  '#ef4444',
  '#8b5cf6',
  '#ec4899',
  '#06b6d4',
  '#14b8a6',
  '#f97316',
  '#84cc16',
];

type ColumnType = 'numeric' | 'date' | 'category';

function detectColumnType(values: any[]): ColumnType {
  if (!values || values.length === 0) return 'category';

  // Check if date
  const dateCount = values.filter(v => {
    if (v == null) return false;
    const str = String(v);
    return !isNaN(Date.parse(str)) && str.length >= 4;
  }).length;
  if (dateCount / values.length > 0.7) return 'date';

  // Check if numeric
  const numericCount = values.filter(v => {
    if (v == null) return false;
    const num = Number(v);
    return !isNaN(num) && isFinite(num);
  }).length;
  if (numericCount / values.length > 0.7) return 'numeric';

  return 'category';
}

function cleanValue(value: any, type: ColumnType): any {
  if (value == null) return null;

  if (type === 'numeric') {
    const num = Number(value);
    return !isNaN(num) && isFinite(num) ? num : null;
  }

  if (type === 'date') {
    const date = new Date(value);
    return !isNaN(date.getTime()) ? date : null;
  }

  return String(value);
}

export function ChartEngine({ data = [] }: ChartEngineProps) {
  if (!data || data.length === 0) {
    return (
      <Card className="h-80">
        <CardHeader>
          <CardTitle>Chart</CardTitle>
        </CardHeader>
        <CardContent className="h-56 flex items-center justify-center">
          <p className="text-gray-500">No data to visualize</p>
        </CardContent>
      </Card>
    );
  }

  const keys = Object.keys(data[0]);
  if (keys.length < 2) {
    return (
      <Card className="h-80">
        <CardHeader>
          <CardTitle>Chart</CardTitle>
        </CardHeader>
        <CardContent className="h-56 flex items-center justify-center">
          <p className="text-gray-500">Need at least 2 columns for chart</p>
        </CardContent>
      </Card>
    );
  }

  // Analyze column types
  const columnTypes: Record<string, ColumnType> = {};
  const cleanedData: Array<Record<string, any>> = [];

  keys.forEach(key => {
    columnTypes[key] = detectColumnType(data.map(row => row[key]));
  });

  data.forEach(row => {
    const cleaned: Record<string, any> = {};
    keys.forEach(key => {
      cleaned[key] = cleanValue(row[key], columnTypes[key]);
    });
    cleanedData.push(cleaned);
  });

  // Filter out rows where both label and value are null
  const validData = cleanedData.filter(row => {
    const hasLabel = row[keys[0]] != null;
    const hasValue = keys.some((k, i) => i > 0 && row[k] != null);
    return hasLabel && hasValue;
  });

  if (validData.length === 0) {
    return (
      <Card className="h-80">
        <CardHeader>
          <CardTitle>Chart</CardTitle>
        </CardHeader>
        <CardContent className="h-56 flex items-center justify-center">
          <p className="text-gray-500">No valid data points to visualize</p>
        </CardContent>
      </Card>
    );
  }

  // Select label and value columns
  const numericKeys = keys.filter(k => columnTypes[k] === 'numeric');
  const dateKeys = keys.filter(k => columnTypes[k] === 'date');

  let labelKey = keys[0];
  let valueKeys = numericKeys.length > 0 ? numericKeys : [keys[1]];

  if (dateKeys.length > 0 && numericKeys.length > 0) {
    labelKey = dateKeys[0];
    valueKeys = numericKeys;
  } else if (numericKeys.length === 0) {
    valueKeys = [keys[1]];
  }

  // Prepare chart data
  let chartLabels: string[] = [];
  const datasets: any[] = [];

  // Sort data by label or value
  let sortedData = [...validData];
  if (columnTypes[labelKey] === 'date') {
    sortedData.sort((a, b) => {
      const dateA = new Date(a[labelKey]);
      const dateB = new Date(b[labelKey]);
      return dateA.getTime() - dateB.getTime();
    });
  } else if (valueKeys.length > 0) {
    sortedData.sort((a, b) => {
      const valA = Number(a[valueKeys[0]]) || 0;
      const valB = Number(b[valueKeys[0]]) || 0;
      return valB - valA;
    });
  }

  // Take top 10 if data is large
  const displayData = sortedData.length > 10 ? sortedData.slice(0, 10) : sortedData;

  chartLabels = displayData.map(row => {
    if (columnTypes[labelKey] === 'date') {
      const date = new Date(row[labelKey]);
      return date.toLocaleDateString();
    }
    return String(row[labelKey]);
  });

  valueKeys.forEach((valueKey) => {
    const chartData = displayData.map(row => Number(row[valueKey]) || 0);
    datasets.push({
      label: valueKey,
      data: chartData,
      backgroundColor: colors.map(c => c + 'cc'),
      borderColor: colors,
      borderWidth: 2,
      pointRadius: 4,
      pointHoverRadius: 6,
      fill: false,
    });
  });

  // Determine chart type
  let chartType: 'bar' | 'line' | 'pie' | 'scatter' = 'bar';
  const uniqueLabels = new Set(chartLabels).size;

  if (columnTypes[labelKey] === 'date' && valueKeys.some(k => columnTypes[k] === 'numeric')) {
    chartType = 'line';
  } else if (uniqueLabels <= 6 && datasets.length === 1) {
    chartType = 'pie';
  } else if (valueKeys.length >= 2 && columnTypes[valueKeys[0]] === 'numeric' && columnTypes[valueKeys[1]] === 'numeric') {
    chartType = 'scatter';
  }

  // Configure chart
  const chartConfig: any = {
    labels: chartLabels,
    datasets: datasets,
  };

  if (chartType === 'scatter') {
    chartConfig.datasets = [
      {
        label: `${valueKeys[0]} vs ${valueKeys[1]}`,
        data: displayData.map(row => ({
          x: Number(row[valueKeys[0]]) || 0,
          y: Number(row[valueKeys[1]]) || 0,
        })),
        backgroundColor: colors[0] + 'cc',
        borderColor: colors[0],
        borderWidth: 2,
        pointRadius: 6,
        pointHoverRadius: 8,
      }
    ];
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: {
          padding: 20,
          usePointStyle: true,
        },
      },
      tooltip: {
        backgroundColor: 'rgba(0,0,0,0.8)',
        padding: 12,
        titleFont: { size: 14 },
        bodyFont: { size: 12 },
      },
    },
    scales: {
      x: {
        ticks: {
          maxRotation: 45,
          minRotation: 0,
          autoSkip: true,
        },
      },
      y: {
        beginAtZero: true,
      },
    },
  };

  return (
    <Card className="h-80">
      <CardHeader>
        <CardTitle>Visualization</CardTitle>
      </CardHeader>
      <CardContent className="h-56">
        {chartType === 'bar' && <Bar data={chartConfig} options={options} />}
        {chartType === 'line' && <Line data={chartConfig} options={{ ...options, scales: { x: { ticks: { maxRotation: 45 } } } }} />}
        {chartType === 'pie' && <Pie data={chartConfig} options={{ ...options, scales: undefined }} />}
        {chartType === 'scatter' && <Scatter data={chartConfig} options={options} />}
      </CardContent>
    </Card>
  );
}
