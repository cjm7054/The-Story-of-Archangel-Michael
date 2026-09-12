import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TYPECAST_API_KEY")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 1. Test actors list or auth
print("Testing Typecast API Key...")
for endpoint in ["https://typecast.ai/api/actors", "https://api.typecast.ai/v1/actors", "https://typecast.ai/api/models"]:
    try:
        r = requests.get(endpoint, headers=headers, timeout=5)
        print(f"GET {endpoint} -> Status: {r.status_code}")
        if r.status_code == 200:
            print("Response:", r.text[:200])
            break
    except Exception as e:
        print(f"Error {endpoint}: {e}")
