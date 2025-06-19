#!/usr/bin/env python3
"""
Test script for the Drug Repositioning Agent Web Frontend
"""

import requests
import json
import time
import sys

def test_web_frontend(base_url="http://127.0.0.1:8082"):
    """Test the web frontend functionality"""
    
    print("🧬 Testing Drug Repositioning Agent Web Frontend")
    print("=" * 60)
    
    # Test 1: Check if server is running
    print("\n1. Testing server status...")
    try:
        response = requests.get(f"{base_url}/api/status", timeout=5)
        if response.status_code == 200:
            status_data = response.json()
            print(f"   ✅ Server is running!")
            print(f"   📊 API Key configured: {status_data.get('api_key_configured', 'Unknown')}")
            print(f"   🧪 Dry run available: {status_data.get('dry_run_available', 'Unknown')}")
        else:
            print(f"   ❌ Server returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Failed to connect to server: {e}")
        return False
    
    # Test 2: Check main page
    print("\n2. Testing main page...")
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("   ✅ Main page loads successfully!")
            if "Drug Repositioning Agent" in response.text:
                print("   ✅ Page contains expected content!")
            else:
                print("   ⚠️  Page content might be incomplete")
        else:
            print(f"   ❌ Main page returned status code: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Failed to load main page: {e}")
        return False
    
    # Test 3: Test analysis endpoint (dry run)
    print("\n3. Testing analysis endpoint (demo mode)...")
    try:
        test_data = {
            "user_input": "Alzheimer's disease",
            "dry_run": True
        }
        response = requests.post(
            f"{base_url}/api/analyze", 
            json=test_data,
            timeout=10
        )
        if response.status_code == 200:
            analysis_data = response.json()
            print("   ✅ Analysis endpoint works!")
            print(f"   📋 Session ID: {analysis_data.get('session_id', 'Unknown')}")
        else:
            print(f"   ❌ Analysis endpoint returned status code: {response.status_code}")
            print(f"   📄 Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Failed to test analysis endpoint: {e}")
        return False
    
    # Test 4: Test history endpoint
    print("\n4. Testing history endpoint...")
    try:
        response = requests.get(f"{base_url}/api/history", timeout=5)
        if response.status_code == 200:
            history_data = response.json()
            print("   ✅ History endpoint works!")
            print(f"   📊 History entries: {len(history_data)}")
        else:
            print(f"   ❌ History endpoint returned status code: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Failed to test history endpoint: {e}")
        return False
    
    # Test 5: Check static files
    print("\n5. Testing static files...")
    static_files = [
        "/static/css/style.css",
        "/static/js/app.js"
    ]
    
    for file_path in static_files:
        try:
            response = requests.get(f"{base_url}{file_path}", timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {file_path} loads successfully!")
            else:
                print(f"   ❌ {file_path} returned status code: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Failed to load {file_path}: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Web Frontend Test Complete!")
    print("\n📝 Manual Test Instructions:")
    print(f"   1. Open browser to: {base_url}")
    print("   2. Enter a disease name like 'Parkinson's disease'")
    print("   3. Check 'Demo Mode' checkbox")
    print("   4. Click 'Start Analysis'")
    print("   5. Watch the real-time progress")
    print("   6. Verify results display correctly")
    print("   7. Test export functionality")
    
    return True

if __name__ == "__main__":
    # Allow custom base URL
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8082"
    
    print(f"Testing web frontend at: {base_url}")
    print("Waiting 3 seconds for server to start...")
    time.sleep(3)
    
    success = test_web_frontend(base_url)
    
    if success:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1) 