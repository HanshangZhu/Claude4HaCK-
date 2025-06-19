#!/usr/bin/env python3
"""
Enhanced CLI Interface for Drug Repositioning Agent
Beautiful terminal interface with rich formatting
"""

import sys
import os
import time
from dotenv import load_dotenv
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich.columns import Columns
from rich.tree import Tree
from rich.live import Live
from rich.layout import Layout
from rich.align import Align
from rich import box

from drug_repositioning_agent import (
    create_drug_repositioning_graph, 
    MolecularAnalysis,
    DrugCandidate,
    DrugCandidateList
)
from langchain_core.messages import HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Initialize Rich console
console = Console()

class DrugRepositioningCLI:
    def __init__(self):
        self.console = console
        self.llm = None
        self.dry_run = False
        
    def initialize_llm(self):
        """Initialize Claude LLM"""
        try:
            self.llm = ChatAnthropic(
                model="claude-3-5-sonnet-20241022",
                anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
                temperature=0.3
            )
            return True
        except Exception as e:
            self.console.print(f"[red]❌ Error initializing LLM: {e}[/red]")
            return False
    
    def show_banner(self):
        """Display application banner"""
        banner_text = """
        # 🧬 Drug Repositioning Agent
        
        **AI-Powered Drug Discovery & Repositioning**
        
        Identify promising drug candidates for repositioning based on molecular pathology analysis.
        """
        
        banner = Panel(
            Markdown(banner_text),
            title="🔬 Welcome",
            border_style="blue",
            box=box.DOUBLE
        )
        
        self.console.print(banner)
    
    def show_main_menu(self):
        """Display main menu and get user choice"""
        menu_options = [
            "🔍 Analyze Disease/Condition",
            "📊 View Analysis History",
            "⚙️  Settings",
            "❓ Help",
            "👋 Exit"
        ]
        
        menu_table = Table(show_header=False, box=box.ROUNDED)
        menu_table.add_column("Option", style="cyan", no_wrap=True)
        menu_table.add_column("Description", style="white")
        
        for i, option in enumerate(menu_options, 1):
            menu_table.add_row(f"[bold]{i}[/bold]", option)
        
        menu_panel = Panel(
            menu_table,
            title="🎯 Main Menu",
            border_style="green"
        )
        
        self.console.print(menu_panel)
        
        choice = Prompt.ask(
            "[bold cyan]Select an option[/bold cyan]",
            choices=["1", "2", "3", "4", "5"],
            default="1"
        )
        
        return int(choice)
    
    def get_disease_input(self):
        """Get disease/condition input from user with rich formatting"""
        input_panel = Panel(
            "[bold cyan]Enter your disease or molecular pathology:[/bold cyan]\n\n"
            "[white]You can provide either:[/white]\n"
            "[green]• A disease name[/green] (e.g., 'Parkinson's disease', 'Type 2 diabetes')\n"
            "[green]• Molecular pathology[/green] (e.g., 'BRCA1 mutations, DNA repair defects')\n\n"
            "[dim]Examples:[/dim]\n"
            "[dim]- Alzheimer's disease[/dim]\n"
            "[dim]- Huntington's disease[/dim]\n"
            "[dim]- p53 mutations, apoptosis defects[/dim]",
            title="📝 Input Required",
            border_style="yellow"
        )
        
        self.console.print(input_panel)
        
        while True:
            disease_input = Prompt.ask("[bold]Disease/Pathology")
            if disease_input.strip():
                return disease_input.strip()
            self.console.print("[red]Please enter a valid disease name or molecular pathology.[/red]")
    
    def analyze_with_progress(self, user_input):
        """Analyze disease with progress tracking"""
        if self.dry_run:
            return self.simulate_analysis(user_input)
        
        if not self.llm:
            if not self.initialize_llm():
                return None
        
        result = {}
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=self.console
        ) as progress:
            
            # Step 1: Molecular Analysis
            task1 = progress.add_task("🔬 Analyzing molecular pathology...", total=100)
            
            try:
                molecular_analysis = self.perform_molecular_analysis(user_input, progress, task1)
                result['molecular_analysis'] = molecular_analysis
                progress.update(task1, completed=100)
            except Exception as e:
                self.console.print(f"[red]❌ Error in molecular analysis: {e}[/red]")
                return None
            
            # Step 2: Drug Identification
            task2 = progress.add_task("💊 Identifying drug candidates...", total=100)
            
            try:
                drug_candidates = self.identify_drug_candidates(molecular_analysis, progress, task2)
                result['drug_candidates'] = drug_candidates
                progress.update(task2, completed=100)
            except Exception as e:
                self.console.print(f"[red]❌ Error in drug identification: {e}[/red]")
                return None
            
            # Step 3: Filtering
            task3 = progress.add_task("🔍 Filtering candidates...", total=100)
            
            try:
                filter_analysis = self.filter_candidates(molecular_analysis, drug_candidates, progress, task3)
                result['filter_analysis'] = filter_analysis
                progress.update(task3, completed=100)
            except Exception as e:
                self.console.print(f"[red]❌ Error in filtering: {e}[/red]")
                result['filter_analysis'] = "Filtering failed"
        
        return result
    
    def perform_molecular_analysis(self, user_input, progress, task):
        """Perform molecular pathology analysis"""
        progress.update(task, advance=25)
        
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
        
        structured_llm = self.llm.with_structured_output(MolecularAnalysis)
        chain = analysis_prompt | structured_llm
        
        progress.update(task, advance=50)
        molecular_analysis = chain.invoke({"user_input": user_input})
        progress.update(task, advance=25)
        
        return molecular_analysis
    
    def identify_drug_candidates(self, molecular_analysis, progress, task):
        """Identify drug repositioning candidates"""
        progress.update(task, advance=25)
        
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
        
        drug_structured_llm = self.llm.with_structured_output(DrugCandidateList)
        drug_chain = drug_prompt | drug_structured_llm
        
        progress.update(task, advance=50)
        drug_candidates = drug_chain.invoke({
            "disease_name": molecular_analysis.disease_name,
            "molecular_markers": molecular_analysis.molecular_markers
        })
        progress.update(task, advance=25)
        
        return drug_candidates
    
    def filter_candidates(self, molecular_analysis, drug_candidates, progress, task):
        """Filter and validate drug candidates"""
        progress.update(task, advance=25)
        
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
        
        progress.update(task, advance=50)
        filter_response = self.llm.invoke(filter_prompt.format_messages(
            disease_name=molecular_analysis.disease_name,
            candidates=candidates_text
        ))
        progress.update(task, advance=25)
        
        return filter_response.content
    
    def simulate_analysis(self, user_input):
        """Simulate analysis for dry run mode"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            task = progress.add_task("🧪 Running simulation...", total=None)
            time.sleep(2)  # Simulate processing time
            
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
            
            progress.stop()
        
        return {
            "molecular_analysis": mock_analysis,
            "drug_candidates": mock_candidates,
            "filter_analysis": "Simulated filtering - this would remove inappropriate candidates"
        }
    
    def display_results(self, result):
        """Display analysis results with rich formatting"""
        molecular_analysis = result['molecular_analysis']
        drug_candidates = result['drug_candidates']
        filter_analysis = result['filter_analysis']
        
        # Disease Information Panel
        disease_panel = Panel(
            f"[bold blue]{molecular_analysis.disease_name}[/bold blue]",
            title="🎯 Target Disease/Condition",
            border_style="blue"
        )
        self.console.print(disease_panel)
        
        # Molecular Markers
        markers_tree = Tree("🔬 [bold]Molecular Markers[/bold]")
        for category, markers in molecular_analysis.molecular_markers.items():
            category_node = markers_tree.add(f"[cyan]{category}[/cyan]")
            for marker in markers:
                category_node.add(f"[white]{marker}[/white]")
        
        markers_panel = Panel(
            markers_tree,
            title="🧬 Molecular Pathology",
            border_style="green"
        )
        self.console.print(markers_panel)
        
        # Drug Candidates Table
        drug_table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        drug_table.add_column("Drug", style="bold cyan", no_wrap=True)
        drug_table.add_column("Status", style="green")
        drug_table.add_column("Current Uses", style="blue")
        drug_table.add_column("Molecular Rationale", style="white")
        
        for candidate in drug_candidates.candidates:
            drug_table.add_row(
                candidate.drug_name,
                candidate.approval_status,
                ", ".join(candidate.current_applications[:2]),  # Limit to 2 applications
                candidate.molecular_rationale[:100] + "..." if len(candidate.molecular_rationale) > 100 else candidate.molecular_rationale
            )
        
        drug_panel = Panel(
            drug_table,
            title="💊 Drug Repositioning Candidates",
            border_style="yellow"
        )
        self.console.print(drug_panel)
        
        # Filtering Analysis
        if filter_analysis and filter_analysis != "Filtering failed":
            filter_panel = Panel(
                Markdown(filter_analysis),
                title="🔍 Filtering Analysis",
                border_style="red"
            )
            self.console.print(filter_panel)
        
        # Sources
        sources_text = "\n".join([f"• {source}" for source in molecular_analysis.sources])
        sources_panel = Panel(
            sources_text,
            title="📚 Sources",
            border_style="dim"
        )
        self.console.print(sources_panel)
    
    def show_settings(self):
        """Show settings menu"""
        settings_table = Table(show_header=True, header_style="bold magenta")
        settings_table.add_column("Setting", style="cyan")
        settings_table.add_column("Current Value", style="green")
        settings_table.add_column("Description", style="white")
        
        settings_table.add_row("Dry Run Mode", str(self.dry_run), "Use simulated data instead of API calls")
        settings_table.add_row("API Key", "***" if os.getenv("ANTHROPIC_API_KEY") else "Not Set", "Anthropic API key status")
        
        settings_panel = Panel(
            settings_table,
            title="⚙️ Settings",
            border_style="blue"
        )
        self.console.print(settings_panel)
        
        if Confirm.ask("Would you like to toggle dry run mode?"):
            self.dry_run = not self.dry_run
            self.console.print(f"[green]✅ Dry run mode: {'Enabled' if self.dry_run else 'Disabled'}[/green]")
    
    def show_help(self):
        """Show help information"""
        help_text = """
        # 🧬 Drug Repositioning Agent Help
        
        ## What is Drug Repositioning?
        Drug repositioning involves finding new therapeutic uses for existing drugs based on shared molecular pathology between diseases.
        
        ## How to Use This Tool
        
        1. **Analyze Disease/Condition**: Enter a disease name or molecular pathology description
        2. **View Results**: Review molecular markers and drug candidates
        3. **Settings**: Configure dry run mode and other options
        
        ## Input Examples
        
        **Disease Names:**
        - Alzheimer's disease
        - Parkinson's disease  
        - Type 2 diabetes
        - Huntington's disease
        
        **Molecular Pathology:**
        - BRCA1 mutations, DNA repair defects
        - p53 mutations, apoptosis pathway disruption
        - Tau protein aggregation, neurodegeneration
        
        ## Features
        
        - 🔬 **Molecular Analysis**: Identifies key pathological markers
        - 💊 **Drug Discovery**: Finds repositioning candidates
        - 🔍 **Smart Filtering**: Removes inappropriate candidates
        - 🧪 **Dry Run Mode**: Test without API calls
        """
        
        help_panel = Panel(
            Markdown(help_text),
            title="❓ Help & Usage Guide",
            border_style="cyan"
        )
        self.console.print(help_panel)
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
    
    def run(self):
        """Main application loop"""
        try:
            self.show_banner()
            
            while True:
                choice = self.show_main_menu()
                
                if choice == 1:  # Analyze Disease/Condition
                    disease_input = self.get_disease_input()
                    
                    self.console.print(f"\n[bold]🔍 Analyzing: {disease_input}[/bold]")
                    
                    result = self.analyze_with_progress(disease_input)
                    
                    if result:
                        self.console.print("\n[bold green]✅ Analysis Complete![/bold green]")
                        self.display_results(result)
                        
                        if Confirm.ask("\nWould you like to save these results?"):
                            self.console.print("[dim]💾 Save functionality coming soon![/dim]")
                    else:
                        self.console.print("[red]❌ Analysis failed. Please try again.[/red]")
                    
                    Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
                
                elif choice == 2:  # View Analysis History
                    self.console.print("[dim]📊 History functionality coming soon![/dim]")
                    Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
                
                elif choice == 3:  # Settings
                    self.show_settings()
                    Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
                
                elif choice == 4:  # Help
                    self.show_help()
                
                elif choice == 5:  # Exit
                    self.console.print("\n[bold blue]👋 Thank you for using the Drug Repositioning Agent![/bold blue]")
                    break
        
        except KeyboardInterrupt:
            self.console.print("\n\n[yellow]👋 Session terminated by user. Goodbye![/yellow]")
        except Exception as e:
            self.console.print(f"\n[red]❌ Unexpected error: {e}[/red]")
            sys.exit(1)

@click.command()
@click.option('--dry-run', is_flag=True, help='Run in dry-run mode with simulated data')
def main(dry_run):
    """Enhanced CLI interface for Drug Repositioning Agent"""
    cli = DrugRepositioningCLI()
    cli.dry_run = dry_run
    cli.run()

if __name__ == "__main__":
    main() 