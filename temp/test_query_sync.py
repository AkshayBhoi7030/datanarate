
import requests

def test_query():
    url = "http://localhost:8000/api/v1/query"
    payload = {"question": "Show all customers"}
    print("Sending test query...")
    try:
        response = requests.post(url, json=payload, timeout=120)
        print(f"Status: {response.status_code}")
        print(f"Response text: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_query()
