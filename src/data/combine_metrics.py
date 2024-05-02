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
        repo_filename = "temp_data/{}.json".format(repo[repo.index("/"):])
        with open(repo_filename, "r") as fh:
            sc_data = json.load(fh)

        #with open(repo_filename.replace("json", "fair.json"), "r") as fh:
        #    fair_data = json.load(fh)

        logging.debug(sc_data)

        # Scorecard scores everything from 0-10, so we can add the same
        # context to each:
        scorecard_context = {
            "valid range": [0, 10],
            "closed interval": True,
            "direction of health": True,  # 10 (max) is best, 0 worst
        }
        sc_metric_names = [
            "Maintained", "Packaging", "Contributors", "CI-Tests", "Code-Review"
        ]

        sc_metrics = dict()
        for name in sc_metric_names:
            metric = scorecard_context.copy()
            for sc_dat in sc_data["checks"]:
                if sc_dat["name"] == name:
                    metric["score"] = sc_dat["score"]
            sc_metrics[name] = metric
        sc_metrics.update(gh_data[repo])

        data.append({
            "metadata": dt.datetime.utcnow().isoformat(),
            "repository": {
                "display_name": repo,
                "url": sc_data["repo"]["name"]
            },
            "metrics": sc_metrics
        })

    print(json.dumps(data))
