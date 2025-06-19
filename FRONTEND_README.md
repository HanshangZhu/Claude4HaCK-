# 🧬 Drug Repositioning Agent - Frontend Interfaces

This document describes the available frontend interfaces for the Drug Repositioning Agent, including both command-line interfaces (CLI) and web interface.

## 🎯 Overview

The Drug Repositioning Agent now provides multiple interfaces:

1. **Enhanced CLI** - Rich, interactive command-line interface with beautiful formatting
2. **Simple CLI** - Basic real-time command-line interface  
3. **Web Interface** - Modern, responsive web application with real-time updates

## 🖥️ Command Line Interfaces (CLI)

### Enhanced CLI Interface

A beautiful, interactive command-line interface with rich formatting, progress bars, and comprehensive menus.

**Features:**
- 🎨 Rich terminal formatting with colors and styling
- 📊 Interactive progress bars and step indicators
- 📋 Menu-driven navigation
- ⚙️ Settings management
- 🧪 Dry-run mode for testing
- 💾 Analysis history (coming soon)
- ❓ Built-in help system
- 🔍 Filtering and validation display

**Quick Start:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run enhanced CLI
python start_cli.py --enhanced

# Run with dry-run mode (no API calls)
python start_cli.py --enhanced --dry-run

# Or run directly
python enhanced_cli.py
```

**Usage:**
```bash
# Interactive launcher
python start_cli.py

# Direct enhanced CLI
python start_cli.py --enhanced

# Enhanced CLI in demo mode
python start_cli.py --enhanced --dry-run
```

### Simple CLI Interface

A straightforward, real-time command-line interface for quick analysis.

**Features:**
- ⚡ Real-time analysis with immediate results
- 🔄 Continuous input mode
- 📝 Simple text-based output
- 🧪 Dry-run mode support

**Usage:**
```bash
# Simple CLI
python start_cli.py --simple

# Or run directly
python realtime_demo.py
python realtime_demo.py --dry-run
```

## 🌐 Web Interface

A modern, responsive web application with real-time progress updates and comprehensive analysis display.

**Features:**
- 🎨 Modern, responsive Bootstrap 5 design
- 📱 Mobile-friendly interface
- ⚡ Real-time progress updates via WebSocket
- 📊 Interactive data visualization
- 💾 Export results (JSON, Text, Print)
- 📈 Analysis history
- 🧪 Demo mode with simulated data
- 🔍 Advanced filtering display
- 📚 Built-in help and examples
- ✨ Animations and smooth transitions

### Quick Start Web Interface

```bash
# Install dependencies (if not already done)
pip install -r requirements.txt

# Start web server
python start_web.py

# The browser will automatically open to http://127.0.0.1:5000
```

### Web Interface Options

```bash
# Basic startup (opens browser automatically)
python start_web.py

# Custom port
python start_web.py --port 8080

# Production mode
python start_web.py --production

# Allow external access
python start_web.py --public

# Custom host and port  
python start_web.py --host 0.0.0.0 --port 3000

# Multiple options
python start_web.py --port 8080 --production --public
```

### Web Interface Usage

1. **Open your browser** to the provided URL (usually http://127.0.0.1:5000)
2. **Enter a disease name** or molecular pathology description
3. **Choose analysis mode**:
   - Real mode (requires API key)
   - Demo mode (uses simulated data)
4. **Click "Start Analysis"** and watch real-time progress
5. **Review results** with interactive displays
6. **Export or print** results as needed

## 🔧 Installation & Setup

### Prerequisites

- Python 3.8+
- Anthropic API key (optional, for full functionality)

### Dependencies Installation

```bash
# Install all dependencies
pip install -r requirements.txt

