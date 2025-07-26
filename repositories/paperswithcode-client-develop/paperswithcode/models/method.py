from typing import Optional

from paperswithcode.models.page import Page
from paperswithcode.models.model import Model


class Method(Model):
    """Method object.

    Attributes:
        id: Method ID.
        name: Method short name.
        full_name: Method full name.
        description: Method description.
        paper: ID of the paper that describes the method.
    """

    id: str
    name: str
    full_name: str
    description: str
    paper: Optional[str]


class Methods(Page):
    """Object representing a paginated page of methods.

    Attributes:
        count: Number of elements matching the query.
        next_page: Number of the next page.
        previous_page: Number of the previous page.
        results: List of methods on this page.
    """

    results: list[Method]
