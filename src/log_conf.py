import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

FORMAT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
LOG_DIR = Path.home() / '.local/state/langcode/logs'

def configure_logging() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format=FORMAT,
        handlers=[
            RotatingFileHandler(
                LOG_DIR / 'app.log',
                maxBytes=4 * 1024**2,
                backupCount=1,
                encoding='utf-8',
            ),
        ],
    )
