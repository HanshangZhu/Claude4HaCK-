#!/usr/bin/env python3
"""
Test script to validate the drug repositioning agent setup
"""

import sys

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing package imports...")
    
    required_packages = [
        ("langgraph", "LangGraph"),
        ("langchain_anthropic", "LangChain Anthropic"),
        ("langchain_core", "LangChain Core"),
        ("pydantic", "Pydantic"),
        ("dotenv", "python-dotenv"),
        ("anthropic", "Anthropic")
    ]
    
    all_good = True
    
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"✓ {name} - OK")
        except ImportError as e:
            print(f"✗ {name} - FAILED: {e}")
            all_good = False
    
    return all_good

def test_api_key():
    """Test if API key is configured"""
    print("\nTesting API key configuration...")
    
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if api_key and api_key != "your_api_key_here":
        print("✓ API key configured")
        return True
    else:
        print("✗ API key not configured - please update .env file")
        return False

def test_agent_creation():
    """Test if the agent can be created"""
    print("\nTesting agent creation...")
    
    try:
        from drug_repositioning_agent import create_drug_repositioning_graph
        app = create_drug_repositioning_graph()
        print("✓ Agent created successfully")
        return True
    except Exception as e:
        print(f"✗ Agent creation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("Drug Repositioning Agent - Setup Validation")
    print("="*60)
    
    tests_passed = []
    
    # Test imports
    tests_passed.append(test_imports())
    
    # Only continue if imports work
    if tests_passed[-1]:
        tests_passed.append(test_api_key())
        tests_passed.append(test_agent_creation())
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    if all(tests_passed):
        print("✓ All tests passed! The agent is ready to use.")
        print("\nRun 'python run_agent.py' to start the interactive interface.")
    else:
        print("✗ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 