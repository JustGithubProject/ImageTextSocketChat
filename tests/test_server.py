# tests/test_temp.py
import subprocess


def test_server_runs():
    try:
        result = subprocess.run(['python', 'server.py'], check=True)
    except subprocess.CalledProcessError as e:
        assert False, f"Server script failed with error: {e}"
    else:
        assert result.returncode == 0, "Server script did not exit cleanly"