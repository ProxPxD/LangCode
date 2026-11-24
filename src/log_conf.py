import logging
from logging import FileHandler
from pathlib import Path

FORMAT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
LOG_DIR = Path.home() / '.local/state/langcode/logs'

def configure_logging() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format=FORMAT,
        handlers=[
            FileHandler(LOG_DIR / 'app.log', encoding='utf-8'),
        ],
    )
