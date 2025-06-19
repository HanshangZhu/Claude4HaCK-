#!/usr/bin/env python3
"""
Real-Time Interactive Drug Repositioning Agent
This accepts user input in real-time for any disease or molecular pathology.
"""

import sys
import argparse
from dotenv import load_dotenv
from drug_repositioning_agent import (
    create_drug_repositioning_graph, 
    MolecularAnalysis,
    DrugCandidate,
    DrugCandidateList
)
from langchain_core.messages import HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
import os

# Load environment variables
load_dotenv()

def get_user_input():
    """Get disease or molecular pathology input from user"""
    print("\n" + "="*80)
    print("🧬 DRUG REPOSITIONING AGENT - REAL-TIME ANALYSIS")
    print("="*80)
    
    print("\nWelcome! I can help identify drugs for repositioning based on molecular pathology.")
    print("\nYou can provide either:")
    print("1. A disease name (e.g., 'Parkinson's disease', 'Type 2 diabetes')")
    print("2. Molecular pathology observations (e.g., 'BRCA1 mutations, DNA repair defects')")
    
    while True:
        user_input = input("\n📝 Enter your disease/pathology: ").strip()
        if user_input:
            return user_input
        print("Please enter a valid disease name or molecular pathology description.")

def analyze_disease_realtime(user_input, dry_run=False):
    """Analyze user-provided disease in real-time"""
    
    print(f"\n🔍 Analyzing: {user_input}")
    print("="*80)
    
    if dry_run:
        print("🧪 DRY RUN MODE: Using simulated analysis")
        return simulate_analysis(user_input)
    
    # Initialize Claude
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        temperature=0.3
    )
    
    # Step 1: Molecular Analysis
    print("\n🔬 STEP 1: MOLECULAR PATHOLOGY ANALYSIS")
    print("-" * 60)
    print("Analyzing molecular mechanisms...")
    
    analysis_prompt = ChatPromptTemplate.from_template("""
    You are a molecular pathologist. Analyze the provided input and identify key molecular markers including:
    - Genetic mutations
    - Cellular abnormalities  
    - Affected molecular pathways
    - Protein expression changes
    - Other molecular phenotypes
    
    If a disease name is provided, identify its molecular characteristics.
    If molecular observations are provided, categorize and analyze them.
    
    Provide comprehensive molecular characterization with sources.
    
    Input: {user_input}
    """)
    
    structured_llm = llm.with_structured_output(MolecularAnalysis)
    chain = analysis_prompt | structured_llm
    
    try:
        molecular_analysis = chain.invoke({"user_input": user_input})
        
        print(f"✓ Disease/Condition: {molecular_analysis.disease_name}")
        print(f"✓ Molecular markers identified:")
        for category, markers in molecular_analysis.molecular_markers.items():
            print(f"   • {category}: {', '.join(markers[:3])}{'...' if len(markers) > 3 else ''}")
        
    except Exception as e:
        print(f"❌ Error in molecular analysis: {e}")
        return None
    
    # Step 2: Drug Identification
    print("\n💊 STEP 2: DRUG REPOSITIONING CANDIDATES")
    print("-" * 60)
    print("Identifying potential drug repositioning candidates...")
    
    drug_prompt = ChatPromptTemplate.from_template("""
    You are an expert in drug repositioning and molecular pathology. 
    Based on the molecular markers provided, identify existing drugs that could be repurposed.
    
    Focus on:
    1. Drugs targeting similar molecular pathways
    2. Drugs used for diseases with similar molecular abnormalities
    3. Drugs affecting the same cellular processes
    
    For each candidate, provide:
    - Drug name
    - Current approval status
    - Current applications
    - Detailed molecular rationale for repositioning
    - Specific shared molecular pathology
    
    Disease/Condition: {disease_name}
    Molecular markers: {molecular_markers}
    """)
    
    drug_structured_llm = llm.with_structured_output(DrugCandidateList)
    drug_chain = drug_prompt | drug_structured_llm
    
    try:
        drug_candidates = drug_chain.invoke({
            "disease_name": molecular_analysis.disease_name,
            "molecular_markers": molecular_analysis.molecular_markers
        })
        
        print(f"✓ Found {len(drug_candidates.candidates)} potential candidates:")
        for i, candidate in enumerate(drug_candidates.candidates, 1):
            print(f"   {i}. {candidate.drug_name} ({candidate.approval_status})")
            
    except Exception as e:
        print(f"❌ Error in drug identification: {e}")
        return None
    
    # Step 3: Filtering
    print("\n🔍 STEP 3: FILTERING & VALIDATION")
    print("-" * 60)
    print("Filtering candidates...")
    
    filter_prompt = ChatPromptTemplate.from_template("""
    Review these drug candidates for {disease_name} repositioning:
    
    {candidates}
    
    Remove any drugs that are:
    1. Already approved or in trials for this specific condition
    2. Would not logically help with the identified molecular pathology
    3. Have weak molecular rationale
    
    Return only the most promising candidates with strong scientific rationale.
    Explain your filtering decisions.
    """)
    
    candidates_text = "\n".join([
        f"- {c.drug_name}: {c.molecular_rationale}" 
        for c in drug_candidates.candidates
    ])
    
    try:
        filter_response = llm.invoke(filter_prompt.format_messages(
            disease_name=molecular_analysis.disease_name,
            candidates=candidates_text
        ))
    except Exception as e:
        print(f"❌ Error in filtering: {e}")
        filter_response = None
    
    # Display Results
    display_results(molecular_analysis, drug_candidates, filter_response)
    
    return {
        "molecular_analysis": molecular_analysis,
        "drug_candidates": drug_candidates,
        "filter_analysis": filter_response.content if filter_response else "No filtering performed"
    }

