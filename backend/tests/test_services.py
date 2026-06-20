import pytest
from app.services.export_service import ExportService


def test_export_csv():
    service = ExportService()
    data = [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]
    output, filename = service.export_csv(data, "test.csv")
    assert output.getvalue() is not None
    assert filename == "test.csv"


def test_export_excel():
    service = ExportService()
    data = [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]
    output, filename = service.export_excel(data, "test.xlsx")
    assert output.getvalue() is not None
    assert filename == "test.xlsx"


def test_export_pdf():
    service = ExportService()
    data = [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]
    output, filename = service.export_pdf(
        data,
        "Who are our users?",
        "SELECT * FROM users",
        "We have 2 users.",
        "test.pdf"
    )
    assert output.getvalue() is not None
    assert filename == "test.pdf"


def test_export_csv_empty_data():
    service = ExportService()
    data = []
    output, filename = service.export_csv(data, "empty.csv")
    assert output.getvalue() is not None
    assert filename == "empty.csv"


def test_export_excel_empty_data():
    service = ExportService()
    data = []
    output, filename = service.export_excel(data, "empty.xlsx")
    assert output.getvalue() is not None
    assert filename == "empty.xlsx"


def test_export_pdf_empty_data():
    service = ExportService()
    data = []
    output, filename = service.export_pdf(
        data,
        "Who are our users?",
        "SELECT * FROM users",
        "No users found.",
        "empty.pdf"
    )
    assert output.getvalue() is not None
    assert filename == "empty.pdf"
