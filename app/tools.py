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
                    raise CommonExceptions.INVALID_PARAMETERS
        else:
            @wraps(func)
            def wrapped(*args: Any, **kwargs: Any) -> Any:
                try:
                    return func(*args, **kwargs)
                except (TypeError, ValueError):
                    raise CommonExceptions.INVALID_PARAMETERS
        return wrapped
    return wrapper


def db_checker() -> Any:
    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        async def wrapped(*args: Any, **kwargs: Any) -> Any:
            try:
                return await func(*args, **kwargs)
            except (TypeError, ValueError):
                raise CommonExceptions.INVALID_PARAMETERS
            except NoResultFound:
                raise CommonExceptions.NOTHING_FOUND
            except IntegrityError:
                raise DatabaseExceptions.DUPLICATED_ENTRY
        return wrapped
    return wrapper
