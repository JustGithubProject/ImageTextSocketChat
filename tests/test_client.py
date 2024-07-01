import subprocess
import time


def test_client_1_runs():
    try:
        proc = subprocess.Popen(['python', 'client_1/client.py'])
        time.sleep(2)

        assert proc.poll() is None, "Client script did not start or exited prematurely"
        
        time.sleep(5)
        proc.terminate()
        proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        assert False, "Client script did not terminate within timeout"



def test_client_2_runs():
    try:
        proc = subprocess.Popen(['python', 'client_2/client.py'])
        time.sleep(2)

        assert proc.poll() is None, "Client script did not start or exited prematurely"
        
        time.sleep(5)
        proc.terminate()
        proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        assert False, "Client script did not terminate within timeout"