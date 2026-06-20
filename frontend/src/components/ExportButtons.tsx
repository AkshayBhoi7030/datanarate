import React from 'react';
import { Button } from './ui/button';
import { FileSpreadsheet, FileText, FileDown } from 'lucide-react';
import { exportAPI } from '../services/api';

interface ExportButtonsProps {
  data: Array<Record<string, any>>;
  question: string;
  sql: string;
  insight: string;
  filename?: string;
}

export function ExportButtons({ data, question, sql, insight, filename = 'data' }: ExportButtonsProps) {
  const handleCSVExport = async () => {
    await exportAPI.exportCSV(data, `${filename}.csv`);
  };

  const handleExcelExport = async () => {
    await exportAPI.exportExcel(data, `${filename}.xlsx`);
  };

  const handlePDFExport = async () => {
    await exportAPI.exportPDF({
      data,
      question,
      sql,
      insight,
      filename: `${filename}.pdf`,
    });
  };

  if (!data || data.length === 0) return null;

  return (
    <div className="flex gap-2">
      <Button variant="outline" size="sm" onClick={handleCSVExport}>
        <FileText className="mr-2" size={16} />
        CSV
      </Button>
      <Button variant="outline" size="sm" onClick={handleExcelExport}>
        <FileSpreadsheet className="mr-2" size={16} />
        Excel
      </Button>
      <Button variant="outline" size="sm" onClick={handlePDFExport}>
        <FileDown className="mr-2" size={16} />
        PDF
      </Button>
    </div>
  );
}
