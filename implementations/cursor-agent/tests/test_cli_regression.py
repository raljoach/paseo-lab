import subprocess
import sys


def test_cli_runs():
    result = subprocess.run(
        [
            sys.executable,
            "implementations/cursor-agent/app/main.py",
            "cheap trip under 300 to Andorra",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Paseo FAST Itinerary" in result.stdout