# Or install manually
pip install langchain langchain-anthropic python-dotenv langgraph pydantic
pip install rich click flask flask-socketio jinja2 waitress
```

### API Key Setup

1. **Get an Anthropic API key** from [console.anthropic.com](https://console.anthropic.com)
2. **Create/edit .env file**:
   ```bash
   ANTHROPIC_API_KEY=your_api_key_here
   FLASK_SECRET_KEY=drug-repo-secret-key-2024
   FLASK_ENV=development
   ```
3. **Without API key**: All interfaces work in demo mode with simulated data

## 📊 Interface Comparison

| Feature | Enhanced CLI | Simple CLI | Web Interface |
|---------|-------------|------------|---------------|
| Rich Formatting | ✅ | ❌ | ✅ |
| Real-time Progress | ✅ | ✅ | ✅ |
| Interactive Menus | ✅ | ❌ | ✅ |
| Export Options | 🔜 | ❌ | ✅ |
| History | 🔜 | ❌ | ✅ |
| Mobile Support | ❌ | ❌ | ✅ |
| Multi-user | ❌ | ❌ | ✅ |
| Browser Required | ❌ | ❌ | ✅ |
| Setup Complexity | Low | Low | Medium |

## 🎨 Web Interface Screenshots & Features

### Main Interface
- Clean, modern design with gradient headers
- Responsive layout that works on all devices
- Real-time status indicators

### Analysis Progress
- Visual progress bar with percentage
- Step-by-step indicators
- Real-time status messages
- Animated progress indicators

### Results Display
- Color-coded molecular markers
- Interactive drug candidate cards
- Comprehensive filtering analysis
- Source references and citations

### Additional Features
- Export results in multiple formats
- Print-friendly layout
- Analysis history tracking
- Built-in help and examples

## 🚀 Deployment Options

### Development
```bash
# Local development with auto-reload
python start_web.py --debug

# Local development on custom port
python start_web.py --port 8080 --debug
```

### Production
```bash
# Production mode (optimized, no debug)
python start_web.py --production

# Production with external access
python start_web.py --production --public --port 80
```

### Docker Deployment (Future)
```dockerfile
# Example Dockerfile structure
FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "start_web.py", "--production", "--host", "0.0.0.0"]
```

## 🧪 Demo Mode

All interfaces support demo mode for testing without an API key:

- **CLI**: Use `--dry-run` flag
- **Web**: Check "Demo Mode" checkbox
- **Features**: Simulated molecular analysis and drug candidates
- **Purpose**: Testing, demonstrations, development

## ❓ Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   python start_web.py --port 8080
   ```

2. **Missing dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **API key issues**
   - Check `.env` file exists and has correct API key
   - Use demo mode if no API key available

4. **Browser doesn't open automatically**
   - Manually navigate to the displayed URL
   - Check firewall settings

### Performance Tips

- Use production mode for better performance
- Close unused browser tabs
- Use demo mode for testing to avoid API costs

## 📝 Examples

### CLI Example Session
```bash
$ python start_cli.py --enhanced
🧬 Starting Enhanced CLI Interface...

# Interactive menu appears with options
# Select "Analyze Disease/Condition"
# Enter "Alzheimer's disease"
# Watch beautiful progress bars and results
```

### Web Interface Example
1. Navigate to http://127.0.0.1:5000
2. Enter "Parkinson's disease"  
3. Click "Start Analysis"
4. Watch real-time progress updates
5. Review comprehensive results
6. Export as needed

## 🔮 Future Enhancements

- [ ] Analysis history persistence
- [ ] User authentication
- [ ] Batch analysis support
- [ ] API endpoint for external integration
- [ ] Docker containerization
- [ ] Cloud deployment guides
- [ ] Advanced visualization options
- [ ] Collaborative features

## 🛟 Support

- **Documentation**: This README and inline help
- **Demo Mode**: Test without API key
- **Examples**: Built into web interface help
- **Error Messages**: Detailed error reporting in all interfaces

Choose the interface that best fits your needs:
- **Enhanced CLI**: For power users who prefer command-line
- **Simple CLI**: For quick, basic analysis  
- **Web Interface**: For comprehensive analysis with visual features 