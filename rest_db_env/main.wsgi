#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/home/sourav/Desktop/pip_env/rest_db_env/")

from main import app as application
