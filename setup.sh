#!/bin/bash

echo "Setting up Drug Repositioning Agent environment..."

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "Conda is not installed. Please install Anaconda or Miniconda first."
    exit 1
fi

# Create conda environment from environment.yml
echo "Creating conda environment..."
conda env create -f environment.yml

echo ""
echo "Environment created successfully!"
echo ""
echo "To activate the environment, run:"
echo "  conda activate drug-repositioning"
echo ""
echo "Don't forget to:"
echo "1. Copy env.example to .env"
echo "2. Add your Anthropic API key to .env"
echo ""
echo "Then run the agent with:"
echo "  python drug_repositioning_agent.py" 