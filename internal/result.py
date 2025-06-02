from __future__ import annotations

import contextlib
import enum
import io
import logging
import sys
import traceback
import typing

__all__ = ("Result", "ResultStatus")

from collections.abc import Callable, Sequence

from types import TracebackType

logger = logging.getLogger(__name__)


class ResultStatus(enum.StrEnum):
    SUCCESS = "success"
    FAILURE = "failure"
    SKIPPED = "skipped"


class Result:
    def __init__(
        self,
        *,
        return_value: typing.Any = None,
        return_value_type: type[typing.Any] = None,
        raised_error: type[Exception] | None = None,
        expected_error_msg: str | None = None,
        expect_stdout: bool = False,
        exact_stdout: str | None = None,
    ) -> None:
        self._return_value = return_value
        if return_value_type is None:
            return_value_type = type(return_value)
        self._return_value_type = return_value_type
        self._raised_error = raised_error
        self._expected_error_msg = expected_error_msg
        self._expect_stdout = expect_stdout
        self._exact_stdout = exact_stdout
        self._exc_handler = _ExceptionHandler(
            raised_error=self._raised_error, expected_error_msg=self._expected_error_msg
        )
        self._listener = _StdoutListener()

    @classmethod
    def from_func(
        cls,
        func: Callable[[typing.Any, ...], typing.Any] | None = None,
        **kwargs: typing.Any,
    ):
        return_value: typing.Any = None
        return_value_type: type[typing.Any] = None
        raised_error: type[Exception] | None = None
        expected_error_msg: str | None = None
        expect_stdout: bool = False
        exact_stdout: str | None = None
        internal_listener = _InternalStdoutListener()
        try:
            with internal_listener:
                ret = func(**kwargs)
        except Exception as exc:
            raised_error = type(raised_error)
            expected_error_msg = str(raised_error)
        else:
            return_value = ret
            return_value_type = type(return_value)

        if internal_listener.stdout:
            expect_stdout = True
            exact_stdout = internal_listener.stdout
        return cls(
            return_value=return_value,
            return_value_type=return_value_type,
            raised_error=raised_error,
            expected_error_msg=expected_error_msg,
            expect_stdout=expect_stdout,
            exact_stdout=exact_stdout,
        )

    def catch(self) -> _ExceptionHandler:
        return self._exc_handler

    def listen(self) -> _StdoutListener:
        return self._listener

    def validate_result(self, return_value: typing.Any) -> ResultStatus:
        if self._exc_handler.result != ResultStatus.SUCCESS:
            self._exc_handler.print_traceback()
            return self._exc_handler.result

        if self._return_value_type is not type(return_value):
            logger.error(
                "Return values type %s does not match expected return value type %s",
                type(return_value),
                self._return_value_type,
            )
            return ResultStatus.FAILURE
        if self._return_value and return_value != self._return_value:
            logger.error(
                "Return value %s does not match expected return value %s",
                return_value,
                self._return_value,
            )
            return ResultStatus.FAILURE
        if self._expect_stdout and self._listener.stdout == "":
            logger.error(
                "Expected outputting something to the console, but didnt get anything"
            )
            return ResultStatus.FAILURE
        if self._exact_stdout and self._listener.stdout != self._exact_stdout:
            logger.error(
                'Expected outputting "%s" to the console but got: "%s"',
                self._exact_stdout,
                self._listener.stdout,
            )
            return ResultStatus.FAILURE
        return ResultStatus.SUCCESS


class _ExceptionHandler:
    def __init__(
        self,
        *,
        raised_error: type[Exception] | None = None,
        expected_error_msg: str | None = None,
    ) -> None:
        self._raised_error = raised_error
        self._expected_error_msg = expected_error_msg
        self._result: ResultStatus = ResultStatus.FAILURE
        self._exception: (
            tuple[
                type[BaseException] | None, BaseException | None, TracebackType | None
            ]
            | None
        ) = None

    @property
    def result(self) -> ResultStatus:
        return self._result

    @property
    def exception(
        self,
    ) -> (
        tuple[type[BaseException] | None, BaseException | None, TracebackType | None]
        | None
    ):
        return self._exception

    def print_traceback(self) -> None:
        if self._exception:
            traceback.print_exception(
                self._exception[0], self._exception[1], self._exception[2]
            )

    def __enter__(self):
        self._result = ResultStatus.FAILURE
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        if exc_type is None and self._raised_error is None:
            self._result = ResultStatus.SUCCESS
            return False
        if exc_type is NotImplementedError:
            self._result = ResultStatus.SKIPPED
            return True

        if self._raised_error:
            if exc_type is not self._raised_error:
                logger.error(
                    "Raised exception %s does not match expected exception %s",
                    exc_type,
                    self._raised_error,
                )
                return True
        if self._expected_error_msg:
            if str(exc_val) != self._expected_error_msg:
                logger.error(
                    'Raised exception message "%s" does not match expected exception message "%s"',
                    str(exc_val),
                    self._expected_error_msg,
                )
                return True

        if self._raised_error or self._expected_error_msg:
            self._result = ResultStatus.SUCCESS
            return True

        self._exception = (exc_type, exc_val, exc_tb)
        return True


class _StdoutListener:
    class _Tee(io.TextIOBase):
        def __init__(self, original: io.TextIOBase, buffer: io.StringIO) -> None:
            self._orig = original
            self._buf = buffer

        def write(self, data: str) -> int:
            self._buf.write(data)
            return self._orig.write(data)

        def flush(self) -> None:
            self._buf.flush()
            self._orig.flush()

        def __getattr__(self, name: str) -> typing.Any:
            return getattr(self._orig, name)

    def __init__(self) -> None:
        self._buf: io.StringIO = io.StringIO()
        self._orig_stdout: io.TextIOBase = sys.stdout
        self._orig_stderr: io.TextIOBase = sys.stderr

    @property
    def stdout(self) -> str:
        return self._buf.getvalue()

    def __enter__(self) -> _StdoutListener:
        self._buf = io.StringIO()

        self._orig_stdout = sys.stdout
        self._orig_stderr = sys.stderr

        sys.stdout = self._Tee(self._orig_stdout, self._buf)
        sys.stderr = self._Tee(self._orig_stderr, self._buf)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        sys.stdout = self._orig_stdout
        sys.stderr = self._orig_stderr

        return False


class _InternalStdoutListener:
    def __init__(self) -> None:
        self._buf: io.StringIO = io.StringIO()
        self._stdout_cm: contextlib.redirect_stdout | None = None
        self._stderr_cm: contextlib.redirect_stderr | None = None

    @property
    def stdout(self) -> str:
        return self._buf.getvalue()

    def __enter__(self) -> _InternalStdoutListener:
        self._buf = io.StringIO()

        self._stdout_cm = contextlib.redirect_stdout(self._buf)
        self._stderr_cm = contextlib.redirect_stderr(self._buf)
        self._stdout_cm.__enter__()
        self._stderr_cm.__enter__()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        self._stderr_cm.__exit__(exc_type, exc_val, exc_tb)
        self._stdout_cm.__exit__(exc_type, exc_val, exc_tb)
        return False
