#!/usr/bin/env python3
import sys
sys.path.append('D:\GITHUB\Supply-Chain-Intelligence-Platform')

try:
    # Test importing the app package
    import app
    print("✓ Successfully imported app package")
    
    # Test importing dashboard modules
    from app.dashboard.pages import home, companies, graph, risk, analytics, ai_assistant
    print("✓ Successfully imported dashboard pages")
    
    # Test importing dashboard queries
    from app.dashboard.dashboard_queries import DashboardQueries
    print("✓ Successfully imported DashboardQueries")
    
    print("\n✅ All imports successful! The package structure is correct.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)