import enum
from dataclasses import dataclass
from typing import Any, Callable, Union

from rich.table import Table
from rich.console import JustifyMethod


class Align(enum.Enum):
    left: JustifyMethod = "left"
    center: JustifyMethod = "center"
    right: JustifyMethod = "right"


@dataclass
class Column:
    Align = Align

    title: str
    path: Union[str, Callable[[Any], str]]
    align: Align = Align.left


def _get_path(obj, path) -> str:
    if callable(path):
        obj = path(obj)
    else:
        path = path.split(".")
        for item in path:
            obj = getattr(obj, item)
        if isinstance(obj, bool):
            obj = ":white_check_mark:" if obj else ":cross_mark:"
    return f"{obj}"


class RichTableMixin:
    HEADERS: list[Column] = []

    @classmethod
    def get_rich_table(cls, header_style="bold magenta") -> Table:
        table = Table(show_header=True, header_style=header_style)
        for column in cls.HEADERS:
            table.add_column(header=column.title, justify=column.align.value)
        return table

    def to_rich_row(self) -> list:
        return [_get_path(self, column.path) for column in self.HEADERS]
