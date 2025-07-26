from typing import Optional

from paperswithcode.models.model import Model


class Page(Model):
    """Page model.

    Attributes:
        count: Number of elements matching the query.
        next_page: Number of the next page.
        previous_page: Number of the previous page.
    """

    count: int
    next_page: Optional[int]
    previous_page: Optional[int]
