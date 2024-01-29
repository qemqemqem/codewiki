import os
from typing import List, Optional
import mimetypes
from pathlib import Path

class RepoFile:
    def __init__(self, name: str, location: str, file_type: Optional[str], content: str):
        self.name = name
        self.location = location
        self.file_type = file_type
        self.content = content

    def __repr__(self) -> str:
        return f"RepoFile(name={self.name}, location={self.location}, file_type={self.file_type})"

def get_file_type(file_path: str) -> Optional[str]:
    type, _ = mimetypes.guess_type(file_path)
    return type

def read_file_contents(file_path: str) -> str:
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {e}"

RepoList = List[RepoFile]

def analyze_directory(directory: Path, excluded_dirs: Optional[List[str]] = None, excluded_extensions: Optional[List[str]] = None) -> RepoList:
    if excluded_dirs is None:
        excluded_dirs = []
    if excluded_extensions is None:
        excluded_extensions = []

    repo_files: RepoList = []
    for root, dirs, files in os.walk(directory, topdown=True):
        root_path = Path(root)
        dirs[:] = [d for d in dirs if (root_path / d).relative_to(directory) not in map(Path, excluded_dirs)]

        for name in files:
            if any(name.endswith(ext) for ext in excluded_extensions):
                continue

            file_path = os.path.join(root, name)
            file_type = get_file_type(file_path)
            content = read_file_contents(file_path)
            repo_files.append(RepoFile(name, file_path, file_type, content))
    return repo_files


if __name__ == "__main__":
    # Example usage
    directory_path = Path("/home/keenan/Dev/mtgrandom")
    excluded_directories = ["/Card Examples", "/sets", "/assets", "/.git"]
    excluded_extensions = ['.log', '.tmp', '.png']
    files_in_repo = analyze_directory(directory_path, excluded_directories, excluded_extensions)
    for file in files_in_repo:
        print(file)
