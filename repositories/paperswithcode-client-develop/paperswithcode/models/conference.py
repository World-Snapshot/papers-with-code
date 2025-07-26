from typing import Optional


from paperswithcode.models.page import Page
from paperswithcode.models.model import Model


class Conference(Model):
    """Conference object.

    Attributes:
        id: Conference ID.
        name: Conerence name.
    """

    id: str
    name: str


class Conferences(Page):
    """Object representing a paginated page of conferences.

    Attributes:
        count: Number of elements matching the query.
        next_page: Number of the next page.
        previous_page: Number of the previous page.
        results: List of conferences on this page.
    """

    results: list[Conference]


class Proceeding(Model):
    """Conference proceeding object.

    Attributes:
        id: Proceeding ID.
        year: Year in which the proceeding was held.
        month: Month in which the proceedingt was held.
    """

    id: str
    year: Optional[int]
    month: Optional[int]


class Proceedings(Page):
    """Object representing a paginated page of proceedings.

    Attributes:
        count: Number of elements matching the query.
        next_page: Number of the next page.
        previous_page: Number of the previous page.
        results: List of proceedings on this page.
    """

    results: list[Proceeding]
