#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
super-meuw-github-scraper
A powerful GitHub search & download tool with a cute meuw touch 🐱
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass
from pathlib import Path

import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich import box
from rich.text import Text
from rich.align import Align

# ==================== CONFIGURATION ====================
GITHUB_API_URL = "https://api.github.com"
GITHUB_SEARCH_URL = f"{GITHUB_API_URL}/search/repositories"
TIMEOUT = 15
MAX_RESULTS = 6000  # حداکثر نتایج درخواستی (عملاً گیت‌هاب حداکثر ۱۰۰۰ برمی‌گرداند)
RESULTS_PER_PAGE = 10

# ==================== BANNER ====================
BANNER = """
                         ,
  ,-.       _,---._ __  / \\
 /  )    .-'       `./ /   \\
(  (   ,'            `/    /|
 \\  `-"             \\'\\   / |
  `.              ,  \\ \\ /  |
   /`.          ,'-`----Y   |
  (            ;        |   '
  |  ,-.    ,-'         |  /
  |  | (   |            | /
  )  |  \\  `.___________|/
  `--'   `--'

   🐱  SUPER-MEUW GITHUB SCRAPER  🐱
   "Searching the GitHub universe with meuw power!"
   
   Created by: super-meuw
"""

# ==================== DATA CLASSES ====================
@dataclass
class GitHubRepo:
    """Represents a GitHub repository"""
    name: str
    full_name: str
    description: str
    url: str
    clone_url: str
    stars: int
    forks: int
    language: str
    updated_at: str
    html_url: str

    def __str__(self) -> str:
        return f"{self.full_name} ⭐ {self.stars}"

