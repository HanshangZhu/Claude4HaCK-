# Claude4HaCK- Drug Repositioning Agent
This is the group repo for an Anthropic hackathon event @ LSE @ 19/06/2025

## Overview

This project implements a Claude-powered agent that identifies drugs that could be repurposed as repositioning candidates for user-provided diseases or molecular pathology mechanisms. The agent uses LangGraph to create a state-based workflow that analyzes molecular pathology similarities between diseases to suggest existing drugs for new therapeutic applications.

## Features

- **Intelligent Disease Analysis**: Extracts molecular markers and pathology from disease names or molecular observations
- **Drug Repositioning Logic**: Identifies drugs from similar diseases based on shared molecular pathology
- **Smart Filtering**: Removes drugs already in use for the target disease
- **Interactive Interface**: User-friendly command-line interface for exploring drug repositioning opportunities
- **State-Based Architecture**: Uses LangGraph for robust workflow management

## Prerequisites

- Anaconda or Miniconda installed
- Anthropic API key (get one at https://console.anthropic.com/)

## Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd Claude4HaCK-
```

### 2. Set up the conda environment
```bash
# Run the setup script
./setup.sh

# Or manually create the environment
conda env create -f environment.yml
```

### 3. Activate the environment
```bash
conda activate drug-repositioning
```

### 4. Configure API key
```bash
# Copy the example environment file
cp env.example .env

# Edit .env and add your Anthropic API key
# Replace 'your_api_key_here' with your actual API key
```

## Usage

### Interactive Mode (Recommended)
```bash
python run_agent.py
```

This will start an interactive session where you can:
- Enter disease names (e.g., "Alzheimer's disease", "Type 2 diabetes")
- Provide molecular pathology observations
- Get detailed drug repositioning recommendations

### Script Mode
```bash
python drug_repositioning_agent.py
```

This runs a demo with Alzheimer's disease as an example.

### Testing Setup
```bash
python test_setup.py
```

This validates that all dependencies are correctly installed and configured.

## Architecture

The agent follows this state diagram:

1. **State 1 (Greeting)**: Initial welcome and instructions
2. **State 2 (Molecular Analysis)**: Extracts disease information or summarizes molecular pathology
3. **State 3 (Drug Identification)**: Identifies potential drug candidates based on molecular similarities
4. **State 4 (Drug Filtering)**: Filters out drugs already used for the target disease
5. **End State**: Presents final recommendations

### Key Components

- `drug_repositioning_agent.py`: Core agent implementation using LangGraph
- `run_agent.py`: Interactive interface for the agent
- `environment.yml`: Conda environment specification
- `requirements.txt`: Python package dependencies
- `test_setup.py`: Setup validation script

## Example Output

```
============================================================
Drug Repositioning Agent - Interactive Mode
============================================================
✓ Agent initialized successfully!

Hi, I am a drug repositioning assistant! I can help identify existing drugs that might be repurposed for your disease of interest based on shared molecular pathology. Please provide either:
1. A disease name, or
2. A set of molecular pathology observations/phenotypes

------------------------------------------------------------

Your input (or 'quit' to exit): Parkinson's disease

Processing your request... 
```

The agent will analyze Parkinson's disease molecular pathology and identify drugs with potential repositioning opportunities based on shared molecular mechanisms.

## Project Structure

```
Claude4HaCK-/
├── drug_repositioning_agent.py  # Core LangGraph agent implementation
├── run_agent.py                 # Interactive CLI interface
├── test_setup.py                # Setup validation script
├── setup.sh                     # Automated setup script
├── environment.yml              # Conda environment specification
├── requirements.txt             # Python package dependencies
├── env.example                  # Example environment variables
├── README.md                    # This file
└── .git/                        # Git repository
```

## How It Works

1. **User Input**: The user provides either a disease name or molecular pathology observations
2. **Molecular Analysis**: Claude analyzes the input to extract key molecular markers, mutations, and pathology
3. **Drug Identification**: The system identifies existing drugs used for diseases with similar molecular profiles
4. **Intelligent Filtering**: Drugs already used for the target disease are filtered out
5. **Recommendation**: The agent presents repositioning candidates with detailed molecular rationale

## Contributing

This project was created for the Anthropic hackathon at LSE. Contributions are welcome!

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with Claude API by Anthropic
- Uses LangGraph for state management
- Created for the Anthropic Hackathon @ LSE @ 19/06/2025