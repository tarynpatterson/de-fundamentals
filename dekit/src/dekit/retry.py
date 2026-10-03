import functools
import logging
import time
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")

logger = logging.getLogger(__name__)


def retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    backoff_multiplier: float = 2.0,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
):
    if max_attempts < 1:
        raise ValueError(f"max_attempts must be at least 1, got {max_attempts}")
    if base_delay < 0:
        raise ValueError(f"base_delay must be non-negative, got {base_delay}")
    if backoff_multiplier < 1:
        raise ValueError(
            f"backoff_multiplier must be at least 1, got {backoff_multiplier}"
        )

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            attempt = 1
            delay = base_delay
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt >= max_attempts:
                        raise
                    logger.warning(
                        "Attempt %d/%d for %s failed: %s. Retrying in %.1fs.",
                        attempt,
                        max_attempts,
                        getattr(func, "__name__", repr(func)),
                        e,
                        delay,
                    )
                    time.sleep(delay)
                    attempt += 1
                    delay *= backoff_multiplier

        return wrapper

    return decorator
