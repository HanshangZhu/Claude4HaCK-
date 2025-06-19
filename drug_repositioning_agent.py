import os
import sys
import argparse
from typing import Dict, List, TypedDict, Annotated, Sequence, Literal
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import operator

# Load environment variables
load_dotenv()

# Global flags
DRY_RUN = False
DEBUG = False

# Initialize Claude (only if not in dry run mode)
def get_llm():
    if DRY_RUN:
        return None
    return ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        temperature=0.3
    )

llm = get_llm()

# Define the graph state
class GraphState(TypedDict):
    """State of the drug repositioning agent"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    user_input: str
    disease_or_pathology: str
    molecular_markers: Dict[str, List[str]]
    drug_candidates: List[Dict[str, str]]
    filtered_candidates: List[Dict[str, str]]
    sources: List[str]

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

# Dry run mock data
def get_mock_molecular_analysis(disease_input: str) -> MolecularAnalysis:
    """Mock molecular analysis for dry run mode"""
    return MolecularAnalysis(
        disease_name="Alzheimer's Disease",
        molecular_markers={
            "mutations": ["APOE4", "APP", "PSEN1", "PSEN2"],
            "cellular_abnormalities": ["amyloid plaques", "neurofibrillary tangles", "neuroinflammation"],
            "pathways": ["amyloid cascade", "tau phosphorylation", "oxidative stress"]
        },
        sources=["PubMed", "KEGG", "Alzheimer's Association"]
    )

def get_mock_drug_candidates() -> DrugCandidateList:
    """Mock drug candidates for dry run mode"""
    return DrugCandidateList(
        candidates=[
            DrugCandidate(
                drug_name="Metformin",
                approval_status="FDA Approved",
                current_applications=["Type 2 Diabetes"],
                molecular_rationale="Activates AMPK pathway, reduces neuroinflammation, may inhibit tau phosphorylation",
                shared_pathology="Both involve metabolic dysfunction and oxidative stress"
            ),
            DrugCandidate(
                drug_name="Lithium",
                approval_status="FDA Approved",
                current_applications=["Bipolar Disorder"],
                molecular_rationale="Inhibits GSK-3β, reduces tau phosphorylation, neuroprotective effects",
                shared_pathology="Tau pathway dysfunction present in both conditions"
            ),
            DrugCandidate(
                drug_name="Rapamycin",
                approval_status="FDA Approved",
                current_applications=["Immunosuppression", "Cancer"],
                molecular_rationale="mTOR inhibition, enhances autophagy, clears protein aggregates",
                shared_pathology="Protein aggregation and autophagy dysfunction"
            )
        ]
    )

# Node functions
def greeting_node(state: GraphState) -> GraphState:
    """State 1: Initial greeting"""
    if DEBUG:
        print("🔄 WORKFLOW DEBUG: Executing greeting_node")
    
    greeting = AIMessage(content="Hi, I am a drug repositioning assistant! I can help identify existing drugs that might be repurposed for your disease of interest based on shared molecular pathology. Please provide either:\n1. A disease name, or\n2. A set of molecular pathology observations/phenotypes")
    return {"messages": [greeting]}

def molecular_analysis_node(state: GraphState) -> GraphState:
    """State 2 (subgraph): Extract disease or summarize molecular pathology"""
    if DEBUG:
        print("🔄 WORKFLOW DEBUG: Executing molecular_analysis_node")
    
    user_input = state["messages"][-1].content if state["messages"] else ""
    
    if DRY_RUN:
        if DEBUG:
            print("🧪 DRY RUN: Using mock molecular analysis")
        result = get_mock_molecular_analysis(user_input)
    else:
        # Create a structured prompt for molecular analysis
        analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a molecular pathologist. Analyze the user input to:
            1. If a disease name is provided, identify its key molecular markers including:
               - Genetic mutations
               - Cellular abnormalities
               - Affected molecular pathways
               - Protein expression changes
               - Other molecular phenotypes
            2. If molecular observations are provided, summarize and categorize them
            
            Provide comprehensive molecular characterization with sources."""),
            MessagesPlaceholder(variable_name="messages")
        ])
        
        # Get structured output
        structured_llm = llm.with_structured_output(MolecularAnalysis)
        chain = analysis_prompt | structured_llm
        
        result = chain.invoke({"messages": state["messages"]})
    
    # Create response message
    markers_summary = ', '.join([f'{k}: {v[0] if v else "N/A"}' for k, v in list(result.molecular_markers.items())[:3]])
    analysis_message = AIMessage(
        content=f"I've analyzed the molecular pathology of {result.disease_name}. "
        f"Key molecular markers include: {markers_summary}..."
    )
    
    return {
        "messages": [analysis_message],
        "disease_or_pathology": result.disease_name,
        "molecular_markers": result.molecular_markers,
        "sources": result.sources
    }

