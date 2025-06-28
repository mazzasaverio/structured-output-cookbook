"""Logging configuration using Loguru."""

import sys
from loguru import logger
from .config import Config


def setup_logger(config: Config) -> None:
    """Configure loguru logger based on config."""
    logger.remove()
    
    if config.log_format == "json":
        format_str = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
    else:
        format_str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | {message}"
    
    logger.add(
        sys.stderr,
        format=format_str,
        level=config.log_level,
        serialize=config.log_format == "json"
    )


def get_logger(name: str):
    """Get a logger instance for a specific module."""
    return logger.bind(name=name)