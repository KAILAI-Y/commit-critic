import subprocess
import os
import tempfile
import shutil

def get_last_commits(count=50):
    """
    Get the recent commit history, with a summary of changed files,
    so that the AI can give more accurate suggestions based on the changed files.
    """
    try:
        # %h: abbreviated hash, %s: subject, %b: body
        # --name-status: show file names and status of changes (Added, Modified, Deleted)
        cmd = [
            "git", "log", 
            f"-n {count}", 
            "--pretty=format:COMMIT_START|%h|%s|%b|FILES:",
            "--name-status" 
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Split the output by custom delimiter
        raw_commits = result.stdout.split("COMMIT_START|")
        commits = [c.strip() for c in raw_commits if c.strip()]
        return commits
    except subprocess.CalledProcessError:
        return []

def get_staged_diff():
    """
    Get code differences in the staging area (for --write mode).
    This is the core data source for the AI to write high-quality commit messages.
    """
    try:
        cmd = ["git", "diff", "--staged"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return ""

def clone_remote_repo(repo_url):
    """
    Clone a remote repository to a temporary directory.
    """
    tmp_dir = tempfile.mkdtemp()
    try:
        # --depth 50 greatly improves cloning speed
        cmd = ["git", "clone", "--depth", "50", "--quiet", repo_url, tmp_dir]
        subprocess.run(cmd, check=True)
        return tmp_dir
    except subprocess.CalledProcessError as e:
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        raise Exception(f"Failed to clone remote repository: {e}")
    
def get_diff_stats():
    """
    Get statistics of the staging area.
    Example output format: "1 file changed, 1 insertion(+), 1 deletion(-)"
    """
    try:
        # --shortstat only shows summary of file count and line changes
        cmd = ["git", "diff", "--staged", "--shortstat"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        output = result.stdout.strip()
        # If there is no output (meaning no changes), return the default value
        return output if output else "No changes detected"
    except subprocess.CalledProcessError:
        return "Error getting stats"

def cleanup_repo(dir_path):
    """
    Clean up temporary folders.
    """
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)