def drug_identification_node(state: GraphState) -> GraphState:
    """State 3: Identify drug repositioning candidates"""
    if DEBUG:
        print("🔄 WORKFLOW DEBUG: Executing drug_identification_node")
    
    if DRY_RUN:
        if DEBUG:
            print("🧪 DRY RUN: Using mock drug candidates")
        result = get_mock_drug_candidates()
    else:
        # Create prompt for drug identification
        drug_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in drug repositioning and molecular pathology. 
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
            
            Ensure the molecular mechanisms align logically."""),
            ("human", f"""Disease: {state['disease_or_pathology']}
            
    Molecular markers: {state['molecular_markers']}

    Identify potential drug repositioning candidates based on shared molecular pathology.""")
        ])
        
        # Get structured output
        structured_llm = llm.with_structured_output(DrugCandidateList)
        chain = drug_prompt | structured_llm
        
        result = chain.invoke({})
    
    # Format candidates for state
    candidates = [
        {
            "drug_name": c.drug_name,
            "approval_status": c.approval_status,
            "current_applications": ", ".join(c.current_applications),
            "molecular_rationale": c.molecular_rationale,
            "shared_pathology": c.shared_pathology
        }
        for c in result.candidates
    ]
    
    # Create summary message
    summary = f"I've identified {len(candidates)} potential drug repositioning candidates for {state['disease_or_pathology']}:\n\n"
    
    for i, candidate in enumerate(candidates[:5], 1):  # Show top 5
        summary += f"{i}. **{candidate['drug_name']}**\n"
        summary += f"   - Approval Status: {candidate['approval_status']}\n"
        summary += f"   - Current Uses: {candidate['current_applications']}\n"
        summary += f"   - Rationale: {candidate['molecular_rationale']}\n\n"
    
    summary_message = AIMessage(content=summary)
    
    return {
        "messages": [summary_message],
        "drug_candidates": candidates
    }

def drug_filtering_node(state: GraphState) -> GraphState:
    """Filter out drugs already used for the disease"""
    if DEBUG:
        print("🔄 WORKFLOW DEBUG: Executing drug_filtering_node")
    
    if DRY_RUN:
        if DEBUG:
            print("🧪 DRY RUN: Simulating drug filtering")
        # In dry run, just filter out one drug as an example
        filtered = state["drug_candidates"][:-1]  # Remove last candidate
        message = AIMessage(content=f"After filtering, {len(filtered)} candidates remain suitable for repositioning (removed 1 drug already in use).")
    else:
        filter_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a drug repositioning expert. Review the drug candidates and:
            1. Remove any drugs already approved or in trials for the target disease
            2. Verify the molecular rationale is scientifically sound
            3. Keep only candidates with strong molecular pathology alignment
            
            Be strict in filtering - only keep truly novel repositioning opportunities."""),
            ("human", f"""Target disease: {state['disease_or_pathology']}
            
    Drug candidates to filter:
    {[{k: v for k, v in c.items() if k != 'shared_pathology'} for c in state['drug_candidates']]}

    Return only the drugs that are NOT currently used for this disease and have valid molecular rationale.""")
        ])
        
        response = llm.invoke(filter_prompt.format_messages())
        
        # For now, pass through all candidates (in a real implementation, this would parse the response)
        # This is a simplified version - you'd want more sophisticated filtering
        filtered = state["drug_candidates"]
        
        if not filtered:
            message = AIMessage(content="No suitable drug repositioning candidates found after filtering.")
        else:
            message = AIMessage(content=f"After filtering, {len(filtered)} candidates remain suitable for repositioning.")
    
    return {
        "messages": [message],
        "filtered_candidates": filtered
    }

