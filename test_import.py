#!/usr/bin/env python3
"""
Simple test to check if web app components import correctly
"""

try:
    print("🧬 Testing Drug Repositioning Agent Web App Imports")
    print("=" * 60)
    
    print("1. Testing web_app import...")
    from web_app import app, socketio
    print("   ✅ web_app imported successfully!")
    
    print("2. Testing routes...")
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(f"   {rule.rule} -> {rule.endpoint}")
    
    print("   Available routes:")
    for route in routes[:5]:  # Show first 5 routes
        print(route)
    if len(routes) > 5:
        print(f"   ... and {len(routes) - 5} more routes")
    
    print("3. Testing agent import...")
    from web_app import agent
    print("   ✅ Agent imported successfully!")
    
    print("\n✅ All imports successful!")
    print("🎯 Web app is ready to run!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Other error: {e}") 