def simulate_analysis(user_input):
    """Simulate analysis for dry run mode"""
    print("\n🧪 SIMULATED ANALYSIS")
    print("-" * 60)
    
    # Create mock data based on user input
    mock_analysis = MolecularAnalysis(
        disease_name=f"Simulated analysis for: {user_input}",
        molecular_markers={
            "example_mutations": ["Mock mutation 1", "Mock mutation 2"],
            "example_pathways": ["Mock pathway 1", "Mock pathway 2"],
            "example_abnormalities": ["Mock abnormality 1", "Mock abnormality 2"]
        },
        sources=["Mock Database", "Simulated Research"]
    )
    
    mock_candidates = DrugCandidateList(
        candidates=[
            DrugCandidate(
                drug_name="Example Drug A",
                approval_status="FDA Approved",
                current_applications=["Condition X", "Condition Y"],
                molecular_rationale="Mock molecular rationale for repositioning",
                shared_pathology="Simulated shared pathology"
            ),
            DrugCandidate(
                drug_name="Example Drug B",
                approval_status="Investigational",
                current_applications=["Condition Z"],
                molecular_rationale="Another mock rationale",
                shared_pathology="Another simulated pathology"
            )
        ]
    )
    
    print(f"✓ Simulated analysis complete for: {user_input}")
    display_results(mock_analysis, mock_candidates, None)
    
    return {
        "molecular_analysis": mock_analysis,
        "drug_candidates": mock_candidates,
        "filter_analysis": "Simulated filtering - this would remove inappropriate candidates"
    }

def display_results(molecular_analysis, drug_candidates, filter_response):
    """Display the analysis results"""
    
    print("\n🎯 ANALYSIS RESULTS")
    print("="*80)
    
    print(f"\n📊 DISEASE/CONDITION: {molecular_analysis.disease_name}")
    print("-" * 50)
    
    print(f"\n🔬 MOLECULAR MARKERS:")
    for category, markers in molecular_analysis.molecular_markers.items():
        print(f"   • {category}: {', '.join(markers)}")
    
    print(f"\n💊 DRUG REPOSITIONING CANDIDATES:")
    print("-" * 50)
    
    for i, candidate in enumerate(drug_candidates.candidates, 1):
        print(f"\n{i}. {candidate.drug_name}")
        print(f"   Status: {candidate.approval_status}")
        print(f"   Current Uses: {', '.join(candidate.current_applications)}")
        print(f"   Molecular Rationale: {candidate.molecular_rationale}")
        print(f"   Shared Pathology: {candidate.shared_pathology}")
    
    if filter_response:
        print(f"\n🔍 FILTERING ANALYSIS:")
        print("-" * 30)
        print(filter_response.content)
    
    print(f"\n📚 SOURCES:")
    print("-" * 20)
    for source in molecular_analysis.sources:
        print(f"• {source}")

def main():
    """Main interactive loop"""
    parser = argparse.ArgumentParser(description="Real-Time Drug Repositioning Agent")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Run in dry-run mode with simulated data")
    
    args = parser.parse_args()
    
    try:
        while True:
            # Get user input
            user_input = get_user_input()
            
            # Analyze
            result = analyze_disease_realtime(user_input, dry_run=args.dry_run)
            
            if result:
                print("\n✅ ANALYSIS COMPLETE!")
                print("="*80)
                
                # Ask if user wants to analyze another condition
                another = input("\n🔄 Would you like to analyze another condition? (y/n): ").strip().lower()
                if another not in ['y', 'yes']:
                    break
            else:
                print("\n❌ Analysis failed. Please try again.")
                retry = input("🔄 Would you like to try again? (y/n): ").strip().lower()
                if retry not in ['y', 'yes']:
                    break
        
        print("\n👋 Thank you for using the Drug Repositioning Agent!")
        
    except KeyboardInterrupt:
        print("\n\n👋 Session terminated by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 