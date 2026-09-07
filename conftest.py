"""
Pytest configuration and fixtures for Supply Chain Intelligence Platform.

This file ensures that the project root is in the Python path so that
the 'app' module can be imported correctly.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
