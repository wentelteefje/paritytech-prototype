import os
import requests
import json
from datetime import datetime, timedelta

dir_path = os.path.join(os.environ['GITHUB_WORKSPACE'], 'data')
os.makedirs(dir_path, exist_ok=True)

# Define your variables here
# token = os.getenv('TOKEN')  # Get the API token from environment variable
owner = "paritytech"  # GitHub username
# repo = "repo"  # Repository name
repo_list = ["polkadot", "substrate", "ink", "ink"] # List of repositories
label_list = ["J7-mentor", "Z6-mentor", "E-mentor-available", "good%20first%20issue"] # Corresponding mentor labels

# Set up headers
# headers = {"Authorization": f"token {token}"}

# Initialize list of issue data
trophy_data = []

for (repo,label) in zip(repo_list,label_list):
    # Get issues
    issues_response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/issues?state=closed&labels=" + label)
    issues = issues_response.json()

    # Iterate over all issues
    for issue in issues:
        # Check if the issue has been assigned to someone
        if issue['assignee']:
            # Get necessary information
            title = issue['title']
            url = issue['html_url']
            closed_at = issue['closed_at']

            # Convert 'closed_at' to "N days ago"
            closed_at_date = datetime.strptime(closed_at, "%Y-%m-%dT%H:%M:%SZ")
            days_ago = (datetime.now() - closed_at_date).days

            # Add to list of issue data
            trophy_data.append({
                'project': repo,
                'title': title,
                'url': url,
                'days_ago': days_ago,
                'assignee': {
                    'login': issue['assignee']['login'],
                    'avatar_url': issue['assignee']['avatar_url'],
                    'html_url': issue['assignee']['html_url']
                }
            })

# Sort trophy_data by 'days_ago'
sorted_trophy_data = sorted(trophy_data, key=lambda x: x['days_ago'])

# Save sorted data to JSON file
with open('../data/trophy_data.json', 'w') as f:
    json.dump(sorted_trophy_data, f)