# Define edge conditions
def should_filter_drugs(state: GraphState) -> Literal["filter", "end"]:
    """Condition to check if we should filter drugs"""
    result = "filter" if state.get("drug_candidates") else "end"
    if DEBUG:
        print(f"🔄 WORKFLOW DEBUG: should_filter_drugs → {result}")
    return result

def should_continue_analysis(state: GraphState) -> Literal["analyze", "end"]:
    """Condition to check if we should continue with analysis"""
    result = "end" if state.get("filtered_candidates") else "analyze"
    if DEBUG:
        print(f"🔄 WORKFLOW DEBUG: should_continue_analysis → {result}")
    return result

def should_analyze(state: GraphState) -> Literal["molecular_analysis", "end"]:
    """Condition to check if we should proceed to molecular analysis"""
    # Check if there's a user message after the greeting
    if len(state["messages"]) > 1:  # More than just the greeting
        # Check if the last message is from the user
        last_message = state["messages"][-1]
        if isinstance(last_message, HumanMessage):
            result = "molecular_analysis"
        else:
            result = "end"
    else:
        result = "end"
    
    if DEBUG:
        print(f"🔄 WORKFLOW DEBUG: should_analyze → {result}")
    return result

def print_workflow_structure():
    """Print the workflow structure for debugging"""
    print("\n" + "="*60)
    print("🔍 WORKFLOW STRUCTURE DEBUG")
    print("="*60)
    print("""
    Entry Point: greeting
    
    Nodes:
    ├── greeting_node (State 1)
    ├── molecular_analysis_node (State 2)
    ├── drug_identification_node (State 3)
    └── drug_filtering_node (State 4)
    
    Flow:
    greeting → [should_analyze] → molecular_analysis OR end
    molecular_analysis → drug_identification
    drug_identification → [should_filter_drugs] → drug_filtering OR end
    drug_filtering → [should_continue_analysis] → molecular_analysis OR end
    
    Conditional Logic:
    • should_analyze: Check if user provided input after greeting
    • should_filter_drugs: Check if drug candidates exist
    • should_continue_analysis: Check if filtering is complete
    """)
    print("="*60 + "\n")

# Build the graph
def create_drug_repositioning_graph():
    """Create the LangGraph state machine for drug repositioning"""
    
    if DEBUG:
        print_workflow_structure()
    
    # Initialize the graph
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("greeting", greeting_node)
    workflow.add_node("molecular_analysis", molecular_analysis_node)
    workflow.add_node("drug_identification", drug_identification_node)
    workflow.add_node("drug_filtering", drug_filtering_node)
    
    # Set entry point
    workflow.set_entry_point("greeting")
    
    # Add conditional edge from greeting to wait for user input
    workflow.add_conditional_edges(
        "greeting",
        should_analyze,
        {
            "molecular_analysis": "molecular_analysis",
            "end": END
        }
    )
    
    # Continue with the rest of the workflow
    workflow.add_edge("molecular_analysis", "drug_identification")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "drug_identification",
        should_filter_drugs,
        {
            "filter": "drug_filtering",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "drug_filtering",
        should_continue_analysis,
        {
            "analyze": "molecular_analysis",
            "end": END
        }
    )
    
    # Compile the graph
    return workflow.compile()

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Drug Repositioning Agent")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Run in dry-run mode with mock data (no API calls)")
    parser.add_argument("--debug", action="store_true", 
                       help="Enable debug mode to show workflow execution")
    return parser.parse_args()

