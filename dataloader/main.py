import os
import sys
import logging
from Configs import getConfig
from linetimer import CodeTimer

config = getConfig()
log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(getattr(logging, config.LOG_LEVEL))

if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(
        os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
    )
    SCRIPT_DIR = os.path.join(SCRIPT_DIR, "..")
    sys.path.append(os.path.normpath(SCRIPT_DIR))

from dataloader.download import download
from dataloader.load import load_data, get_graph

if __name__ == "__main__":
    config = getConfig()
    log.info(
        "Start with loglevel '{}' and ENV={}".format(
            config.LOG_LEVEL, os.environ["ENV"] if "ENV" in os.environ else "DEV"
        )
    )
    log.info("Test DB connection ({})...".format(config.NEO4J))
    get_graph().run("MATCH (n) return n limit 1")
    log.info("...DB is reachable") 
    with CodeTimer("Downloader", unit="s"):
        download()
    with CodeTimer("Importer", unit="s"):
        load_data()
