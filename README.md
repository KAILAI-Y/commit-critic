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

#### 📊 Example Output
**1. Analysis Report(**`--analyze`**)**
The tool identifies poor practices and suggests context-aware improvements:
![alt text](/images/output_analyze_bad.png)
![alt text](/images/output_analyze_good.png)
![alt text](/images/output_analyze_stats.png)
**2. Interactive Mode (**`--write`**)**
Real-time analysis of your staged changes with smart summaries:
![alt text](/images/output_write.png)