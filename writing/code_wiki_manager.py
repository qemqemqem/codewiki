import os
import random
from pathlib import Path
from typing import List, Dict, Optional

from code_handling.repoman import RepoList
from code_handling.repoman import analyze_directory
from formatting.formatting import sanitize_article_name
from writing.article import Article
from writing.wiki_manager import WikiManager


class CodeWikiManager(WikiManager):
    def __init__(self, wiki_name: str, wiki_path: Path, code_path: Path):
        super().__init__(wiki_name, wiki_path)
        self.code_path: Path = code_path

        # Load the code
        # TODO pass these in as parameters
        excluded_directories = ["Card Examples", "sets", "assets", ".git"]
        excluded_extensions = ['.log', '.tmp', '.png', '.txt']
        self.code: RepoList = analyze_directory(code_path, excluded_directories, excluded_extensions)

    def get_all_links(self) -> Dict[str, int]:
        links: Dict[str, int] = {}
        for article in self.articles:
            for link in article.get_all_links():
                if link in links:
                    links[link] += 1
                else:
                    links[link] = 1

        for repo_file in self.code:
            cleaned_name = sanitize_article_name(repo_file.name)
            # print(f"Repo file: {repo_file.name} to {cleaned_name}")
            if cleaned_name in links:
                links[cleaned_name] += 1
            else:
                links[cleaned_name] = 1

        return links
