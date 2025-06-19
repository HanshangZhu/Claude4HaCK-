#!/usr/bin/env python3
"""
Interactive Demo of Drug Repositioning Agent
This demonstrates the complete workflow execution with dry-run capabilities.
"""

import sys
import argparse
from drug_repositioning_agent import (
    create_drug_repositioning_graph, 
    DRY_RUN, DEBUG, 
    get_mock_molecular_analysis, 
    get_mock_drug_candidates
)
from langchain_core.messages import HumanMessage, AIMessage

def simulate_complete_workflow(debug=False, dry_run=False):
    """Simulate a complete workflow execution"""
    
    # Set global flags
    import drug_repositioning_agent
    drug_repositioning_agent.DRY_RUN = dry_run
    drug_repositioning_agent.DEBUG = debug
    
    print("\n" + "="*60)
    print("🎭 DRUG REPOSITIONING AGENT - COMPLETE WORKFLOW DEMO")
    print("="*60)
    
    if dry_run:
        print("🧪 DRY RUN MODE: Using mock data")
    if debug:
        print("🔍 DEBUG MODE: Showing workflow steps")
    
    print("\n" + "="*60)
    print("STEP 1: INITIALIZATION")
    print("="*60)
    
    # Create the agent
    app = create_drug_repositioning_graph()
    
    # Initialize state
    state = {
        "messages": [],
        "user_input": "",
        "disease_or_pathology": "",
        "molecular_markers": {},
        "drug_candidates": [],
        "filtered_candidates": [],
        "sources": []
    }
    
    print("✓ Agent initialized successfully!")
    
    print("\n" + "="*60)
    print("STEP 2: GREETING")
    print("="*60)
    
    # Execute greeting
    result = app.invoke(state)
    greeting_msg = result["messages"][-1].content
    print(f"Assistant: {greeting_msg}")
    
    print("\n" + "="*60)
    print("STEP 3: USER INPUT")
    print("="*60)
    
    # Simulate user input
    user_input = "I'm interested in finding drug repositioning candidates for Leigh Syndrome"
    print(f"User: {user_input}")
    
    # Add user message to state
    result["messages"].append(HumanMessage(content=user_input))
    
    print("\n" + "="*60)
    print("STEP 4: MOLECULAR ANALYSIS")
    print("="*60)
    
    if dry_run:
        # Manual execution for dry run to show each step
        print("🧪 Executing molecular analysis with mock data...")
        
        # Mock molecular analysis for Leigh Syndrome
        from drug_repositioning_agent import MolecularAnalysis
        mock_analysis = MolecularAnalysis(
            disease_name="Leigh Syndrome",
            molecular_markers={
                "genetic_mutations": ["SURF1 gene mutations", "MT-ATP6 gene mutations", "MT-ND genes mutations"],
                "cellular_abnormalities": ["Mitochondrial dysfunction", "Decreased ATP production", "Increased lactate levels"],
                "affected_pathways": ["Oxidative phosphorylation pathway", "Electron transport chain", "Pyruvate metabolism"],
                "protein_expression": ["Reduced Complex I activity", "Decreased Complex IV levels", "Altered ATP synthase expression"],
                "molecular_phenotypes": ["Elevated lactate:pyruvate ratio", "Increased ROS production", "Mitochondrial DNA depletion"]
            },
            sources=["OMIM", "GeneReviews", "Nature Reviews Neurology", "Journal of Medical Genetics"]
        )
        result["disease_or_pathology"] = mock_analysis.disease_name
        result["molecular_markers"] = mock_analysis.molecular_markers
        result["sources"] = mock_analysis.sources
        
        analysis_msg = f"I've analyzed the molecular pathology of {mock_analysis.disease_name}. Key molecular markers include: genetic mutations (SURF1), cellular abnormalities (mitochondrial dysfunction), pathways (oxidative phosphorylation)..."
        result["messages"].append(AIMessage(content=analysis_msg))
        print(f"Assistant: {analysis_msg}")
        
        print(f"\n🔬 Molecular Markers Found:")
        for category, markers in mock_analysis.molecular_markers.items():
            print(f"   {category}: {', '.join(markers)}")
    else:
        print("Would execute molecular analysis with Claude API...")
        return  # Skip further execution without API
    
    print("\n" + "="*60)
    print("STEP 5: DRUG IDENTIFICATION")
    print("="*60)
    
    if dry_run:
        print("🧪 Identifying drug candidates with mock data...")
        
        # Mock drug identification for Leigh Syndrome
        from drug_repositioning_agent import DrugCandidate, DrugCandidateList
        mock_candidates = DrugCandidateList(
            candidates=[
                DrugCandidate(
                    drug_name="Dichloroacetate (DCA)",
                    approval_status="Investigational",
                    current_applications=["Lactic acidosis", "Mitochondrial diseases (clinical trials)"],
                    molecular_rationale="DCA inhibits pyruvate dehydrogenase kinase, activating the pyruvate dehydrogenase complex. Reduces lactate accumulation and improves glucose oxidation.",
                    shared_pathology="Elevated lactate levels and pyruvate metabolism dysfunction"
                ),
                DrugCandidate(
                    drug_name="EPI-743",
                    approval_status="Investigational/Orphan Drug",
                    current_applications=["Mitochondrial diseases", "Friedreich's ataxia"],
                    molecular_rationale="Vitamin E analog that protects respiratory chain complexes from oxidative stress, enhances electron transport.",
                    shared_pathology="Oxidative stress and mitochondrial dysfunction"
                ),
                DrugCandidate(
                    drug_name="Idebenone",
                    approval_status="EU Approved for Friedreich's ataxia",
                    current_applications=["Friedreich's ataxia", "Leber's hereditary optic neuropathy"],
                    molecular_rationale="Synthetic CoQ10 analog that acts as electron carrier, bypasses Complex I deficiency, improves ATP production.",
                    shared_pathology="Mitochondrial respiratory chain dysfunction and Complex I deficiency"
                )
            ]
        )
        candidates = [
            {
                "drug_name": c.drug_name,
                "approval_status": c.approval_status,
                "current_applications": ", ".join(c.current_applications),
                "molecular_rationale": c.molecular_rationale,
                "shared_pathology": c.shared_pathology
            }
            for c in mock_candidates.candidates
        ]
        
        result["drug_candidates"] = candidates
        
        summary = f"I've identified {len(candidates)} potential drug repositioning candidates for {result['disease_or_pathology']}:\n\n"
        for i, candidate in enumerate(candidates, 1):
            summary += f"{i}. **{candidate['drug_name']}**\n"
            summary += f"   - Approval Status: {candidate['approval_status']}\n"
            summary += f"   - Current Uses: {candidate['current_applications']}\n"
            summary += f"   - Rationale: {candidate['molecular_rationale']}\n\n"
        
        result["messages"].append(AIMessage(content=summary))
        print(f"Assistant: {summary}")
    
    print("\n" + "="*60)
    print("STEP 6: DRUG FILTERING")
    print("="*60)
    
    if dry_run:
        print("🧪 Filtering drug candidates...")
        
        # Mock filtering (remove last candidate as demo)
        filtered = candidates[:-1]
        result["filtered_candidates"] = filtered
        
        filter_msg = f"After filtering, {len(filtered)} candidates remain suitable for repositioning (removed 1 drug already in use)."
        result["messages"].append(AIMessage(content=filter_msg))
        print(f"Assistant: {filter_msg}")
    
    print("\n" + "="*60)
    print("STEP 7: FINAL RESULTS")
    print("="*60)
    
    if result.get("filtered_candidates"):
        print("🎯 FINAL REPOSITIONING CANDIDATES:")
        print("-" * 40)
        
        for i, candidate in enumerate(result["filtered_candidates"], 1):
            print(f"\n{i}. {candidate['drug_name']}")
            print(f"   Status: {candidate['approval_status']}")
            print(f"   Current Uses: {candidate['current_applications']}")
            print(f"   Molecular Rationale: {candidate['molecular_rationale']}")
            print(f"   Shared Pathology: {candidate['shared_pathology']}")
    
    print("\n" + "="*60)
    print("WORKFLOW COMPLETE!")
    print("="*60)
    
    return result

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Interactive Drug Repositioning Agent Demo")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Run in dry-run mode with mock data")
    parser.add_argument("--debug", action="store_true", 
                       help="Enable debug mode")
    
    args = parser.parse_args()
    
    try:
        result = simulate_complete_workflow(debug=args.debug, dry_run=args.dry_run)
        
        if not args.dry_run:
            print("\n" + "⚠️  " * 20)
            print("NOTE: Full execution requires Anthropic API key")
            print("Run with --dry-run flag to see complete workflow")
            print("⚠️  " * 20)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 