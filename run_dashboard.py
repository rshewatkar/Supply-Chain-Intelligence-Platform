#!/usr/bin/env python3
"""
Run script for Supply Chain Intelligence Platform Dashboard

This script runs the dashboard from the project root directory to avoid import issues.
"""

import os
import subprocess
import sys

def main():
    print("🔧 Supply Chain Intelligence Platform Dashboard")
    print("=" * 60)
    
    # Get the project root directory
    project_root = "D:\GITHUB\Supply-Chain-Intelligence-Platform"
    dashboard_path = os.path.join(project_root, "app", "dashboard", "app.py")
    
    print(f"Project root: {project_root}")
    print(f"Dashboard file: {dashboard_path}")
    
    # Check if dashboard exists
    if not os.path.exists(dashboard_path):
        print(f"❌ ERROR: Dashboard file not found at {dashboard_path}")
        return 1
    
    # Check if streamlit is available
    try:
        import streamlit
        print(f"✅ Streamlit version: {streamlit.__version__}")
    except ImportError:
        print("❌ ERROR: Streamlit is not installed")
        print("   Install it with: pip install streamlit")
        return 1
    
    # Change to project root directory
    print(f"\n📂 Changing to project root directory...")
    os.chdir(project_root)
    
    # Check if we can import the app package
    print(f"\n🔍 Testing package imports...")
    try:
        import app
        print("✅ Successfully imported app package")
    except ImportError as e:
        print(f"❌ Failed to import app package: {e}")
        print("   This indicates a package configuration issue.")
        return 1
    
    # Run streamlit from the project root
    print(f"\n🚀 Starting Streamlit dashboard...")
    print(f"   Run command: streamlit run app/dashboard/app.py")
    print(f"   Server will be available at: http://localhost:8501")
    print("\n" + "=" * 60)
    
    try:
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", 
            "run", "app/dashboard/app.py"
        ], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Streamlit exited with error: {e}")
        return 1
    except KeyboardInterrupt:
        print(f"\n👋 Streamlit stopped by user")
        return 0
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)