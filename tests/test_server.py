import subprocess
import time


def test_server_runs():
    try:
        proc = subprocess.Popen(['python', 'your_server_script.py'])
        time.sleep(2)

        assert proc.poll() is None, "Server script did not start or exited prematurely"
        
        time.sleep(5)
        proc.terminate()
        proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        assert False, "Server script did not terminate within timeout"

if __name__ == "__main__":
    pytest.main()
