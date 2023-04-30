from functools import wraps
from inspect import iscoroutinefunction
from typing import Any, Callable
from sqlalchemy.exc import IntegrityError, NoResultFound
from app.constants.exceptions import CommonExceptions


def parameter_checker():
    def wrapper(func: Callable) -> Callable:
        if iscoroutinefunction(func):
            @wraps(func)
            async def wrapped(*args: Any, **kwargs: Any) -> Any:
                try:
                    return await func(*args, **kwargs)
                except (TypeError, ValueError):
                    raise CommonExceptions.INVALID_PARAMETERS
            return wrapped
        else:
            @wraps(func)
            def wrapped(*args: Any, **kwargs: Any) -> Any:
                try:
                    return func(*args, **kwargs)
                except (TypeError, ValueError):
                    raise CommonExceptions.INVALID_PARAMETERS
            return wrapped
    return wrapper


def db_checker():
    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        async def wrapped(*args: Any, **kwargs: Any) -> Any:
            try:
                return await func(*args, **kwargs)

            except (TypeError, ValueError):
                raise CommonExceptions.INVALID_PARAMETERS
            except NoResultFound:
                raise CommonExceptions.NOTHING_FOUND
            except AttributeError:
                raise CommonExceptions.NOTHING_FOUND
            except IntegrityError:
                raise CommonExceptions.DUPLICATED_ENTRY

        return wrapped
    return wrapper
