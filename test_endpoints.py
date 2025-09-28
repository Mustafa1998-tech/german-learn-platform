import os
import sys
import json
from django.test import Client
from django.urls import reverse

def run_tests():
    # Set up the test client
    client = Client()
    
    print("=== Testing API Endpoints ===\n")
    
    # 1. Test Home Page
    print("1. Testing Home Page (GET /)")
    response = client.get('/')
    print(f"Status Code: {response.status_code}")
    print(f"Template Used: {response.templates[0].name if response.templates else 'No template'}")
    print()
    
    # 2. Test Level List (should be in the home page)
    print("2. Testing Level List (in Home Page)")
    print("Checking if levels are present in the response...")
    print(f"Contains 'Levels' text: {'Levels' in str(response.content)}")
    print()
    
    # 3. Test Process Quiz (POST /api/quiz/<slug:lesson_slug>/)
    print("3. Testing Process Quiz (POST /api/quiz/)")
    # First, we need a valid lesson_slug
    # For testing, we'll use a sample one
    test_lesson_slug = "test-lesson"
    quiz_data = {
        'answers': json.dumps({
            '1': 'a',
            '2': 'b',
            '3': 'c'
        })
    }
    response = client.post(
        f'/api/quiz/{test_lesson_slug}/',
        data=json.dumps(quiz_data),
        content_type='application/json'
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.content.decode('utf-8')}")
    print()
    
    # 4. Test Generate Audio (GET /api/generate-audio/<int:lesson_id>/)
    print("4. Testing Generate Audio (GET /api/generate-audio/)")
    test_lesson_id = 1  # Assuming there's a lesson with ID 1
    response = client.get(f'/api/generate-audio/{test_lesson_id}/')
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.content.decode('utf-8')}")

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "german_learning_platform.settings")
    import django
    django.setup()
    run_tests()
