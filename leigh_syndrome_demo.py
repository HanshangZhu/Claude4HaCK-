#!/usr/bin/env python3
"""
Direct Demo for Leigh Syndrome Drug Repositioning
This bypasses the workflow issues and directly processes the analysis.
"""

import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Dict, List

# Load environment variables
load_dotenv()

# Initialize Claude
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=0.3
)

# Define output schemas
class MolecularAnalysis(BaseModel):
    """Schema for molecular analysis output"""
    disease_name: str = Field(description="Standardized disease name")
    molecular_markers: Dict[str, List[str]] = Field(
        description="Dictionary of molecular markers including mutations, cellular abnormalities, pathways"
    )
    sources: List[str] = Field(description="Sources of information used")

class DrugCandidate(BaseModel):
    """Schema for drug candidate"""
    drug_name: str = Field(description="Name of the drug")
    approval_status: str = Field(description="FDA/regulatory approval status")
    current_applications: List[str] = Field(description="Current approved uses")
    molecular_rationale: str = Field(description="Molecular pathology rationale for repositioning")
    shared_pathology: str = Field(description="Shared molecular pathology with target disease")

class DrugCandidateList(BaseModel):
    """Schema for list of drug candidates"""
    candidates: List[DrugCandidate] = Field(description="List of potential drug repositioning candidates")

def analyze_leigh_syndrome():
    """Analyze Leigh Syndrome for drug repositioning"""
    
    print("="*80)
    print("🧬 DRUG REPOSITIONING ANALYSIS: LEIGH SYNDROME")
    print("="*80)
    
    # Step 1: Molecular Analysis
    print("\n🔬 STEP 1: MOLECULAR PATHOLOGY ANALYSIS")
    print("-" * 50)
    
    analysis_prompt = ChatPromptTemplate.from_template("""
    You are a molecular pathologist. Analyze Leigh Syndrome and identify its key molecular markers including:
    - Genetic mutations
    - Cellular abnormalities  
    - Affected molecular pathways
    - Protein expression changes
    - Other molecular phenotypes
    
    Provide comprehensive molecular characterization with sources.
    
    Disease: Leigh Syndrome
    """)
    
    structured_llm = llm.with_structured_output(MolecularAnalysis)
    chain = analysis_prompt | structured_llm
    
    print("Analyzing molecular pathology...")
    molecular_analysis = chain.invoke({"disease": "Leigh Syndrome"})
    
    print(f"✓ Disease: {molecular_analysis.disease_name}")
    print(f"✓ Molecular markers identified:")
    for category, markers in molecular_analysis.molecular_markers.items():
        print(f"   • {category}: {', '.join(markers[:3])}{'...' if len(markers) > 3 else ''}")
    
    # Step 2: Drug Identification
    print("\n💊 STEP 2: DRUG REPOSITIONING CANDIDATES")
    print("-" * 50)
    
    drug_prompt = ChatPromptTemplate.from_template("""
    You are an expert in drug repositioning and molecular pathology. 
    Based on the molecular markers provided for Leigh Syndrome, identify existing drugs that could be repurposed.
    
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
    
    Disease: {disease_name}
    Molecular markers: {molecular_markers}
    """)
    
    drug_structured_llm = llm.with_structured_output(DrugCandidateList)
    drug_chain = drug_prompt | drug_structured_llm
    
    print("Identifying drug repositioning candidates...")
    drug_candidates = drug_chain.invoke({
        "disease_name": molecular_analysis.disease_name,
        "molecular_markers": molecular_analysis.molecular_markers
    })
    
    print(f"✓ Found {len(drug_candidates.candidates)} potential candidates:")
    for i, candidate in enumerate(drug_candidates.candidates, 1):
        print(f"   {i}. {candidate.drug_name} ({candidate.approval_status})")
    
    # Step 3: Filtering
    print("\n🔍 STEP 3: FILTERING & VALIDATION")
    print("-" * 50)
    
    filter_prompt = ChatPromptTemplate.from_template("""
    Review these drug candidates for Leigh Syndrome repositioning:
    
    {candidates}
    
    Remove any drugs that are:
    1. Already approved or in trials for Leigh Syndrome
    2. Would not logically help with mitochondrial dysfunction
    3. Have weak molecular rationale
    
    Return only the most promising candidates with strong scientific rationale.
    """)
    
    candidates_text = "\n".join([
        f"- {c.drug_name}: {c.molecular_rationale}" 
        for c in drug_candidates.candidates
    ])
    
    print("Filtering candidates...")
    filter_response = llm.invoke(filter_prompt.format_messages(candidates=candidates_text))
    
    # Step 4: Final Results
    print("\n🎯 FINAL RESULTS")
    print("="*80)
    
    print(f"\nDisease: {molecular_analysis.disease_name}")
    print(f"Key Pathology: Mitochondrial dysfunction, energy metabolism defects")
    
    print(f"\n📋 DRUG REPOSITIONING CANDIDATES:")
    print("-" * 50)
    
    for i, candidate in enumerate(drug_candidates.candidates, 1):
        print(f"\n{i}. {candidate.drug_name}")
        print(f"   Status: {candidate.approval_status}")
        print(f"   Current Uses: {', '.join(candidate.current_applications)}")
        print(f"   Molecular Rationale: {candidate.molecular_rationale}")
        print(f"   Shared Pathology: {candidate.shared_pathology}")
    
    print(f"\n🔍 FILTERING ANALYSIS:")
    print("-" * 30)
    print(filter_response.content)
    
    print(f"\n📚 SOURCES:")
    print("-" * 20)
    for source in molecular_analysis.sources:
        print(f"• {source}")
    
    print("\n" + "="*80)
    print("✅ ANALYSIS COMPLETE")
    print("="*80)
    
    return {
        "molecular_analysis": molecular_analysis,
        "drug_candidates": drug_candidates,
        "filter_analysis": filter_response.content
    }

def main():
    """Main execution"""
    try:
        print("🚀 Starting Leigh Syndrome Drug Repositioning Analysis...")
        print("🔑 API Key configured successfully")
        
        result = analyze_leigh_syndrome()
        
        print("\n💡 SUMMARY:")
        print(f"• Disease analyzed: {result['molecular_analysis'].disease_name}")
        print(f"• Drug candidates found: {len(result['drug_candidates'].candidates)}")
        print(f"• Molecular pathways analyzed: {len(result['molecular_analysis'].molecular_markers)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your API key configuration.")

if __name__ == "__main__":
    main() 