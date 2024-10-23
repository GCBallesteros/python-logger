"""Main Log object from which we can new loggers"""

import datetime
import inspect
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path

from .exceptions import InvalidValue
from .Formatter import Apache


class Log(object):
    """
    All the attributes below can be provided to the Log builder.

    Attributes
    ----------
    project_name: str
    log_level: str
    assign_logger_name: bool
    input_formatter: str | logging.Formatter
    log_to_stdout: bool
    log_to_file: bool
    log_dir: Path
    log_file_suffix: str
    rotate_file_by_size: bool
    rotating_file_max_size_bytes: int
    rotate_file_by_time: bool
    rotation_period: str
    rotation_interval: int
    rotation_time: datetime.time | None
    rotating_file_backup_count: int
    colors_to_stdout: bool
    ignore_log_attribute_list: list[str] | None
    """

    ALLOWED_FORMATTER_STR_LIST = ["apache"]

    def __init__(
        self,
        project_name: str = "log",
        log_level: str = "info",
        assign_logger_name: bool = True,
        formatter: str | logging.Formatter = "apache",
        log_to_stdout: bool = True,
        log_to_file: bool = False,
        log_dir: Path = Path("logs"),
        log_file_suffix: str = "S",
        rotate_file_by_size: bool = False,
        rotating_file_max_size_bytes: int = 1048576,
        rotate_file_by_time: bool = False,
        rotation_period: str = "H",
        rotation_interval: int = 1,
        rotation_time: datetime.time | None = None,
        rotating_file_backup_count: int = 1024,
        colors_to_stdout: bool = True,
        ignore_log_attribute_list: list[str] | None = None,
    ) -> None:
        self.project_name = project_name
        self.log_level = log_level.upper()
        self.assign_logger_name = assign_logger_name
        self.input_formatter = formatter
        self.log_to_stdout = log_to_stdout
        self.log_to_file = log_to_file
        self.log_dir = log_dir.resolve()
        self.log_file_suffix = log_file_suffix
        self.rotate_file_by_size = rotate_file_by_size
        self.rotating_file_max_size_bytes = rotating_file_max_size_bytes
        self.rotate_file_by_time = rotate_file_by_time
        self.rotation_period = rotation_period.upper()
        self.rotation_interval = rotation_interval
        self.rotation_time = rotation_time
        self.rotating_file_backup_count = rotating_file_backup_count
        self.colors_to_stdout = colors_to_stdout
        self.ignore_log_attribute_list = ignore_log_attribute_list
        self.__set_logger()
        self.__set_log_handlers()

    def __set_logger(self) -> None:
        if self.assign_logger_name is True:
            self.__logger = logging.getLogger(name=self.project_name)
            print(logging.root.manager.loggerDict)
        else:
            self.__logger = logging.getLogger()
            print("root", logging.root.manager.loggerDict)

        self.__logger.setLevel(self.log_level)

    def get_logger(self) -> logging.Logger:
        """Get a logger"""
        return self.__logger

    def __set_log_handlers(self) -> None:
        if self.rotate_file_by_size is True:
            self.__set_log_filepath(set_suffix=True)
            fh = RotatingFileHandler(
                filename=self.__log_filepath,
                encoding="utf-8",
                maxBytes=self.rotating_file_max_size_bytes,
                backupCount=self.rotating_file_backup_count,
            )
            self.__add_handler(handler=fh, add_colors=False)

        elif self.rotate_file_by_time is True:
            self.__validate_rotation_period()
            self.__set_log_filepath(set_suffix=False)
            fh = TimedRotatingFileHandler(
                filename=self.__log_filepath,
                encoding="utf-8",
                when=self.rotation_period,
                interval=self.rotation_interval,
                backupCount=self.rotating_file_backup_count,
                utc=True,
                atTime=self.rotation_time,
            )
            self.__add_handler(handler=fh, add_colors=False)

        elif self.log_to_file is True:
            self.__set_log_filepath(set_suffix=True)
            fh = logging.FileHandler(filename=self.__log_filepath, encoding="utf-8")
            self.__add_handler(handler=fh, add_colors=False)

        else:
            pass

        if self.log_to_stdout:
            sh = logging.StreamHandler()
            self.__add_handler(handler=sh, add_colors=self.colors_to_stdout)

    def __set_log_filepath(self, set_suffix: bool = False) -> None:
        self.__set_log_filename(set_suffix=set_suffix)
        if not self.log_dir.exists():
            self.log_dir.mkdir(exist_ok=True)
        self.__log_filepath = self.log_dir / self.__log_filename

    def __validate_rotation_period(self) -> None:
        allowed_rotation_period_list = ["S", "M", "H", "D", "MIDNIGHT"]
        allowed_rotation_period_list += list(map(lambda n: f"W{n}", range(0, 7)))
        if self.rotation_period not in allowed_rotation_period_list:
            raise InvalidValue(
                self.rotation_period,
                allowed_rotation_period_list,
            )

    def __set_log_filename(self, set_suffix: bool = False) -> None:
        if set_suffix is True:
            self.__log_filename = "{0}_{1}.{2}".format(
                self.project_name, self.__get_log_filename_suffix(), "log"
            )
        else:
            self.__log_filename = f"{self.project_name}.log"

    def __get_log_filename_suffix(self) -> str:
        suffix_to_date_time_format_dict = {
            "S": "%Y-%m-%d_%H-%M-%S",
            "M": "%Y-%m-%d_%H-%M-00",
            "H": "%Y-%m-%d_%H-00-00",
            "D": "%Y-%m-%d",
        }

        if self.log_file_suffix not in suffix_to_date_time_format_dict.keys():
            raise InvalidValue(
                self.log_file_suffix, list(suffix_to_date_time_format_dict.keys())
            )
        datetime_now = self.__get_datetime_now()

        return datetime_now.strftime(
            suffix_to_date_time_format_dict[self.log_file_suffix]
        )

    def __get_datetime_now(self) -> datetime.datetime:
        return datetime.datetime.now(tz=datetime.timezone.utc)

    def __add_handler(self, handler: logging.Handler, add_colors: bool) -> None:
        handler.setLevel(self.log_level)
        handler.setFormatter(self.__get_formatter(add_colors=add_colors))
        self.__logger.addHandler(handler)

    def __get_formatter(self, add_colors: bool) -> logging.Formatter:
        if isinstance(self.input_formatter, logging.Formatter):
            return self.input_formatter

        elif isinstance(self.input_formatter, str):
            if self.input_formatter.lower() == "apache":
                return Apache(
                    add_colors=add_colors,
                    ignore_log_attribute_list=self.ignore_log_attribute_list,
                    datefmt="%Y-%m-%d @ %H:%M:%S",
                )
            else:
                raise InvalidValue(
                    value=self.input_formatter,
                    allowed_value_list=self.ALLOWED_FORMATTER_STR_LIST,
                )
        else:
            e_ = "'formatter' must be of type 'logging.Formatter' or 'str'"
            raise TypeError(e_)

    def log_function_call(self, func):
        """Decorator to log function calls."""

        def wrapper(*args, **kwargs):
            func_args = inspect.signature(func).bind(*args, **kwargs).arguments
            self.get_logger().info(
                "{0}.{1}({2})".format(
                    func.__module__,
                    func.__qualname__,
                    ", ".join("{} = {!r}".format(*item) for item in func_args.items()),
                )
            )
            return func(*args, **kwargs)

        return wrapper
