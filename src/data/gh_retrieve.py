import json
import logging
import os

import github
from github import Github
from github import Auth

from cli import RepositoryParser


if __name__ == "__main__":
    args = RepositoryParser().parse_args()
    # using an access token
    auth = Auth.Token(os.environ["GITHUB_API_TOKEN"])
    g = Github(auth=auth)

    data = dict()

    for repo in args.repositories:
        data[repo] = dict()

        #logging.info("Getting {}".format(repo))
        repository = g.get_repo(repo, lazy=True)

        try:
            most_recent_commit = repository.get_commits().reversed.get_page(0)[0]
            data[repo]["last_modified"] = most_recent_commit.stats.last_modified
        except github.GithubException:
            data[repo]["last_modified"] = None

        # Getting a bit narly with repeated code, address
        try:
            data[repo]["license_exists"] = repository.get_license() is not None
        except github.UnknownObjectException:
            data[repo]["license_exists"] = False

        try:
            data[repo]["readme_exists"] = repository.get_readme() is not None
        except github.UnknownObjectException:
            data[repo]["readme_exists"] = False

    g.close()
    print(json.dumps(data))