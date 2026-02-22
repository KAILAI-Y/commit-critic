import argparse
import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.spinner import Spinner
from git_utils import get_diff_stats, get_last_commits, get_staged_diff, clone_remote_repo
from llm_service import CommitAI

console = Console()

def main():
    parser = argparse.ArgumentParser(description="AI Commit Message Critic Challenge")
    parser.add_argument("--analyze", action="store_true", help="Analyze the quality of commit history")
    parser.add_argument("--write", action="store_true", help="Generate commit message based on staged changes")
    parser.add_argument("--url", type=str, help="Remote repository URL (used with --analyze)")
    
    args = parser.parse_args()
    ai = CommitAI()

    # --- Mode 1: Analysis Mode ---
    if args.analyze:
        repo_name = "Current Repository"
        original_cwd = os.getcwd()

        # If a remote URL is provided
        if args.url:
            try:
                with console.status(f"[bold green]Cloning remote repository: {args.url}..."):
                    tmp_dir = clone_remote_repo(args.url)
                    os.chdir(tmp_dir)
                    repo_name = args.url
            except Exception as e:
                console.print(f"[red]Error: Unable to clone remote repository. {e}[/red]")
                return

        try:
            with console.status(f"[bold blue]Fetching last 50 commits from {repo_name} and analyzing..."):
                commits = get_last_commits(50)
                if not commits or len(commits) < 1:
                    console.print("[yellow]No commit history found.[/yellow]")
                    return
                
                # Call AI for analysis
                analysis_report = ai.analyze_commits("\n".join(commits))
                
                # Print the result directly 
                console.print(analysis_report)
        finally:
            if args.url:
                os.chdir(original_cwd) # Change back to the original directory after finishing

    # --- Mode 2: Interactive Writing Mode ---
    elif args.write:
        stats = get_diff_stats()

        console.print(f"\n[bold]Analyzing staged changes...[/bold] ([magenta]{stats}[/magenta])")
    
        with console.status("[bold magenta]Analyzing staged changes..."):
            diff = get_staged_diff()
            
        if not diff or diff.strip() == "":
            console.print("[yellow]⚠️  No staged changes to analyze.[/yellow]")
            return
        
        with console.status("[bold cyan]Generating suggestion..."):
            suggestion_text = ai.suggest_commit(diff)
        
        console.print(f"\n{suggestion_text}")

        user_input = console.input("\nPress [bold green]Enter[/bold green] to accept, or type your own message: \n> ")
        
        import subprocess
        try:
            if user_input.strip() == "":
                # User accepted the suggestion, parse it
                try:
                    commit_block = suggestion_text.split("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")[1].strip()
                    message_lines = commit_block.split('\n', 1)
                    commit_summary = message_lines[0].strip()
                    commit_body = message_lines[1].strip() if len(message_lines) > 1 else ""
                    
                    commit_args = ["git", "commit", "-m", commit_summary]
                    if commit_body:
                        commit_args.extend(["-m", commit_body])
                    
                    subprocess.run(commit_args, check=True)

                except IndexError:
                    # Fallback for safety if parsing fails
                    subprocess.run(["git", "commit", "-m", suggestion_text], check=True)
            else:
                # User provided their own message
                subprocess.run(["git", "commit", "-m", user_input], check=True)

            console.print("\n[bold green]✅ Commit successful![/bold green]")
        except subprocess.CalledProcessError:
            console.print("\n[bold red]❌ Commit failed, please check git status.[/bold red]")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()