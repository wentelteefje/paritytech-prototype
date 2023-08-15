import os
import requests
import json
from datetime import datetime, timedelta


# token = os.getenv('TOKEN')  # Get the API token from environment variable
owner = "paritytech"  # GitHub username
repo_list = ["polkadot", "substrate", "cumulus", "ink"]  # List of repositories
loc_dict = {
  "polkadot": 500000,
  "substrate": 500000,
  "cumulus": 500000,
  "ink": 500000
}

# Initialize results dictionary
results = {}

# Iterate over all repositories
for repo in repo_list:
    # Send a request to get repository info (includes star count)
    repo_info = requests.get(f"https://api.github.com/repos/{owner}/{repo}").json()

    # Get star count
    star_count = repo_info.get("stargazers_count", 0)

    # Get the repository creation date
    created_at = repo_info.get('created_at')

    # Parse the creation date string into a datetime object
    created_at_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")

    # Calculate the age of the repository in days
    repo_age_days = (datetime.utcnow() - created_at_date).days

    # Send a HEAD request to get commits
    commit_response = requests.head(f"https://api.github.com/repos/{owner}/{repo}/commits?per_page=1")

    # Extract 'Link' header
    link_header = commit_response.headers.get('Link')

    # Extract 'last' link
    last_link = [link for link in link_header.split(", ") if "rel=\"last\"" in link][0]

    # Extract page number from 'last' link
    total_commits = int(last_link.split("page=")[-1].split(">")[0])

    # Calculate the average daily commits
    daily_average_commits = round(total_commits / repo_age_days, 1)

    # Get time 24 hours ago
    one_day_ago = datetime.utcnow() - timedelta(days=1)

    # Initialize commit count
    commit_count_last_24 = 0

    # Iterate over all pages until a commit is found that is older than 24 hours
    for i in range(1, total_commits + 1):
        commit = requests.get(f"https://api.github.com/repos/{owner}/{repo}/commits?per_page=1&page={i}").json()[0]
        commit_date = datetime.strptime(commit['commit']['committer']['date'], "%Y-%m-%dT%H:%M:%SZ")
        if commit_date > one_day_ago:
            commit_count_last_24 += 1
        else:
            break

    # Get contributors - We want to get the top20, but fetch 21 in case a dependabot is there
    contributors = requests.get(f"https://api.github.com/repos/{owner}/{repo}/contributors?per_page=21").json()

    # Extract contributor information
    contributor_info = [
        {'login': contributor['login'], 'avatar_url': contributor['avatar_url'], 'html_url': contributor['html_url']} 
        for contributor in contributors 
        if contributor['login'] != "dependabot[bot]"
    ]
    
    # Drop last contributor if dependabot was not there
    if len(contributor_info) != 20:
        contributor_info.pop()

    # Add result to the dictionary
    results[repo] = {
        "star_count": star_count,
        "loc": loc_dict[repo],
        "daily_average_commits": daily_average_commits,
        "total_commits": total_commits,
        "commit_count_last_24": commit_count_last_24,
        "contributors": contributor_info
    }

with open('repo_info.json', 'w') as f:
    json.dump(results, f)
