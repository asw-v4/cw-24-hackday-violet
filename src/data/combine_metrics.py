import argparse
import datetime as dt
import logging
import json
import os


from cli import DataParser

"""

{
  "metadata": "<string, timestamp (standard format e.g. ISO8601)>",
  "repository": {
    "display name": "<string, name for vis. label, e.g. GH repo name>",
    "URL": "<string, GH repo link>"
  },
  "status": {
    "<numeric metric name>": {
      "valid range": ["<minimum>", "<maximum>"],
      "closed interval": "<Bool, True if range is closed, False if open or half open>",
      "direction of health": "<Bool, True means increasing is better i.e. maximum is healthiest>"
    },
    "<Boolean metric name>": "<Bool, corresponds to value that is healthy>"
  }
}
"""

if __name__ == "__main__":
    args = DataParser().parse_args()
    gh_data = json.load(args.github)

    data = []

    for repo in gh_data:
        logging.debug(repo)
        with open(repo, "r") as fh:
            sc_data = json.load(fh)

        logging.debug(sc_data)
        data.append({
            "metadata": dt.datetime.utcnow().isoformat(),
            "repository": {
                "display_name": repo,
                "url": sc_data["repo"]["name"]
            },
            "metrics": sc_data["checks"]
        })

    print(json.dumps(data))
