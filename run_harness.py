import os
import sys
import datetime
import subprocess

def run_behave(tags=None):
    """Run behave tests with optional tags."""
    cmd = ["behave"]
    if tags:
        cmd += ["-t", tags]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("ERRORS:", result.stderr, file=sys.stderr)


def hil_module_available():
    """Check if typhoon HIL API is available."""
    try:
        import typhoon.api.hil as hil
        return True
    except ImportError:
        return False


def main():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"=== Test Harness Started at {timestamp} ===")

    if hil_module_available():
        print("[INFO] Typhoon HIL API detected ✅ Running all tests...")
        run_behave()
    else:
        print("[WARNING] Typhoon HIL API not found ⚠️ Skipping HIL tests...")
        print("[INFO] Running only non-HIL tagged tests...")
        run_behave(tags="~hil")  # run tests that are NOT tagged @hil

    print("=== Test Harness Finished ===")


if __name__ == "__main__":
    main()
