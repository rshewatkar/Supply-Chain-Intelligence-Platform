#!/usr/bin/env python3
"""
Fix script for ModuleNotFoundError: No module named 'app.dashboard'; 'app' is not a package

This script diagnoses and fixes the import issues in the Supply Chain Intelligence Platform.
"""

import os
import sys
import importlib

def print_header(title):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")

def check_current_directory():
    print_header("Step 1: Checking Current Directory")
    
    current_dir = os.getcwd()
    project_root = "D:\GITHUB\Supply-Chain-Intelligence-Platform"
    
    print(f"Current working directory: {current_dir}")
    print(f"Project root directory: {project_root}")
    
    if current_dir != project_root:
        print(f"⚠️  WARNING: Not running from project root")
        print(f"   This can cause import issues when using package names like 'app.dashboard.pages.home'")
        print(f"   Recommended: Change to project root or fix import paths")
        return False
    else:
        print(f"✅ Good: Running from project root")
        return True