import os
import random
from pathlib import Path
from typing import List, Dict, Optional

from code_handling.repoman import RepoList
from code_handling.repoman import analyze_directory
from writing.article import Article
from writing.wiki_manager import WikiManager


class CodeWikiManager(WikiManager):
    def __init__(self, wiki_name: str, wiki_path: Path, code_path: Path):
        super().__init__(wiki_name, wiki_path)
        self.code_path: Path = code_path

        # Load the code
        self.code: RepoList = analyze_directory(code_path)
