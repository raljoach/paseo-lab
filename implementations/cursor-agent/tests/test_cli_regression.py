import subprocess
import sys


def test_cli_runs():
    result = subprocess.run(
        [
            sys.executable,
            "app/main.py",
            "--destination",
            "Andorra",
            "--budget",
            "300",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Paseo FAST Itinerary" in result.stdout