# Claude4HaCK- Drug Repositioning Agent
This is the group repo for an Anthropic hackathon event @ LSE @ 19/06/2025

## Overview

This project implements a Claude-powered agent that identifies drugs that could be repurposed as repositioning candidates for user-provided diseases or molecular pathology mechanisms. The agent uses LangGraph to create a state-based workflow that analyzes molecular pathology similarities between diseases to suggest existing drugs for new therapeutic applications.

## Features

- **Intelligent Disease Analysis**: Extracts molecular markers and pathology from disease names or molecular observations
- **Drug Repositioning Logic**: Identifies drugs from similar diseases based on shared molecular pathology
- **Smart Filtering**: Removes drugs already in use for the target disease
- **Multiple Interfaces**: Enhanced CLI, Simple CLI, and Modern Web Interface
- **Real-time Progress**: Live updates during analysis
- **Demo Mode**: Test without API key using simulated data
- **Export Options**: Save results in JSON, text, or print format
- **State-Based Architecture**: Uses LangGraph for robust workflow management

## Prerequisites

- Python 3.8+ (Anaconda/Miniconda recommended)
- Anthropic API key (optional - get one at https://console.anthropic.com/)
  - **Note**: All interfaces work in demo mode without an API key

## Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/HanshangZhu/Claude4HaCK-.git
cd Claude4HaCK-

# Install dependencies
pip install -r requirements.txt

# Configure API key (optional)
cp env.example .env
# Edit .env and add your Anthropic API key
```

### 2. Choose Your Interface

#### 🎨 **Enhanced CLI** (Recommended for Terminal Users)
Beautiful terminal interface with rich formatting, progress bars, and interactive menus.

```bash
# Interactive launcher - choose your interface
python start_cli.py

# Direct enhanced CLI
python start_cli.py --enhanced

# Demo mode (no API key needed)
python start_cli.py --enhanced --dry-run
```

#### ⚡ **Simple CLI** (Quick Analysis)
Fast, straightforward command-line interface for immediate results.

```bash
# Simple CLI
python start_cli.py --simple

# Or run directly
python realtime_demo.py
python realtime_demo.py --dry-run  # Demo mode
```

#### 🌐 **Web Interface** (Comprehensive Experience)
Modern, responsive web application with real-time updates.

```bash
# Start web server (browser opens automatically)
python start_web.py

# Custom port
python start_web.py --port 8080

# Production mode
python start_web.py --production

# Allow external access
python start_web.py --public
```

## Usage Examples

### Web Interface
1. Open browser to http://127.0.0.1:5000 (opens automatically)
2. Enter disease name: `"Alzheimer's disease"` or `"Parkinson's disease"`
3. Or molecular pathology: `"BRCA1 mutations, DNA repair defects"`
4. Choose Real mode (with API key) or Demo mode
5. Watch real-time analysis progress
6. Export results as needed

### CLI Examples
```bash
# Enhanced CLI with beautiful formatting
python start_cli.py --enhanced
> Enter: "Huntington's disease"
> Watch interactive progress and formatted results

# Simple CLI for quick analysis  
python realtime_demo.py
> Enter: "Type 2 diabetes"
> Get immediate text-based results
```

## Interface Comparison

| Feature | Enhanced CLI | Simple CLI | Web Interface |
|---------|-------------|------------|---------------|
| Rich Formatting | ✅ | ❌ | ✅ |
| Real-time Progress | ✅ | ✅ | ✅ |
| Interactive Menus | ✅ | ❌ | ✅ |
| Export Options | 🔜 | ❌ | ✅ |
| History Tracking | 🔜 | ❌ | ✅ |
| Mobile Support | ❌ | ❌ | ✅ |
| Multi-user Support | ❌ | ❌ | ✅ |
| Setup Complexity | Low | Low | Medium |

## Demo Mode

All interfaces support demo mode for testing without an API key:
- **Enhanced CLI**: `python start_cli.py --enhanced --dry-run`
- **Simple CLI**: `python realtime_demo.py --dry-run`
- **Web Interface**: Check "Demo Mode" checkbox

Demo mode provides realistic simulated data to test the full workflow.

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
├── 🧬 Core Agent
│   ├── drug_repositioning_agent.py    # LangGraph agent implementation
│   └── test_setup.py                  # Setup validation
├── 🖥️ CLI Interfaces  
│   ├── enhanced_cli.py                # Rich terminal interface
│   ├── realtime_demo.py               # Simple CLI interface
│   ├── start_cli.py                   # CLI launcher script
│   ├── interactive_demo.py            # Step-by-step demo
│   └── leigh_syndrome_demo.py         # Specific disease demo
├── 🌐 Web Interface
│   ├── web_app.py                     # Flask web application
│   ├── start_web.py                   # Web server launcher
│   ├── templates/index.html           # Main web interface
│   ├── static/css/style.css           # Modern CSS styling
│   └── static/js/app.js               # Frontend JavaScript
├── 📚 Configuration & Setup
│   ├── requirements.txt               # Python dependencies
│   ├── environment.yml                # Conda environment
│   ├── setup.sh                       # Automated setup script
│   ├── env.example                    # API key template
│   └── .gitignore                     # Git ignore rules
└── 📖 Documentation
    ├── README.md                      # This file
    └── FRONTEND_README.md             # Detailed frontend guide
```

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **API Key Issues**
   - Use demo mode: Add `--dry-run` flag or check "Demo Mode"
   - Check `.env` file has correct API key format

3. **Port Already in Use (Web)**
   ```bash
   python start_web.py --port 8080
   ```

4. **Permission Issues**
   ```bash
   chmod +x setup.sh
   ```

### Getting Help

- **Enhanced CLI**: Built-in help menu (option 4)
- **Web Interface**: Click "Help" in navigation
- **Documentation**: See `FRONTEND_README.md` for detailed frontend guide

## Advanced Usage

### Custom Configuration
```bash
# Web interface with custom settings
python start_web.py --host 0.0.0.0 --port 3000 --production

# CLI with specific options
python enhanced_cli.py --dry-run
```

### API Integration
The web interface provides RESTful endpoints:
- `POST /api/analyze` - Start analysis
- `GET /api/history` - Get analysis history  
- `GET /api/status` - Check API status

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