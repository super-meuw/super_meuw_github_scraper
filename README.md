

## 📖 What is super-meuw-github-scraper?

**super-meuw-github-scraper** is a powerful command-line tool that lets you search GitHub repositories by any keyword, view detailed results in a beautiful table, and clone your chosen repositories with just a few keystrokes. It's designed to be fast, user-friendly, and visually appealing with a cute meuw touch!

### Why use this tool?
- 🔍 **Search GitHub** without opening your browser
- 📊 **Beautiful terminal UI** with rich tables and progress bars
- ⬇️ **Clone any repository** using native `git clone` (full history included)
- 🚀 **Batch clone** all results with a single command
- 🔐 **GitHub Token support** to increase API rate limits (5000 requests/hour)
- 📅 **Smart duplicate handling** – adds today's date to folder name if already exists
- 🎨 **Colorful and interactive** experience with ASCII cat banner

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔎 **Smart Search** | Search GitHub repositories by keyword, sorted by stars |
| 📊 **Beautiful Display** | Clean table with repository info (stars, forks, language, description) |
| ⬇️ **One-Click Clone** | Enter a number to clone any repository instantly |
| 📦 **Batch Clone** | Use `ALL` to clone every repository in your search results |
| 🎯 **Progress Tracking** | Real-time progress bars for search and clone operations |
| 🔐 **Token Support** | Optional GitHub token for higher API rate limits (5000/h) |
| 📅 **Duplicate Handling** | Automatically adds date to folder name if a directory already exists |
| 🗂️ **Full Git History** | Uses `git clone` to preserve all commits and branches |
| 🐱 **Meuw Design** | Colorful, cat-themed interface with super-meuw branding |

---

## 📦 Installation

### Prerequisites
- **Python 3.8** or higher
- **Git** installed and available in PATH
- pip (Python package installer)

### Step 1: Install Git (if not already installed)
```bash
# On Debian/Ubuntu/Kali
sudo apt install git

# On macOS (with Homebrew)
brew install git

# On Windows
# Download from https://git-scm.com/download/win

### Step 2: Clone or Download the Tool
```bash
# Clone the repository
git clone https://github.com/super-meuw/super-meuw-github-scraper.git
cd super-meuw-github-scraper

# Or just download the Python file directly
wget https://raw.githubusercontent.com/super-meuw/super-meuw-github-scraper/main/super_meuw_github_scraper.py
```

### Step 3: Install Dependencies

#### Option A: Using Virtual Environment (Recommended)
```bash
# Create and activate virtual environment
python3 -m venv meuw-env
source meuw-env/bin/activate  # On Windows: meuw-env\Scripts\activate

# Install required packages
pip install requests rich
```

#### Option B: Using pipx (For Kali Linux or similar)
```bash
# Install pipx if not already installed
sudo apt install -y pipx
pipx ensurepath

