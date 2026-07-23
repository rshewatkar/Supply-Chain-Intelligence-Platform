"""
Utility functions for file and directory operations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.utils.logger import get_logger

logger = get_logger(__name__)


def ensure_directory(directory: str | Path) -> Path:
    """
    Create a directory if it does not already exist.

    Parameters
    ----------
    directory : str | Path
        Directory path.

    Returns
    -------
    Path
        Path object of the directory.
    """

    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)

    return directory


def save_json(data: Any, file_path: str | Path, indent: int = 4) -> None:
    """
    Save data to a JSON file.

    Parameters
    ----------
    data : Any
        Data to save.

    file_path : str | Path
        Output JSON file.

    indent : int
        JSON indentation.
    """

    file_path = Path(file_path)

    ensure_directory(file_path.parent)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=indent,
            ensure_ascii=False,
        )

    logger.info("Saved JSON -> %s", file_path)


def load_json(file_path: str | Path) -> Any:
    """
    Load a JSON file.

    Parameters
    ----------
    file_path : str | Path

    Returns
    -------
    Any
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} does not exist.")

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    logger.info("Loaded JSON <- %s", file_path)

    return data


def write_text(text: str, file_path: str | Path) -> None:
    """
    Save text to a file.
    """

    file_path = Path(file_path)

    ensure_directory(file_path.parent)

    file_path.write_text(
        text,
        encoding="utf-8",
    )

    logger.info("Saved text -> %s", file_path)


def read_text(file_path: str | Path) -> str:
    """
    Read text from a file.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} does not exist.")

    logger.info("Loaded text <- %s", file_path)

    return file_path.read_text(
        encoding="utf-8",
    )


def file_exists(file_path: str | Path) -> bool:
    """
    Check whether a file exists.
    """

    return Path(file_path).exists()