# ==================== CORE ENGINE ====================
class SuperMeuwGitHubScraper:
    """Main engine for searching and downloading from GitHub"""
    
    def __init__(self):
        self.console = Console()
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "super-meuw-scraper/1.0.0"
        })
        self.search_results: List[GitHubRepo] = []
        self.download_dir = Path.cwd() / "super-meuw-downloads"
        self.download_dir.mkdir(exist_ok=True)
        self.github_token = None
    
    def show_banner(self):
        """Display the super-meuw banner"""
        self.console.print(BANNER, style="bright_magenta")
        self.console.print()
        self.console.print("🐾 Ready to search the GitHub universe! 🐾", style="bold cyan")
        self.console.print()
    
    def get_github_token(self):
        """Ask user for GitHub token and set it in session headers"""
        self.console.print(Panel(
            "[bold yellow]🔑 GitHub Token (Optional)[/bold yellow]\n"
            "Enter your GitHub Personal Access Token to increase API rate limits.\n"
            "Without token: 60 requests/hour\n"
            "With token: 5000 requests/hour\n\n"
            "[dim]How to get a token:[/dim]\n"
            "1. Go to [blue]https://github.com/settings/tokens[/blue]\n"
            "2. Click 'Generate new token (classic)'\n"
            "3. Give it a name, select 'repo' and 'public_repo' scopes\n"
            "4. Generate and copy the token\n\n"
            "[dim]Press Enter to continue without token[/dim]",
            title="🔐 Authentication",
            border_style="bright_blue"
        ))
        
        token = Prompt.ask("\n[bold cyan]Paste your token (or press Enter to skip)[/bold cyan]", default="")
        if token.strip():
            self.github_token = token.strip()
            self.session.headers.update({
                "Authorization": f"token {self.github_token}"
            })
            self.console.print("[green]✅ Token set successfully! Rate limit increased to 5000 requests/hour.[/green]")
        else:
            self.console.print("[yellow]⚠️  No token provided. Using unauthenticated API (60 requests/hour).[/yellow]")
        self.console.print()
    
    def search_github(self, query: str) -> List[GitHubRepo]:
        """Search GitHub repositories based on query with pagination up to MAX_RESULTS"""
        repos = []
        page = 1
        fetched = 0
        total_available = None
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console
        ) as progress:
            task = progress.add_task(
                f"[cyan]🔎 Searching GitHub for '{query}'...",
                total=MAX_RESULTS
            )
            
            while fetched < MAX_RESULTS:
                params = {
                    "q": query,
                    "sort": "stars",
                    "order": "desc",
                    "per_page": RESULTS_PER_PAGE,
                    "page": page
                }
                
                try:
                    response = self.session.get(
                        GITHUB_SEARCH_URL,
                        params=params,
                        timeout=TIMEOUT
                    )
                    response.raise_for_status()
                    data = response.json()
                    
                    # Check total count
                    if total_available is None:
                        total_available = data.get("total_count", 0)
                        if total_available > MAX_RESULTS:
                            total_available = MAX_RESULTS
                        progress.update(task, total=min(total_available, MAX_RESULTS))
                    
                    items = data.get("items")
                    if not items:
                        break
                    
                    for item in items:
                        if fetched >= MAX_RESULTS:
                            break
                        
                        # Safely get description and language
                        description = item.get("description") or "No description"
                        language = item.get("language") or "Unknown"
                        
                        repo = GitHubRepo(
                            name=item["name"],
                            full_name=item["full_name"],
                            description=description,
                            url=item["url"],
                            clone_url=item["clone_url"],
                            stars=item["stargazers_count"],
                            forks=item["forks_count"],
                            language=language,
                            updated_at=item["updated_at"],
                            html_url=item["html_url"]
                        )
                        repos.append(repo)
                        fetched += 1
                        progress.update(task, advance=1)
                    
                    # Check if we've reached the end
                    if len(items) < RESULTS_PER_PAGE or fetched >= total_available:
                        break
                    
                    page += 1
                    time.sleep(0.5)  # Be nice to GitHub API
                    
                except requests.exceptions.RequestException as e:
                    self.console.print(f"[red]Error searching GitHub: {e}[/red]")
                    break
                except KeyError as e:
                    self.console.print(f"[red]Error parsing response: {e}[/red]")
                    break
            
            if not repos and total_available == 0:
                self.console.print("[yellow]No results found for your query.[/yellow]")
            elif repos:
                self.console.print(f"[dim]✅ Retrieved {len(repos)} repositories (total available: {min(total_available, MAX_RESULTS)})[/dim]")
        
        return repos
    
    def display_results(self, repos: List[GitHubRepo]):
        """Display search results in a beautiful table"""
        if not repos:
            self.console.print("[yellow]😿 No results found. Try a different query![/yellow]")
            return
        
        table = Table(
            title=f"🐱 Found {len(repos)} Meuw-tastic repositories!",
            box=box.ROUNDED,
            border_style="bright_cyan",
            header_style="bold magenta",
            show_lines=True
        )
        
        table.add_column("#", style="dim", width=4)
        table.add_column("Repository", style="cyan", no_wrap=True)
        table.add_column("Description", style="white", max_width=40)
        table.add_column("⭐ Stars", style="bright_yellow", justify="right")
        table.add_column("🔀 Forks", style="bright_green", justify="right")
        table.add_column("Language", style="bright_blue")
        
        for idx, repo in enumerate(repos, 1):
            # Truncate description if too long
            desc = repo.description[:60] + "..." if len(repo.description) > 60 else repo.description
            table.add_row(
                str(idx),
                repo.full_name,
                desc,
                f"{repo.stars:,}",
                f"{repo.forks:,}",
                repo.language
            )
        
        self.console.print(table)
        self.console.print()
        
        self.console.print("[dim]💡 Tip: Enter a number to download, 'ALL' for all, or 'exit' to quit[/dim]")
    
    def download_repo(self, repo: GitHubRepo) -> bool:
        """Download a repository using git clone with duplicate name handling"""
        try:
            self.console.print(f"\n[cyan]🐱 Cloning {repo.full_name}...[/cyan]")
            
            # Base folder name
            base_name = repo.full_name.replace("/", "_")
            dest_path = self.download_dir / base_name
            
            # Check if folder already exists
            if dest_path.exists():
                # Add today's date to folder name
                today = datetime.now().strftime("%Y-%m-%d")
                new_name = f"{today}_{base_name}"
                dest_path = self.download_dir / new_name
                self.console.print(f"[yellow]⚠️  Folder '{base_name}' already exists. Using '{new_name}' instead.[/yellow]")
            
            # Clone the repository using git
            self.console.print(f"[cyan]📥 Cloning into {dest_path}...[/cyan]")
            
            # Run git clone command
            result = subprocess.run(
                ["git", "clone", repo.clone_url, str(dest_path)],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout for large repos
            )
            
            if result.returncode == 0:
                self.console.print(f"[green]✅ Successfully cloned {repo.full_name}![/green]")
                self.console.print(f"[dim]📁 Location: {dest_path}[/dim]")
                return True
            else:
                error_msg = result.stderr.strip()
                self.console.print(f"[red]❌ Git clone failed: {error_msg}[/red]")
                return False
                
        except subprocess.TimeoutExpired:
            self.console.print(f"[red]❌ Clone timeout for {repo.full_name} (took more than 5 minutes)[/red]")
            return False
        except Exception as e:
            self.console.print(f"[red]❌ Error cloning {repo.full_name}: {e}[/red]")
            return False
    
    def download_all(self, repos: List[GitHubRepo]):
        """Download all repositories in the list"""
        self.console.print("\n[bold cyan]🐱 Cloning ALL repositories! Hold tight! 🐱[/bold cyan]")
        
        success_count = 0
        for idx, repo in enumerate(repos, 1):
            self.console.print(f"\n[dim]Processing {idx}/{len(repos)}...[/dim]")
            if self.download_repo(repo):
                success_count += 1
            time.sleep(1)  # Be nice to GitHub
        
        self.console.print(f"\n[bold green]✅ Cloned {success_count}/{len(repos)} repositories successfully![/bold green]")
    
    def run(self):
        """Main application loop"""
        self.show_banner()
        self.get_github_token()
        
        while True:
            query = Prompt.ask(
                "\n[bold cyan]🔍 Enter your search term[/bold cyan]",
                default="python"
            )
            
            if query.lower() in ['exit', 'quit', 'q']:
                self.console.print("\n[yellow]🐱 Meuw! Goodbye! 🐱[/yellow]")
                break
            
            self.console.print(f"\n[cyan]🔎 Searching for '{query}'...[/cyan]")
            repos = self.search_github(query)
            
            if not repos:
                self.console.print("[yellow]😿 No results found. Try again![/yellow]")
                continue
            
            self.search_results = repos
            self.display_results(repos)
            
            while True:
                choice = Prompt.ask(
                    "\n[bold yellow]👉 Enter your choice[/bold yellow]",
                    default="exit"
                )
                
                if choice.lower() == 'exit':
                    self.console.print("\n[yellow]🐱 Meuw! Goodbye! 🐱[/yellow]")
                    return
                
                if choice.upper() == 'ALL':
                    self.download_all(repos)
                    break
                
                try:
                    idx = int(choice)
                    if 1 <= idx <= len(repos):
                        repo = repos[idx - 1]
                        self.download_repo(repo)
                        break
                    else:
                        self.console.print(
                            f"[red]Please enter a number between 1 and {len(repos)}, ALL, or exit[/red]"
                        )
                except ValueError:
                    self.console.print("[red]Invalid input! Enter a number, ALL, or exit[/red]")
            
            again = Prompt.ask(
                "\n[cyan]🔍 Search again?[/cyan]",
                choices=["y", "n"],
                default="y"
            )
            if again.lower() != 'y':
                self.console.print("\n[yellow]🐱 Meuw! Happy coding! 🐱[/yellow]")
                break

# ==================== MAIN ENTRY POINT ====================
def main():
    """Main entry point for the application"""
    try:
        try:
            import rich
        except ImportError:
            print("❌ Required package 'rich' not found!")
            print("📦 Install it with: pip install rich")
            sys.exit(1)
        
        # Check if git is installed
        try:
            subprocess.run(["git", "--version"], capture_output=True, check=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            console = Console()
            console.print("[red]❌ Git is not installed or not in PATH![/red]")
            console.print("[yellow]Please install git first: sudo apt install git[/yellow]")
            sys.exit(1)
        
        scraper = SuperMeuwGitHubScraper()
        scraper.run()
        
    except KeyboardInterrupt:
        console = Console()
        console.print("\n[yellow]🐱 Meuw! Interrupted! Goodbye! 🐱[/yellow]")
        sys.exit(0)
    except Exception as e:
        console = Console()
        console.print(f"\n[red]❌ An unexpected error occurred: {e}[/red]")
        console.print("[dim]Please report this issue to super-meuw[/dim]")
        sys.exit(1)

if __name__ == "__main__":
    main()
