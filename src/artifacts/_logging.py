"""SDK-wide logging configuration.

Provides a simple ``setup_logging()`` helper so beginners can enable
informative output with a single call::

    import artifacts
    artifacts.setup_logging()             # INFO level
    artifacts.setup_logging(logging.DEBUG) # verbose
"""

from __future__ import annotations

import logging


def setup_logging(level: int = logging.INFO) -> None:
    """Configure logging for the Artifacts SDK.

    Sets up a ``StreamHandler`` on the ``"artifacts"`` logger with a
    concise timestamp format.  Subsequent calls update the level
    without adding duplicate handlers.
    """
    logger = logging.getLogger("artifacts")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s] %(name)s %(levelname)s: %(message)s",
                datefmt="%H:%M:%S",
            )
        )
        logger.addHandler(handler)
    logger.setLevel(level)
