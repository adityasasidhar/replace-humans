import subprocess

def run_command(command):
    """Run a terminal command and return its output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode