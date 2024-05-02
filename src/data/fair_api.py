import json
import logging
import requests

from cli import RepositoryParser

if __name__ == "__main__":
    args = RepositoryParser().parse_args()

    data = dict()
    for repo in args.repositories:
        response = requests.get("https://fair-checker.france-bioinformatique.fr/api/check/metrics_all",
                                params=dict(url="https://github.com/{}".format(repo)))

        data[repo] = response.json()

    print(json.dumps(data))
