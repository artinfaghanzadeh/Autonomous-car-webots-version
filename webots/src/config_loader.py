import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_ROOT = os.path.join(PROJECT_ROOT, "config")

if CONFIG_ROOT not in sys.path:
    sys.path.append(CONFIG_ROOT)

import parameters