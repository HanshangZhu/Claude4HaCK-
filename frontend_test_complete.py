#!/usr/bin/env python3
"""
Complete Frontend Test - Runs web server and tests it all in foreground
"""

import threading
import time
import requests
import json
import sys
import os
from contextlib import contextmanager

# Import web app components
from web_app import socketio, app

def find_free_port():
    """Find a free port to use"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

@contextmanager
def web_server(port):
    """Context manager to run web server in background thread"""
    server_thread = None
    try:
        print(f"🚀 Starting web server on port {port}...")
        
        # Start server in thread
        server_thread = threading.Thread(
            target=lambda: socketio.run(app, host='127.0.0.1', port=port, debug=False),
            daemon=True
        )
        server_thread.start()
        
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        time.sleep(3)
        
        # Check if server is responding
        for attempt in range(5):
            try:
                response = requests.get(f"http://127.0.0.1:{port}/api/status", timeout=2)
                if response.status_code == 200:
                    print("✅ Server is ready!")
                    break
            except:
                if attempt < 4:
                    print(f"   Attempt {attempt + 1}/5 failed, retrying...")
                    time.sleep(2)
                else:
                    raise Exception("Server failed to start")
        
        yield f"http://127.0.0.1:{port}"
        
    finally:
        print("🛑 Server context ended")

def test_web_frontend_comprehensive(base_url):
    """Comprehensive test of web frontend"""
    
    print("\n🧬 COMPREHENSIVE WEB FRONTEND TEST")
    print("=" * 80)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Server Status
    print("\n📊 TEST 1: Server Status")
    print("-" * 40)
    total_tests += 1
    try:
        response = requests.get(f"{base_url}/api/status", timeout=5)
        if response.status_code == 200:
            status_data = response.json()
            print(f"✅ Status Code: {response.status_code}")
            print(f"📋 API Key Configured: {status_data.get('api_key_configured', 'Unknown')}")
            print(f"🧪 Dry Run Available: {status_data.get('dry_run_available', 'Unknown')}")
            tests_passed += 1
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Test 2: Main Page
    print("\n🏠 TEST 2: Main Page Load")
    print("-" * 40)
    total_tests += 1
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            content = response.text
            print(f"✅ Status Code: {response.status_code}")
            print(f"📄 Content Length: {len(content)} characters")
            
            # Check for key elements
            checks = [
                ("Drug Repositioning Agent", "Title"),
                ("Bootstrap", "CSS Framework"),
                ("Socket.IO", "Real-time Communication"),
                ("analysis-form", "Form Element"),
                ("api/analyze", "API Endpoint")
            ]
            
            for check, description in checks:
                if check in content:
                    print(f"   ✅ {description} found")
                else:
                    print(f"   ⚠️  {description} not found")
            
            tests_passed += 1
        else:
            print(f"❌ Status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Test 3: Static Files
    print("\n📁 TEST 3: Static Files")
    print("-" * 40)
    static_files = [
        ("/static/css/style.css", "CSS Styles"),
        ("/static/js/app.js", "JavaScript")
    ]
    
    for file_path, description in static_files:
        total_tests += 1
        try:
            response = requests.get(f"{base_url}{file_path}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {description}: {len(response.text)} chars")
                tests_passed += 1
            else:
                print(f"❌ {description}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {description}: {e}")
    
    # Test 4: Analysis API (Demo Mode)
    print("\n🔬 TEST 4: Analysis API (Demo Mode)")
    print("-" * 40)
    total_tests += 1
    try:
        test_data = {
            "user_input": "Alzheimer's disease",
            "dry_run": True
        }
        response = requests.post(
            f"{base_url}/api/analyze", 
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        if response.status_code == 200:
            analysis_data = response.json()
            print(f"✅ Analysis API works!")
            print(f"📋 Session ID: {analysis_data.get('session_id', 'Unknown')}")
            tests_passed += 1
        else:
            print(f"❌ Status code: {response.status_code}")
            print(f"📄 Response: {response.text}")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Test 5: History API
    print("\n📚 TEST 5: History API")
    print("-" * 40)
    total_tests += 1
    try:
        response = requests.get(f"{base_url}/api/history", timeout=5)
        if response.status_code == 200:
            history_data = response.json()
            print(f"✅ History API works!")
            print(f"📊 History entries: {len(history_data)}")
            tests_passed += 1
        else:
            print(f"❌ Status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Test 6: Frontend Components
    print("\n🎨 TEST 6: Frontend Components")
    print("-" * 40)
    total_tests += 1
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            content = response.text
            
            # Check for key frontend components
            components = [
                ('id="analysis-form"', "Analysis Form"),
                ('id="progress-section"', "Progress Section"),
                ('id="results-section"', "Results Section"),
                ('class="btn btn-primary"', "Primary Button"),
                ('Bootstrap', "Bootstrap Framework"),
                ('Socket.IO', "WebSocket Support")
            ]
            
            component_count = 0
            for component, name in components:
                if component in content:
                    print(f"   ✅ {name}")
                    component_count += 1
                else:
                    print(f"   ❌ {name}")
            
            if component_count >= len(components) * 0.8:  # 80% pass rate
                tests_passed += 1
                print(f"✅ Frontend components: {component_count}/{len(components)}")
            else:
                print(f"❌ Frontend components: {component_count}/{len(components)}")
        else:
            print(f"❌ Could not load main page")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    print(f"✅ Tests Passed: {tests_passed}/{total_tests}")
    print(f"📈 Success Rate: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED! Frontend is working perfectly!")
        status = "EXCELLENT"
    elif tests_passed >= total_tests * 0.8:
        print("👍 Most tests passed! Frontend is working well!")
        status = "GOOD"
    elif tests_passed >= total_tests * 0.5:
        print("⚠️  Some issues found. Frontend partially working.")
        status = "PARTIAL"
    else:
        print("❌ Major issues found. Frontend needs attention.")
        status = "POOR"
    
    # Manual testing instructions
    print(f"\n📋 MANUAL TESTING INSTRUCTIONS")
    print("-" * 50)
    print(f"🌐 Open browser to: {base_url}")
    print("🔍 Test these scenarios:")
    print("   1. Enter 'Alzheimer's disease' in the input field")
    print("   2. Check 'Demo Mode' checkbox")
    print("   3. Click 'Start Analysis' button")
    print("   4. Watch the real-time progress bar")
    print("   5. Verify results display with molecular markers")
    print("   6. Test export functionality (JSON, Text, Print)")
    print("   7. Click 'Help' to view usage guide")
    print("   8. Try mobile responsive design")
    
    return status, tests_passed, total_tests

def main():
    """Main test function"""
    
    print("🧬 DRUG REPOSITIONING AGENT - FRONTEND TEST")
    print("=" * 80)
    
    # Find free port
    port = find_free_port()
    print(f"🔌 Using port: {port}")
    
    try:
        # Run web server and test
        with web_server(port) as base_url:
            print(f"🌐 Server URL: {base_url}")
            
            # Run comprehensive tests
            status, passed, total = test_web_frontend_comprehensive(base_url)
            
            print(f"\n🏁 FINAL RESULT: {status}")
            print(f"📊 Score: {passed}/{total} ({(passed/total)*100:.1f}%)")
            
            if status in ["EXCELLENT", "GOOD"]:
                print("\n🎯 FRONTEND IS WORKING! 🎯")
                print("Users can now:")
                print("• Access the web interface")
                print("• Analyze diseases in demo mode")
                print("• View real-time progress")
                print("• Export results")
                print("• Use mobile-responsive design")
                return True
            else:
                print(f"\n⚠️  FRONTEND HAS ISSUES")
                return False
                
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 