import logging
from datetime import datetime, timezone

from . import configs, utils


class Apache(logging.Formatter):
    """Apache style log formatter"""

    def __init__(self, fmt: str | None = None, datefmt=None, style="%", *_, **kwargs):
        self.add_colors = kwargs.pop("add_colors", False)
        self.ignore_log_attribute_list = kwargs.pop("ignore_log_attribute_list", None)
        self.timezone = timezone.utc

        if self.ignore_log_attribute_list is None:
            self.ignore_log_attribute_list = configs.DEFAULT_IGNORE_ATTRIBUTE_LIST

        if fmt is not None:
            log_format = fmt
        else:
            log_format = utils.get_apache_log_format(
                attr_config_dict=configs.LOG_ATTRIBUTES_TO_NAME_AND_FORMAT_AND_COLOR_DICT,
                ignore_attr_list=self.ignore_log_attribute_list,
                add_colors=self.add_colors,
            )

        super().__init__(fmt=log_format, datefmt=datefmt, style=style)

    def formatTime(self, record, datefmt=None) -> str:
        """Override: logging.Formatter.formatTime"""
        if datefmt is not None:
            s = datetime.fromtimestamp(record.created, tz=self.timezone).strftime(
                datefmt
            )
        else:
            s = str(datetime.fromtimestamp(record.created, tz=self.timezone))
        return s
