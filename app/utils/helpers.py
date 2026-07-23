"""
General helper functions used throughout the project.
"""

from __future__ import annotations

import time
import uuid
from datetime import datetime
from functools import wraps
from typing import Any, Callable


def generate_uuid() -> str:
    """
    Generate a unique UUID string.

    Returns
    -------
    str
        UUID4 string.
    """
    return str(uuid.uuid4())


def current_timestamp() -> str:
    """
    Return the current UTC timestamp.

    Returns
    -------
    str
    """
    return datetime.utcnow().isoformat()


def batch_iterator(items: list[Any], batch_size: int):
    """
    Yield items in batches.

    Parameters
    ----------
    items : list
        Input list.

    batch_size : int
        Batch size.

    Yields
    ------
    list
        Batch of items.
    """

    for i in range(0, len(items), batch_size):
        yield items[i : i + batch_size]


def truncate_text(
    text: str,
    max_length: int = 200,
) -> str:
    """
    Truncate long text.

    Parameters
    ----------
    text : str

    max_length : int

    Returns
    -------
    str
    """

    if len(text) <= max_length:
        return text

    return text[:max_length] + "..."


def timer(func: Callable):
    """
    Decorator to measure execution time.

    Example
    -------
    @timer
    def process():
        ...
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        start = time.perf_counter()

        result = func(*args, **kwargs)

        elapsed = time.perf_counter() - start

        print(
            f"{func.__name__} executed in "
            f"{elapsed:.2f} seconds."
        )

        return result

    return wrapper