#!/usr/bin/env python3
"""Client for interacting with GitHub API."""
from typing import List, Dict
from utils import get_json, memoize

class GithubOrgClient:
    """Client to fetch GitHub organization information."""

    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str) -> None:
        self._org_name = org_name

    @memoize
    def org(self) -> Dict:
        """Return the organization data."""
        return get_json(self.ORG_URL.format(org=self._org_name))

    @property
    def _public_repos_url(self) -> str:
        return self.org["repos_url"]

    def public_repos(self, license: str = None) -> List[str]:
        repos = get_json(self._public_repos_url)
        repo_names = [repo["name"] for repo in repos]
        if license:
            repo_names = [
                repo["name"] for repo in repos
                if repo.get("license", {}).get("key") == license
            ]
        return repo_names

    @staticmethod
    def has_license(repo: Dict, license_key: str) -> bool:
        return repo.get("license", {}).get("key") == license_key
