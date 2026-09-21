@echo off
REM Run script for Supply Chain Intelligence Platform Dashboard
REM This script runs the dashboard from the project root directory to avoid import issues.

title Supply Chain Intelligence Platform Dashboard

SET PROJECT_ROOT=D:\GITHUB\Supply-Chain-Intelligence-Platform
SET DASHBOARD_PATH=%PROJECT_ROOT%\app\dashboard\app.py

echo.
echo ============================================================
echo 🔧 Supply Chain Intelligence Platform Dashboard
ECHO ============================================================
echo.

echo 📂 Project root: %PROJECT_ROOT%
echo 📄 Dashboard file: %DASHBOARD_PATH%
echo.

if not exist "%DASHBOARD_PATH%" (
    echo ❌ ERROR: Dashboard file not found at %DASHBOARD_PATH%
    goto :error_exit
)

echo 🔍 Testing package imports...
python -c "
import sys
import os
project_root = r'%PROJECT_ROOT%'
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    import app
    print('✅ Successfully imported app package')
except ImportError as e:
    print(f'❌ Failed to import app package: {e}')
    sys.exit(1)
"

if errorlevel neq 0 (
    echo ❌ Package import failed. Exiting...
    goto :error_exit
)

echo.
echo 🚀 Starting Streamlit dashboard...
echo 📡 Server will be available at: http://localhost:8501
echo.
echo ============================================================
echo Note: Run streamlit from the project root directory:
echo cd /d %PROJECT_ROOT%
echo streamlit run app/dashboard/app.py
echo ============================================================
echo.

:run_streamlit
cd /d "%PROJECT_ROOT%"
streamlit run app/dashboard/app.py
if errorlevel neq 0 (
    echo.
    echo ❌ Streamlit exited with error. Exiting...
    goto :error_exit
)

:error_exit
echo.
echo ❌ Error occurred. Please check the output above for details.
echo.
pause
exit /b 1