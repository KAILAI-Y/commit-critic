import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

class CommitAI:
    def __init__(self):
        # Ensure API KEY is in environment variables
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Error: GEMINI_API_KEY not found in .env file")
            
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.5-flash" 

    def analyze_commits(self, commit_logs: str) -> str:
        """
        Analyze historical commit records.
        The input includes the message of each commit and its modified file name.
        """
        prompt = f"""
        You are a highly critical Senior Software Engineer. I will provide a list of recent git commits. 
        Each commit starts with 'COMMIT_START|' and includes the hash, message, and a list of changed files after 'FILES:'.

        TASK:
        1. Critique the commit messages.
        2. Identify the worst offenders (vague, no type, one-word).
        3. Identify the best examples (follows Conventional Commits, descriptive).
        4. Provide stats.

        RULES FOR YOUR CRITIQUE:
        - If FILES includes 'auth.py' and msg is 'fix bug', Better is 'fix(auth): resolve token expiration'
        - If FILES includes 'README.md' and msg is 'update', Better is 'docs(readme): update installation guide'
        - BE PRECISE. Use the filenames to guess the 'scope'.
        - SCORING: 1/10 for "wip" or "update". 9/10 for clear, scoped messages.
        
        OUTPUT FORMAT (Strictly follow this with emojis):
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        💩 COMMITS THAT NEED WORK
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        Commit: "[original msg]"
        Score: [X]/10
        Issue: [One sentence under 15 words describing the issue, sharp, e.g., 'Too vague - which bug?']
        Better: "[Specific suggestion using the FILES context]"

        (Repeat for bad commits...)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        💎 WELL-WRITTEN COMMITS
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        Commit: "[orignal msg]"
        Score: [X]/10
        Why it's good: [Come phrase to summarize the strength, like 'Clear scope', 'specific changes', 'measurable impact']

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        📊 YOUR STATS
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        Average score: [X].X/10
        Vague commits: [X] ([X]%)
        One-word commits: [X] ([X]%)

        COMMITS DATA:
        {commit_logs}
        """
        
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt
        )
        return response.text

    def suggest_commit(self, diff_text: str) -> str:
        """
        Generate an accurate commit message based on the diff of the current staging area.
        """
        # Truncate the first 10000 characters to prevent exceeding the Token limit
        diff_context = diff_text[:10000] 
        
        prompt = f"""
        You are an expert at writing Conventional Commits. Based on the following git diff, 
        write a concise and professional commit message.

        STRICT OUTPUT FORMAT:
        Changes detected:
        - [Point 1: e.g., Modified authentication logic]
        - [Point 2: e.g., Added error handling]

        Suggested commit message:
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        [type]([scope]): [short summary]

        - [Detail 1]
        - [Detail 2]
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        INSTRUCTIONS:
        - Identify 2-3 main high-level changes for 'Changes detected'.
        - Use Conventional Commits for the suggested message.
        - Do not use markdown blocks.

        GIT DIFF:
        {diff_context}
        """
        
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt
        )
        return response.text.strip()