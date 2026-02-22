## 🤖 AI Git Commit Critic 🚀
An AI-powered terminal tool designed to elevate Git workflow quality. It analyzes commit history, critiques message clarity using file-change context, and assists developers in writing perfect Conventional Commits.

#### 🌟 Key Features
- **🔍 Analysis Mode (**`--analyze`**)**: Reviews the last 50 commits. It doesn't just look at text; it correlates messages with modified files to provide accurate "Better" suggestions.

- **🌍 Remote Repository Support**: Analyze any public GitHub repository by providing its URL.

- **✍️ Interactive Writer (**`--write`**)**: Analyzes git diff --staged to suggest structured commit messages, including a summary of detected changes.

- **📊 Quality Metrics**: Generates stats on "vague" vs. "descriptive" commits and calculates an overall repository health score.

#### 🛠️ Tech Stack
- **Language**: Python 3.9+

- **LLM**: Google Gemini 2.5 Flash 

- **CLI UI**: [Rich](https://github.com/Textualize/rich) for advanced terminal formatting and status spinners.

- **Environment**: `python-dotenv` for secure API key management.

#### 🚀 Quick Start
**1. Installation**
```bash
git clone https://github.com/KAILAI-Y/commit-critic
cd commit-critic

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**2. Configuration**
Create a `.env` file in the root directory:

```Code snippet
GEMINI_API_KEY=your_api_key_here
```

**3. Usage**
```Bash
# Analyze current repository
python commit_critic.py --analyze

# Analyze a remote repository
python commit_critic.py --analyze --url="<GITHUB_REPO_URL>"

# Generate a commit message for staged changes
git add .
python commit_critic.py --write
```
#### 🛠️ Global Integration 
You can use this tool as a global Git extension to maintain high-quality commit standards across all your local projects.

**1. Ensure Path Independence**
To allow the script to find your API key from any directory, ensure llm_service.py uses absolute path resolution for the `.env` file:

```Python
from pathlib import Path
from dotenv import load_dotenv

# Force search for .env in the script's home directory
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
```

**2. Set Up Global Aliases**
Add these to your shell configuration file (e.g.,` ~/.zshrc` or `~/.bashrc`) using the path to your project's virtual environment. This ensures all dependencies like `google-genai` are always available。

```Bash
# Replace [PATH_TO_PROJECT] with your actual project directory
alias gcw='/[PATH_TO_PROJECT]/venv/bin/python /[PATH_TO_PROJECT]/commit_critic.py --write'
alias gca='/[PATH_TO_PROJECT]/venv/bin/python /[PATH_TO_PROJECT]/commit_critic.py --analyze'
```
**3. Usage Anywhere**
After running `source ~/.zshrc`, you can navigate to any Git repository on your machine and run:

- **gcw**: To generate a perfect commit message for your staged changes.

- **gca**: To audit the history of the current repository.

#### 📊 Example Output
**1. Analysis Report(**`--analyze`**)**
The tool identifies poor practices and suggests context-aware improvements:
![alt text](/images/output_analyze_bad.png)
![alt text](/images/output_analyze_good.png)
![alt text](/images/output_analyze_stats.png)
**2. Interactive Mode (**`--write`**)**
Real-time analysis of your staged changes with smart summaries:
![alt text](/images/output_write.png)