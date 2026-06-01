import subprocess
import sys

def test_orchestration_end_to_end():
    result = subprocess.run(
    [
    sys.executable,
    "implementations/cursor-agent/app/main.py",
    "cheap relaxing trip under 500 to Andorra",
    ],
    capture_output=True,
    text=True,
    )


    assert result.returncode == 0

    output = result.stdout

    assert "Andorra" in output
    assert "Paseo FAST Itinerary" in output
    assert "budget" not in output.lower()

