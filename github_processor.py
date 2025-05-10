import os
import tempfile
import zipfile
import requests
from io import BytesIO

class GitHubRepoProcessor:
    def __init__(self, repo_url, include_extensions=None):
        self.repo_url = repo_url
        self.include_extensions = include_extensions or [
            ".py", ".java", ".js", ".ts", ".rb", ".c", ".md", ".txt", ".html", ".css"
        ]

    def download_and_extract_repo(self):
        owner_repo = self.repo_url.rstrip("/").replace("https://github.com/", "")
        archive_url = f"https://api.github.com/repos/{owner_repo}/zipball"

        print(f"Downloading ZIP from: {archive_url}")
        response = requests.get(archive_url)
        if response.status_code != 200:
            raise Exception(f"Failed to download ZIP archive: {response.status_code}")

        return zipfile.ZipFile(BytesIO(response.content))

    def get_combined_file_contents(self):
        zip_file = self.download_and_extract_repo()
        combined_content = ""

        with tempfile.TemporaryDirectory() as tmpdir:
            zip_file.extractall(tmpdir)

            for root, dirs, files in os.walk(tmpdir):
                for file in files:
                    ext = os.path.splitext(file)[1]
                    if ext in self.include_extensions:
                        path = os.path.join(root, file)
                        try:
                            with open(path, "r", encoding="utf-8") as f:
                                content = f.read()
                                combined_content += f"\n\n--- FILE: {file} ---\n{content}"
                        except Exception as e:
                            print(f"Skipped file {file}: {e}")
        return combined_content