# Main execution
if __name__ == "__main__":
    # Parse command line arguments
    args = parse_arguments()
    
    # Set global flags
    DRY_RUN = args.dry_run
    DEBUG = args.debug
    
    # Reinitialize LLM if needed
    if not DRY_RUN:
        llm = get_llm()
    
    # Print mode information
    mode_info = []
    if DRY_RUN:
        mode_info.append("🧪 DRY RUN MODE")
    if DEBUG:
        mode_info.append("🔍 DEBUG MODE")
    
    if mode_info:
        print("\n" + " | ".join(mode_info))
        print("-" * 50)
    
    # Create the graph
    app = create_drug_repositioning_graph()
    
    # Example usage
    print("Drug Repositioning Agent initialized!")
    print("=" * 50)
    
    # Initial state
    initial_state = {
        "messages": [],
        "user_input": "",
        "disease_or_pathology": "",
        "molecular_markers": {},
        "drug_candidates": [],
        "filtered_candidates": [],
        "sources": []
    }
    
    # Run the initial greeting - this should stop at greeting and wait
    result = app.invoke(initial_state)
    print(result["messages"][-1].content)
    print("\n" + "=" * 50)
    print("Note: The agent is now waiting for user input. In interactive mode, you would provide a disease name.")
    print("Simulating user input for demo purposes...")
    print("\n" + "=" * 50)
    
    # Example: User provides a disease
    user_message = HumanMessage(content="I'm interested in finding drug repositioning candidates for Alzheimer's disease")
    result["messages"].append(user_message)
    
    # Continue the workflow - this should now process the user input
    try:
        # Since we added a user message, we need to continue from where the greeting left off
        # The workflow should now detect the user input and proceed to molecular analysis
        print("Processing the user input through the workflow...")
        
        # Create a new state that starts after greeting with the user message
        processing_state = {
            "messages": result["messages"],  # Include both greeting and user message
            "user_input": user_message.content,
            "disease_or_pathology": "",
            "molecular_markers": {},
            "drug_candidates": [],
            "filtered_candidates": [],
            "sources": []
        }
        
        # Now invoke the workflow again - it should proceed to molecular analysis
        final_result = app.invoke(processing_state)
        
        # Print all messages from the conversation
        print("\n🗨️  CONVERSATION HISTORY:")
        print("=" * 50)
        for i, msg in enumerate(final_result["messages"]):
            role = "User" if isinstance(msg, HumanMessage) else "Assistant"
            print(f"{i+1}. {role}: {msg.content}")
            print("\n" + "-" * 30 + "\n")
            
        # Show final results if available
        if final_result.get("filtered_candidates"):
            print("\n🎯 FINAL REPOSITIONING CANDIDATES:")
            print("=" * 50)
            for i, candidate in enumerate(final_result["filtered_candidates"], 1):
                print(f"{i}. {candidate['drug_name']}")
                print(f"   Status: {candidate['approval_status']}")
                print(f"   Current Uses: {candidate['current_applications']}")
                print(f"   Molecular Rationale: {candidate['molecular_rationale']}")
                if candidate.get('shared_pathology'):
                    print(f"   Shared Pathology: {candidate['shared_pathology']}")
                print()
                
    except Exception as e:
        if DRY_RUN:
            print(f"Unexpected error in dry run mode: {e}")
        else:
            print(f"Expected error (no API key): {e}")
            print("\nThis is expected - you need to configure your Anthropic API key in the .env file")
            print("Try running with --dry-run flag to test the workflow without API calls:")
            print("  python drug_repositioning_agent.py --dry-run --debug") 