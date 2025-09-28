import os
import sys
import json
import requests
from django.urls import reverse

def test_endpoints():
    base_url = "http://localhost:8000"
    
    print("=== Testing API Endpoints ===\n")
    
    # 1. Test Home Page
    print("1. Testing Home Page (GET /)")
    try:
        response = requests.get(f"{base_url}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response Length: {len(response.text)} characters")
        print()
    except Exception as e:
        print(f"Error: {e}")
    
    # 2. Test Process Quiz (POST /api/quiz/test-lesson/)
    print("2. Testing Process Quiz (POST /api/quiz/test-lesson/)")
    try:
        quiz_data = {
            'answers': json.dumps({
                '1': 'a',
                '2': 'b',
                '3': 'c'
            })
        }
        response = requests.post(
            f"{base_url}/api/quiz/test-lesson/",
            json=quiz_data
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}..." if len(response.text) > 200 else response.text)
        print()
    except Exception as e:
        print(f"Error: {e}")
    
    # 3. Test Generate Audio (GET /api/generate-audio/1/)
    print("3. Testing Generate Audio (GET /api/generate-audio/1/)")
    try:
        response = requests.get(f"{base_url}/api/generate-audio/1/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}..." if len(response.text) > 200 else response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_endpoints()