# Install required packages
pipx install requests rich
```

#### Option C: System-wide (Not recommended)
```bash
# ⚠️ This may cause conflicts on some systems
pip install requests rich --break-system-packages
```

---

## 🚀 Usage

### Basic Usage
```bash
python super_meuw_github_scraper.py
```

### Quick Start Guide

1. **Run the tool**:
   ```bash
   python super_meuw_github_scraper.py
   ```

2. **Enter your GitHub token (optional)** when prompted:
   ```
   🔑 GitHub Token (Optional)
   Enter your GitHub Personal Access Token to increase API rate limits.
   Without token: 60 requests/hour
   With token: 5000 requests/hour
   ```
   - Press Enter to skip (use unauthenticated mode)
   - Or paste your token for higher limits

3. **Enter your search term** when prompted:
   ```
   🔍 Enter your search term: fastapi
   ```

4. **View the results** in a beautiful table:
   ```
   ┌───┬─────────────────────┬──────────────┬────────┬────────┬──────────┐
   │ # │ Repository          │ Description  │ ⭐ Stars│ 🔀 Forks│ Language │
   ├───┼─────────────────────┼──────────────┼────────┼────────┼──────────┤
   │ 1 │ tiangolo/fastapi    │ FastAPI...   │ 62,847 │ 5,312  │ Python   │
   │ 2 │ encode/httpx        │ A next-gen  │ 11,234 │ 723    │ Python   │
   └───┴─────────────────────┴──────────────┴────────┴────────┴──────────┘
   ```

5. **Choose what to do**:
   - Enter a **number** (e.g., `1`) to clone that repository
   - Enter `ALL` to clone all repositories
   - Enter `exit` to quit

6. **Watch the clone progress**:
   ```
   🐱 Cloning tiangolo/fastapi...
   📥 Cloning into /home/user/super-meuw-downloads/tiangolo_fastapi...
   ✅ Successfully cloned tiangolo/fastapi!
   📁 Location: /home/user/super-meuw-downloads/tiangolo_fastapi
   ```

### Example Session
```bash
$ python super_meuw_github_scraper.py

                         ,
  ,-.       _,---._ __  / \
 /  )    .-'       `./ /   \
(  (   ,'            `/    /|
 \  `-"             \'\   / |
  `.              ,  \ \ /  |
   /`.          ,'-`----Y   |
  (            ;        |   '
  |  ,-.    ,-'         |  /
  |  | (   |            | /
  )  |  \  `.___________|/
  `--'   `--'

   🐱  SUPER-MEUW GITHUB SCRAPER  🐱
   "Searching the GitHub universe with meuw power!"
   
   Created by: super-meuw

🐾 Ready to search the GitHub universe! 🐾

╭──────────────────────────────────────────────────────────────────── 🔐 Authentication ────────────────────────────────────╮
│ 🔑 GitHub Token (Optional)                                                                                               │
│ Enter your GitHub Personal Access Token to increase API rate limits.                                                     │
│ Without token: 60 requests/hour                                                                                          │
│ With token: 5000 requests/hour                                                                                           │
│                                                                                                                          │
│ How to get a token:                                                                                                      │
│ 1. Go to https://github.com/settings/tokens                                                                              │
│ 2. Click 'Generate new token (classic)'                                                                                  │
│ 3. Give it a name, select 'repo' and 'public_repo' scopes                                                                │
│ 4. Generate and copy the token                                                                                           │
│                                                                                                                          │
│ Press Enter to continue without token                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

Paste your token (or press Enter to skip): 
⚠️  No token provided. Using unauthenticated API (60 requests/hour).

🔍 Enter your search term: machine learning
🔎 Searching for 'machine learning'...
✅ Retrieved 30 repositories (total available: 347)
🐱 Found 30 Meuw-tastic repositories!
... (table displayed here)

👉 Enter your choice: ALL
🐱 Cloning ALL repositories! Hold tight! 🐱
... (clones all repositories)
```

---

## 📁 Output Directory Structure

All cloned repositories are saved in the `super-meuw-downloads/` folder with full Git history:

```
super-meuw-downloads/
├── tiangolo_fastapi/
│   ├── .git/
│   ├── fastapi/
│   ├── tests/
│   └── ...
├── scikit-learn_scikit-learn/
│   ├── .git/
│   ├── sklearn/
│   ├── examples/
│   └── ...
└── ...
```

### Duplicate Handling
If a folder with the same name already exists, the tool automatically adds today's date to the new folder name:

```
super-meuw-downloads/
├── owner_repo/                    # Existing folder
├── 2026-07-23_owner_repo/         # New clone from today
└── ...
```

This prevents overwriting and preserves your work.

---

## 🔑 Getting a GitHub Token (Optional)

To increase your API rate limit from 60 to 5000 requests per hour:

1. Go to [GitHub Settings → Tokens](https://github.com/settings/tokens)
2. Click **"Generate new token (classic)"**
3. Give it a descriptive name (e.g., "super-meuw-scraper")
4. Select the following scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `public_repo` (Access public repositories)
5. Click **"Generate token"**
6. **Copy the token immediately** (you won't see it again!)
7. Paste it when prompted by the tool

> **Note:** You can also press Enter to skip token entry and use the unauthenticated mode (60 requests/hour).

---

## 🛠️ Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **"externally-managed-environment" error** | Use a virtual environment or pipx (see Installation) |
| **"ModuleNotFoundError: No module named 'rich'"** | Install rich: `pip install rich` |
| **"git is not installed"** | Install git: `sudo apt install git` (Linux) or download from git-scm.com |
| **Clone fails with 404 or timeout** | Repository may be private or very large. Check your token permissions. |
| **No results found** | Try a different search term or check your internet connection |
| **Rate limit exceeded** | Use a GitHub token to increase limit to 5000/hour |

### GitHub API Rate Limits
- **Unauthenticated:** 60 requests per hour
- **Authenticated (with token):** 5,000 requests per hour

> **Tip:** Each search request fetches 10 repositories. For 30 results, you need 3 requests. With a token, you can perform up to 5000 requests per hour – plenty for heavy searching!

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Ideas for Contribution
- Add support for cloning specific branches (`--branch`)
- Implement shallow clones (`--depth 1`) for faster downloads
- Add advanced search filters (language, stars range, date)
- Export results to CSV/JSON
- Add a GUI version
- Support for private repositories with SSH keys


---

<div align="center">

**Made by super-meuw**

*"Finding code with the power of meuw!"* 🐱

</div>
```
