import logging
import sys
from datetime import datetime

DEBUG = True  # Set to False in production

log_history = []

class UILogHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        log_history.append((datetime.now(), msg))
        if len(log_history) > 200:
            log_history.pop(0)

# Configure root logger
logger = logging.getLogger('perftracker')
logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)
handler = UILogHandler()
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Also log to stderr
stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setFormatter(formatter)
logger.addHandler(stderr_handler)

def get_recent_logs(n=50):
    return list(log_history)[-n:]

def log_exception(exc):
    logger.exception("Exception occurred: %s", exc) 