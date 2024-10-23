"""Generate the log format string"""

from colorama import Style


def get_apache_log_format(
    attr_config_dict: dict[str, tuple[str | None, str | None, int]],
    ignore_attr_list: list[str],
    add_colors: bool = False,
) -> str:
    """Generate an Apache log format string

    Parameters
    ----------
    attr_config_dict

    ignore_attr_list
        A list of what fields in the `attr_config_dict` should be ignored.
    add_colors
        If `True` add color to the logs
    """
    format_list = list()
    for attr, (attr_name, str_format, color) in attr_config_dict.items():
        if attr in ["message", "msg"] or attr in ignore_attr_list:
            continue

        attr_name = attr if attr_name is None else attr_name
        str_format = "s" if str_format is None else str_format

        if add_colors is True:
            format_list.append(f"{color}%({attr}){str_format}{Style.RESET_ALL}")
        else:
            format_list.append(f"{attr_name} %({attr}){str_format}")

    return "|".join(format_list) + " %(message)s"
