import re
from functools import wraps
from inspect import iscoroutinefunction
from typing import Any, Callable
from sqlalchemy.exc import IntegrityError, NoResultFound
from app.common.exceptions import CommonExceptions, DatabaseExceptions


def parameter_checker() -> Any:
    def wrapper(func: Callable) -> Callable:
        if iscoroutinefunction(func):
            @wraps(func)
            async def wrapped(*args: Any, **kwargs: Any) -> Any:
                try:
                    return await func(*args, **kwargs)
                except (TypeError, ValueError):
                    # raise CommonExceptions.INVALID_PARAMETERS
                    raise
        else:
            @wraps(func)
            def wrapped(*args: Any, **kwargs: Any) -> Any:
                try:
                    return func(*args, **kwargs)
                except (TypeError, ValueError):
                    # raise CommonExceptions.INVALID_PARAMETERS
                    raise
        return wrapped
    return wrapper


def db_checker() -> Any:
    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        async def wrapped(*args: Any, **kwargs: Any) -> Any:
            try:
                return await func(*args, **kwargs)
            except StopAsyncIteration:
                raise
                # raise DatabaseExceptions.COMMON_EXCEPTION
            except (TypeError, ValueError):
                # raise CommonExceptions.INVALID_PARAMETERS
                raise
            except NoResultFound:
                # raise CommonExceptions.NOTHING_FOUND
                raise
            except IntegrityError:
                # raise DatabaseExceptions.DUPLICATED_ENTRY
                raise
        return wrapped
    return wrapper


def remove_dup_spaces(text: str) -> str:
    return " ".join(text.split())


def hard_clean_text(text: str):
    pattern = re.compile(r"[^\w]]")
    return re.sub(pattern, "", text)
