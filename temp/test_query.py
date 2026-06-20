
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import httpx
import asyncio

async def test_query():
    url = "http://localhost:8000/api/v1/query"
    payload = {"question": "Show top 5 customers by revenue"}
    print("Sending test query...")
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(url, json=payload)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_query())
