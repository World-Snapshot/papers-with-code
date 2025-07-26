from paperswithcode.models.page import Page
from paperswithcode.models.model import Model


class Author(Model):
    """Author object.

    Attributes:
        id: Author ID.
        full_name: Author full name.
    """

    id: str
    full_name: str


class Authors(Page):
    """Object representing a paginated page of authors.

    Attributes:
        count: Number of elements matching the query.
        next_page: Number of the next page.
        previous_page: Number of the previous page.
        results: List of authors on this page.
    """

    results: list[Author]
