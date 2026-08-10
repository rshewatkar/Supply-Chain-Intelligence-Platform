import subprocess
import sys
from pathlib import Path


def main():
    """
    Launch the Supply Chain Intelligence Streamlit dashboard.
    """

    dashboard_path = (
        Path(__file__).resolve().parent.parent
        / "app"
        / "dashboard"
        / "graph_dashboard.py"
    )

    if not dashboard_path.exists():
        print(
            f"Dashboard file not found:\n"
            f"{dashboard_path}"
        )
        sys.exit(1)

    print("=" * 60)
    print("Supply Chain Intelligence Platform")
    print("Graph Analytics Dashboard")
    print("=" * 60)

    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(dashboard_path),
        ],
        check=True,
    )


if __name__ == "__main__":
    main()