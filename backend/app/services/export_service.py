from io import BytesIO
from typing import List, Dict
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from app.core.logging import logger


class ExportService:
    def export_csv(self, data: List[Dict], filename: str = "export.csv"):
        logger.debug(f"Exporting {len(data)} rows to CSV")
        df = pd.DataFrame(data)
        output = BytesIO()
        df.to_csv(output, index=False, encoding="utf-8")
        output.seek(0)
        return output, filename

    def export_excel(self, data: List[Dict], filename: str = "export.xlsx"):
        logger.debug(f"Exporting {len(data)} rows to Excel")
        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Data")
        output.seek(0)
        return output, filename

    def export_pdf(self, data: List[Dict], question: str, sql: str, insight: str, filename: str = "report.pdf"):
        logger.debug(f"Exporting report to PDF")
        output = BytesIO()
        doc = SimpleDocTemplate(output, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Title
        story.append(Paragraph("DataNarrate Report", styles["Title"]))
        story.append(Spacer(1, 12))

        # Question
        story.append(Paragraph("Question", styles["Heading2"]))
        story.append(Paragraph(question, styles["BodyText"]))
        story.append(Spacer(1, 12))

        # SQL
        story.append(Paragraph("Generated SQL", styles["Heading2"]))
        story.append(Paragraph(sql, styles["Code"]))
        story.append(Spacer(1, 12))

        # Insights
        story.append(Paragraph("AI Insights", styles["Heading2"]))
        story.append(Paragraph(insight, styles["BodyText"]))
        story.append(Spacer(1, 12))

        # Data Table
        if data:
            story.append(Paragraph("Results", styles["Heading2"]))
            df = pd.DataFrame(data)
            table_data = [df.columns.tolist()] + df.values.tolist()
            table = Table(table_data)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]))
            story.append(table)

        doc.build(story)
        output.seek(0)
        return output, filename
