from github import Github
from Project import Project

LANGUAGES_TO_ANALYZE = ["C", "C++"]

class ProjectFinder:
    def __init__(self):
        self.github = Github()
        self.results = None
    
    def get_projects(self):
        if not self.results:
            self.results = self.github.search_repositories("code")
            self.page_at = 0
        
        repos = self.results.get_page(self.page_at)
        self.page_at += 1
        
        results = []
        for repo in repos:
            if repo.language in LANGUAGES_TO_ANALYZE:
                results.append(Project(repo))
        
        return results