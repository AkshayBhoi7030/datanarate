from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from io import BytesIO
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

app = FastAPI(title="DataNarrate API", debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {
        "success": True,
        "data": {
            "status": "healthy",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat()
        },
        "message": "Service is healthy"
    }

@app.get("/status")
async def status():
    return {
        "success": True,
        "data": {
            "database": "healthy",
            "redis": "healthy",
            "overall": "healthy"
        }
    }

@app.get("/api/v1/history")
async def history():
    return {"success": True, "data": [], "total": 0, "page": 1, "page_size": 20}

@app.post("/api/v1/history")
async def create_history(request: Request):
    return {"success": True, "data": {}}

@app.delete("/api/v1/history/{id}")
async def delete_history(id: str):
    return {"success": True}

@app.get("/api/v1/saved-queries")
async def saved_queries():
    return {"success": True, "data": [], "total": 0, "page": 1, "page_size": 20}

@app.post("/api/v1/saved-queries")
async def create_saved_query(request: Request):
    return {"success": True, "data": {}}

@app.put("/api/v1/saved-queries/{id}")
async def update_saved_query(id: str, request: Request):
    return {"success": True, "data": {}}

@app.delete("/api/v1/saved-queries/{id}")
async def delete_saved_query(id: str):
    return {"success": True}

@app.patch("/api/v1/saved-queries/{id}/favorite")
async def toggle_favorite(id: str):
    return {"success": True, "data": {}}

@app.post("/api/v1/query")
async def query(request: Request):
    body = await request.json()
    question = body.get("question", "demo")
    return {
        "success": True,
        "data": {
            "question": question,
            "sql": "SELECT * FROM demo_table",
            "data": [
                {"id": 1, "name": "Demo Data 1", "value": 100},
                {"id": 2, "name": "Demo Data 2", "value": 200}
            ],
            "insight": f"Based on your question: '{question}', here are the results!"
        },
        "message": "Query executed successfully"
    }

@app.post("/api/v1/exports/csv")
async def export_csv(request: Request):
    body = await request.json()
    data = body.get("data", [])
    filename = body.get("filename", "export.csv")
    df = pd.DataFrame(data)
    output = BytesIO()
    df.to_csv(output, index=False, encoding="utf-8")
    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.post("/api/v1/exports/excel")
async def export_excel(request: Request):
    body = await request.json()
    data = body.get("data", [])
    filename = body.get("filename", "export.xlsx")
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
    output.seek(0)
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.post("/api/v1/exports/pdf")
async def export_pdf(request: Request):
    body = await request.json()
    data = body.get("data", [])
    question = body.get("question", "")
    sql = body.get("sql", "")
    insight = body.get("insight", "")
    filename = body.get("filename", "report.pdf")
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("DataNarrate Report", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Question", styles["Heading2"]))
    story.append(Paragraph(question, styles["BodyText"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Generated SQL", styles["Heading2"]))
    story.append(Paragraph(sql, styles["Code"] if "Code" in styles else styles["BodyText"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("AI Insights", styles["Heading2"]))
    story.append(Paragraph(insight, styles["BodyText"]))
    story.append(Spacer(1, 12))
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
    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.get("/api/v1/preferences")
async def get_preferences():
    return {"success": True, "data": {"theme": "light", "language": "en"}}

@app.get("/api/v1/schema")
async def get_schema():
    return {
        "success": True,
        "data": [
            {
                "table_name": "customers",
                "columns": [
                    {"name": "id", "type": "integer", "primary_key": True},
                    {"name": "name", "type": "varchar", "nullable": False},
                    {"name": "email", "type": "varchar", "nullable": False},
                    {"name": "created_at", "type": "timestamp", "nullable": False}
                ]
            },
            {
                "table_name": "orders",
                "columns": [
                    {"name": "id", "type": "integer", "primary_key": True},
                    {"name": "customer_id", "type": "integer", "foreign_key": "customers.id"},
                    {"name": "total", "type": "decimal", "nullable": False},
                    {"name": "status", "type": "varchar", "nullable": False},
                    {"name": "created_at", "type": "timestamp", "nullable": False}
                ]
            },
            {
                "table_name": "products",
                "columns": [
                    {"name": "id", "type": "integer", "primary_key": True},
                    {"name": "name", "type": "varchar", "nullable": False},
                    {"name": "price", "type": "decimal", "nullable": False},
                    {"name": "stock", "type": "integer", "nullable": False}
                ]
            },
            {
                "table_name": "order_items",
                "columns": [
                    {"name": "id", "type": "integer", "primary_key": True},
                    {"name": "order_id", "type": "integer", "foreign_key": "orders.id"},
                    {"name": "product_id", "type": "integer", "foreign_key": "products.id"},
                    {"name": "quantity", "type": "integer", "nullable": False},
                    {"name": "price", "type": "decimal", "nullable": False}
                ]
            }
        ]
    }

@app.put("/api/v1/preferences")
async def update_preferences(request: Request):
    return {"success": True, "data": {}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_simple_working:app", host="0.0.0.0", port=8000, reload=True)
