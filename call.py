import subprocess
import os
import sys

def call_batch_script(batch_file, repo_path):
    # Ensure the path is properly formatted
    repo_path = os.path.abspath(repo_path)  # Convert to absolute path
    # Call the batch file
    try:
        result = subprocess.run([batch_file, repo_path], check=True)
        print("Batch script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing batch script: {e}")

if __name__ == "__main__":
    
    # Check if a repository path was provided
    if len(sys.argv) != 2:
        print("Usage: python caller.py <repo_path>")
        sys.exit(1)
    
    # Get the repository path from command-line arguments
    repo_path = sys.argv[1]
    
    #repo_path = r'C:\Users\Test\Documents\GitHub\Test2024EEP\Test2024EEP'
    # Specify the path to your batch file
    batch_file = r"C:\Users\Test\Documents\GitHub\Test2024EEP\git_command.bat"
    
    # Call the batch script with the provided repository path
    call_batch_script(batch_file, repo_path)
