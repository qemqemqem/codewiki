import os
import mimetypes

class RepoFile:
    def __init__(self, name, location, file_type, content):
        self.name = name
        self.location = location
        self.file_type = file_type
        self.content = content

    def __repr__(self):
        return f"RepoFile(name={self.name}, location={self.location}, file_type={self.file_type}, len(content)={len(self.content)})"

def get_file_type(file_path):
    type, _ = mimetypes.guess_type(file_path)
    return type if type else "Unknown"

def read_file_contents(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {e}"

def analyze_directory(directory, excluded_dirs=None, excluded_extensions=None):
    if excluded_dirs is None:
        excluded_dirs = []
    if excluded_extensions is None:
        excluded_extensions = []

    repo_files = []
    for root, dirs, files in os.walk(directory, topdown=True):
        # Filter out the excluded directories
        dirs[:] = [d for d in dirs if os.path.join(root, d).replace(directory, '') not in excluded_dirs]

        for name in files:
            if any(name.endswith(ext) for ext in excluded_extensions):
                continue  # Skip files with excluded extensions

            file_path = os.path.join(root, name)
            file_type = get_file_type(file_path)
            content = read_file_contents(file_path)
            repo_files.append(RepoFile(name, file_path, file_type, content))
    return repo_files


if __name__ == "__main__":
    # Example usage
    directory_path = "/home/keenan/Dev/mtgrandom"
    excluded_directories = ["/Card Examples", "/sets", "/assets", "/.git"]
    excluded_extensions = ['.log', '.tmp']
    files_in_repo = analyze_directory(directory_path, excluded_directories, excluded_extensions)
    for file in files_in_repo:
        print(file)
