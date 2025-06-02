import logging
import typing
from collections.abc import Callable

from internal.result import Result, ResultStatus

logger = logging.getLogger(__name__)

__all__ = ("Task",)

FuncT = typing.TypeVar("FuncT", bound=Callable[[typing.Any, ...], typing.Any])


class Task:
    def __init__(
        self,
        func: FuncT,
        result: Result | None = None,
        good_func: FuncT | None = None,
        **kwargs: typing.Any,
    ) -> None:
        self._func = func
        if result is None and good_func is None:
            raise RuntimeError("Need to provide one of result or good_func")
        elif result is None:
            self._result = Result.from_func(good_func, **kwargs)
        else:
            self._result = result
        self._kwargs = kwargs
        self._func_name = getattr(self._func, "__name__", "<anon>")

    def run_task(self) -> None:
        logger.info('Running task "%s"', self._func_name)

        return_value: typing.Any = None
        with self._result.catch(), self._result.listen():
            return_value = self._func(**self._kwargs)

        result = self._result.validate_result(return_value)
        match result:
            case ResultStatus.SUCCESS:
                logger.info('Task "%s" completed successfully!', self._func_name)
            case ResultStatus.SKIPPED:
                logger.warning('Task "%s" skipped!', self._func_name)
            case ResultStatus.FAILURE:
                logger.error('Task "%s" failed!', self._func_name)
