
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app.executors.safe_sql_executor import SafeSQLExecutor

def test_sql_execution():
    print("Testing SQL executor...")
    executor = SafeSQLExecutor()
    
    test_sql = "SELECT COUNT(*) as customer_count FROM customers"
    results = executor.execute(test_sql)
    print("Test query results:", results)
    assert len(results) > 0, "Should have at least one result"
    print("✅ SQL executor test passed!")


if __name__ == "__main__":
    test_sql_execution()

