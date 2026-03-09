import os
import subprocess
import shutil
import stat
from pathlib import Path

def run_cmd(cmd, cwd=None):
    subprocess.run(cmd, cwd=cwd, shell=True, check=True)

def on_rm_error(func, path, exc_info):
    # Set write permission and retry
    os.chmod(path, stat.S_IWRITE)
    func(path)

def setup():
    test_dir = Path("test_repo")
    if test_dir.exists():
        shutil.rmtree(test_dir, onerror=on_rm_error)
    
    test_dir.mkdir()
    print(f"Subdirectory '{test_dir}' created.")

    # Initialize git
    run_cmd("git init", cwd=test_dir)
    
    # Create a "base" file
    base_code = """def login(username, password):
    # Missing input validation
    query = f"SELECT * FROM users WHERE user='{username}' AND pass='{password}'"
    print(f"Executing: {query}")
    return True

if __name__ == '__main__':
    login('admin', '12345')
"""
    (test_dir / "app.py").write_text(base_code)
    
    # Commit base
    run_cmd("git add app.py", cwd=test_dir)
    run_cmd('git commit -m "Initial commit"', cwd=test_dir)
    
    # Create a "change" with a bug/code smell
    new_code = """def login(username, password):
    # Still missing input validation - SQL Injection risk!
    query = f"SELECT * FROM users WHERE user='{username}' AND pass='{password}'"
    print(f"Executing: {query}")
    return True

def process_data(data):
    # Potentially slow/buggy function
    result = []
    for i in range(len(data)):
        for j in range(len(data)):
            result.append(data[i] + data[j])
    return result

if __name__ == '__main__':
    login('admin', '12345')
    print(process_data([1, 2, 3]))
"""
    (test_dir / "app.py").write_text(new_code)
    
    # Add another file
    (test_dir / "utils.py").write_text("def helper():\n    pass\n")
    run_cmd("git add utils.py", cwd=test_dir)
    
    print("\n" + "=" * 60)
    print("  OK  TEST REPOSITORY READY")
    print("=" * 60)
    print(f"Location: {test_dir.resolve()}")
    print("Changes: Modified 'app.py' (SQL injection) and added 'utils.py' (staged).")
    print("\nYou can now run:")
    print(f"  python cli.py review {test_dir}")

if __name__ == "__main__":
    setup()
