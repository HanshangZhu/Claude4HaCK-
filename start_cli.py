#!/usr/bin/env python3
"""
Startup script for Drug Repositioning Agent CLI interfaces
"""

import sys
import os
import argparse
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import rich
        import click
        return True
    except ImportError:
        return False

def install_dependencies():
    """Install required dependencies"""
    print("Installing required dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def run_enhanced_cli(dry_run=False):
    """Run the enhanced CLI with rich formatting"""
    if not check_dependencies():
        print("Enhanced CLI dependencies not found. Installing...")
        install_dependencies()
    
    from enhanced_cli import main
    sys.argv = ["enhanced_cli.py"]
    if dry_run:
        sys.argv.append("--dry-run")
    main()

def run_simple_cli():
    """Run the simple real-time CLI"""
    from realtime_demo import main
    main()

def main():
    parser = argparse.ArgumentParser(description="Drug Repositioning Agent CLI Launcher")
    parser.add_argument("--enhanced", action="store_true", 
                       help="Use the enhanced CLI with rich formatting")
    parser.add_argument("--simple", action="store_true", 
                       help="Use the simple real-time CLI")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Run in dry-run mode with simulated data")
    
    args = parser.parse_args()
    
    if args.enhanced:
        print("🧬 Starting Enhanced CLI Interface...")
        run_enhanced_cli(dry_run=args.dry_run)
    elif args.simple:
        print("🧬 Starting Simple CLI Interface...")
        run_simple_cli()
    else:
        # Interactive selection
        print("\n🧬 Drug Repositioning Agent - CLI Interface Selection")
        print("=" * 60)
        print("1. Enhanced CLI (Rich formatting, menus, progress bars)")
        print("2. Simple CLI (Basic real-time interface)")
        print("3. Exit")
        
        while True:
            choice = input("\nSelect interface (1-3): ").strip()
            
            if choice == "1":
                print("\n🎨 Starting Enhanced CLI Interface...")
                run_enhanced_cli(dry_run=args.dry_run)
                break
            elif choice == "2":
                print("\n⚡ Starting Simple CLI Interface...")
                run_simple_cli()
                break
            elif choice == "3":
                print("👋 Goodbye!")
                sys.exit(0)
            else:
                print("❌ Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main() 