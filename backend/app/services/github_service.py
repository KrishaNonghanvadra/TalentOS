import re

import requests


GITHUB_API = "https://api.github.com"


def extract_github_username(github_url: str) -> str:
    github_url = github_url.rstrip("/")

    match = re.search(
        r"github\.com/([^/]+)",
        github_url
    )

    if not match:
        raise ValueError("Invalid GitHub URL")

    return match.group(1)


def get_github_profile(github_url: str):
    username = extract_github_username(
        github_url
    )

    response = requests.get(
        f"{GITHUB_API}/users/{username}",
        timeout=10
    )

    if response.status_code == 404:
        raise ValueError("GitHub user not found")

    response.raise_for_status()

    return response.json()

def get_github_repositories(
    github_url: str
):
    username = extract_github_username(
        github_url
    )

    response = requests.get(
        f"{GITHUB_API}/users/{username}/repos",
        params={
            "per_page": 100,
            "sort": "updated"
        },
        timeout=10
    )

    response.raise_for_status()

    return response.json()

def analyze_github(
    github_url: str
):
    profile = get_github_profile(
        github_url
    )

    repositories = get_github_repositories(
        github_url
    )

    languages = {}

    for repository in repositories:

        language = repository.get(
            "language"
        )

        if language:
            languages[language] = (
                languages.get(language, 0) + 1
            )

    return {
        "username": profile["login"],
        "name": profile.get("name"),
        "public_repositories": profile.get(
            "public_repos", 0
        ),
        "languages": languages
    }