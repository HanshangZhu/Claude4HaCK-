#!/usr/bin/env python3
"""
Interactive Drug Repositioning Agent
This script provides an interactive interface to the drug repositioning agent.
"""

import os
import sys
from drug_repositioning_agent import create_drug_repositioning_graph
from langchain_core.messages import HumanMessage

def check_api_key():
    """Check if the API key is configured"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("Error: ANTHROPIC_API_KEY not configured!")
        print("Please:")
        print("1. Copy env.example to .env")
        print("2. Add your Anthropic API key to the .env file")
        sys.exit(1)
    return True

def main():
    """Main interactive loop"""
    print("\n" + "="*60)
    print("Drug Repositioning Agent - Interactive Mode")
    print("="*60)
    
    # Check API key
    check_api_key()
    
    # Create the agent
    try:
        app = create_drug_repositioning_graph()
        print("✓ Agent initialized successfully!")
    except Exception as e:
        print(f"Error initializing agent: {e}")
        sys.exit(1)
    
    # Initial state
    state = {
        "messages": [],
        "user_input": "",
        "disease_or_pathology": "",
        "molecular_markers": {},
        "drug_candidates": [],
        "filtered_candidates": [],
        "sources": []
    }
    
    # Run initial greeting
    state = app.invoke(state)
    print("\n" + state["messages"][-1].content)
    
    # Interactive loop
    while True:
        print("\n" + "-"*60)
        user_input = input("\nYour input (or 'quit' to exit): ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\nThank you for using the Drug Repositioning Agent!")
            break
        
        if not user_input:
            print("Please provide a disease name or molecular pathology observations.")
            continue
        
        # Add user message
        state["messages"].append(HumanMessage(content=user_input))
        
        try:
            # Process through the agent
            print("\nProcessing your request...\n")
            state = app.invoke(state)
            
            # Display the latest assistant response
            for msg in state["messages"][-2:]:  # Show last exchange
                if hasattr(msg, 'content'):
                    role = "You" if msg.__class__.__name__ == "HumanMessage" else "Assistant"
                    if role == "Assistant":
                        print(f"\n{role}: {msg.content}")
                        
            # If we have drug candidates, show detailed results
            if state.get("filtered_candidates"):
                print("\n" + "="*60)
                print("DETAILED DRUG REPOSITIONING RESULTS")
                print("="*60)
                
                for i, candidate in enumerate(state["filtered_candidates"], 1):
                    print(f"\n{i}. {candidate['drug_name']}")
                    print(f"   Status: {candidate['approval_status']}")
                    print(f"   Current Uses: {candidate['current_applications']}")
                    print(f"   Molecular Rationale: {candidate['molecular_rationale']}")
                    if candidate.get('shared_pathology'):
                        print(f"   Shared Pathology: {candidate['shared_pathology']}")
                    print()
                
        except Exception as e:
            print(f"\nError processing request: {e}")
            print("Please try again with a different input.")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main() 