import argparse
import logging


class RepositoryParser(argparse.ArgumentParser):
    """An ArgumentParser specialised to support retrieval of repositories
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_argument("repositories",
                          help="Get list of repositories in form of user/repo",
                          nargs="+")
        self.add_argument("-v",
                          "--verbose",
                          action="store_true",
                          default=False)

    def parse_args(self, *args, **kwargs):
        args = super().parse_args(*args, **kwargs)

        logging.basicConfig(
            level=logging.DEBUG if args.verbose else logging.INFO)
        logging.getLogger("matplotlib").setLevel(logging.WARNING)

        return args
