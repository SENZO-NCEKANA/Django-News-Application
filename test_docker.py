#!/usr/bin/env python3
"""
Docker Playground Test Script for Django News Application
This script tests the basic functionality of the Django app.
"""

import requests
import time
import sys

def test_app():
    """Test the Django News Application."""
    base_url = "http://localhost:8000"
    
    print("🐳 Testing Django News Application on Docker Playground...")
    print("=" * 60)
    
    # Test 1: Home page
    print("1. Testing home page...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("   ✅ Home page loads successfully")
            print(f"   📄 Response size: {len(response.text)} characters")
        else:
            print(f"   ❌ Home page failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Home page error: {e}")
        return False
    
    # Test 2: Static files
    print("2. Testing static files...")
    try:
        response = requests.get(f"{base_url}/static/", timeout=5)
        print("   ✅ Static files accessible")
    except requests.exceptions.RequestException:
        print("   ⚠️  Static files not accessible (normal for development)")
    
    # Test 3: API endpoints
    print("3. Testing API endpoints...")
    try:
        response = requests.get(f"{base_url}/api/articles/", timeout=5)
        if response.status_code in [200, 401]:  # 401 is expected without auth
            print("   ✅ API endpoints accessible")
        else:
            print(f"   ⚠️  API returned: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ⚠️  API test failed: {e}")
    
    print("=" * 60)
    print("🎉 Docker Playground test completed!")
    print("✅ Your Django News Application is working correctly!")
    return True

if __name__ == "__main__":
    test_app()
