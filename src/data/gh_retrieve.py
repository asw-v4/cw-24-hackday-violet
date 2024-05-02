import datetime as dt
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
    auth = Auth.Token(os.environ["GITHUB_AUTH_TOKEN"])
    g = Github(auth=auth)

    data = dict()

    for repo in args.repositories:
        data[repo] = dict()

        repository = g.get_repo(repo, lazy=True)

        try:
            most_recent_commit = repository.get_commits().reversed.get_page(0)[0]
            data[repo]["last_modified_secs_ago"] = int((dt.datetime.now(dt.timezone.utc) - most_recent_commit.last_modified_datetime).total_seconds())
        except github.GithubException:
            data[repo]["last_modified_secs_ago"] = None

        # Getting a bit narly with repeated code, address
        try:
            data[repo]["license_exists"] = repository.get_license() is not None
        except github.UnknownObjectException:
            data[repo]["license_exists"] = False

        try:
            data[repo]["readme_exists"] = repository.get_readme() is not None
        except github.UnknownObjectException:
            data[repo]["readme_exists"] = False

        # computeOpenIssueRatio from isitmaintained
        #   - https://github.com/mnapoli/IsItMaintained/blob/cb451435e5232496600a9747722db4942fd88041/src/Maintained/Statistics/StatisticsComputer.php#L103
        try:
            data[repo]["open_count"] = repository.get_issues(state="open").totalCount
            data[repo]["closed_count"] = repository.get_issues(state="closed").totalCount
        except github.GithubException:
            data[repo]["open_count"] = -1
            data[repo]["closed_count"] = -1

    g.close()
    print(json.dumps(data))