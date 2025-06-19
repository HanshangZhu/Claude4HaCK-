#!/usr/bin/env python3
"""
Startup script for Drug Repositioning Agent Web Interface
"""

import sys
import os
import argparse
import subprocess
import webbrowser
import time

def check_dependencies():
    """Check if required web dependencies are installed"""
    try:
        import flask
        import flask_socketio
        return True
    except ImportError:
        return False

def install_dependencies():
    """Install required dependencies"""
    print("Installing required web dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def check_api_key():
    """Check if API key is configured"""
    from dotenv import load_dotenv
    load_dotenv()
    return bool(os.getenv("ANTHROPIC_API_KEY"))

def setup_environment():
    """Setup environment variables if needed"""
    if not os.path.exists('.env'):
        print("Creating .env file...")
        with open('.env', 'w') as f:
            f.write("# Add your Anthropic API key here\n")
            f.write("ANTHROPIC_API_KEY=your_api_key_here\n")
            f.write("FLASK_SECRET_KEY=drug-repo-secret-key-2024\n")
            f.write("FLASK_ENV=development\n")
        print("✅ .env file created. Please add your Anthropic API key.")
        return False
    return True

def run_web_app(port=5000, debug=True, host='127.0.0.1'):
    """Run the web application"""
    
    # Check dependencies
    if not check_dependencies():
        print("Web dependencies not found. Installing...")
        install_dependencies()
    
    # Setup environment
    if not setup_environment():
        print("\n⚠️  Please edit the .env file and add your Anthropic API key.")
        print("You can still run the app in demo mode without an API key.")
        input("Press Enter to continue...")
    
    # Check API key
    has_api_key = check_api_key()
    if not has_api_key:
        print("\n⚠️  No API key found. Running in demo mode only.")
        print("To enable full functionality, add your Anthropic API key to the .env file.")
    
    print(f"\n🌐 Starting Drug Repositioning Agent Web Interface...")
    print(f"🔗 Server will be available at: http://{host}:{port}")
    print(f"📊 API Status: {'✅ Full functionality' if has_api_key else '🧪 Demo mode only'}")
    print(f"🛠️  Debug Mode: {'Enabled' if debug else 'Disabled'}")
    
    # Set environment variables
    os.environ['FLASK_ENV'] = 'development' if debug else 'production'
    os.environ['PORT'] = str(port)
    
    # Import and run the web app
    from web_app import socketio, app
    
    # Open browser after a short delay
    if host == '127.0.0.1' or host == 'localhost':
        def open_browser():
            time.sleep(1.5)
            webbrowser.open(f'http://{host}:{port}')
        
        import threading
        threading.Thread(target=open_browser, daemon=True).start()
    
    # Run the application
    try:
        socketio.run(app, debug=debug, host=host, port=port)
    except KeyboardInterrupt:
        print("\n👋 Shutting down web server...")
    except Exception as e:
        print(f"❌ Error starting web server: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Drug Repositioning Agent Web Interface")
    parser.add_argument("--port", type=int, default=5000, 
                       help="Port to run the web server on (default: 5000)")
    parser.add_argument("--host", default="127.0.0.1", 
                       help="Host to bind the server to (default: 127.0.0.1)")
    parser.add_argument("--debug", action="store_true", default=True,
                       help="Run in debug mode (default: True)")
    parser.add_argument("--production", action="store_true",
                       help="Run in production mode (disables debug)")
    parser.add_argument("--public", action="store_true",
                       help="Make server accessible from other machines (sets host to 0.0.0.0)")
    
    args = parser.parse_args()
    
    # Handle production mode
    if args.production:
        args.debug = False
        print("🚀 Running in production mode")
    
    # Handle public access
    if args.public:
        args.host = "0.0.0.0"
        print("🌍 Server will be accessible from other machines")
    
    # Check if port is in use
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((args.host, args.port))
        except OSError:
            print(f"❌ Port {args.port} is already in use. Try a different port with --port")
            available_port = args.port + 1
            while available_port < args.port + 100:
                try:
                    s.bind((args.host, available_port))
                    print(f"💡 Suggested alternative: --port {available_port}")
                    break
                except OSError:
                    available_port += 1
            sys.exit(1)
    
    print("\n🧬 Drug Repositioning Agent - Web Interface")
    print("=" * 60)
    
    run_web_app(port=args.port, debug=args.debug, host=args.host)

if __name__ == "__main__":
    main() 