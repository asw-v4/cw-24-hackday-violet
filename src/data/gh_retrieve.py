import os

from github import Github
from github import Auth

# using an access token
auth = Auth.Token(os.environ["GITHUB_API_TOKEN"])

# First create a Github instance:

# Public Web Github
g = Github(auth=auth)

# Then play with your Github objects:
for repo in g.get_user().get_repos():
    print(repo.name)

# To close connections after use
g.close()