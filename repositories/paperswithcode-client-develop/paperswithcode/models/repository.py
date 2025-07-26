from typing import Optional

from paperswithcode.models.page import Page
from paperswithcode.models.model import Model


class Repository(Model):
    """Repository object.

    Attributes:
        url: URL of the repository.
        owner: Repository owner.
        name: Repository name.
        description: Repository description.
        stars: Number of repository stars.
        framework: Implementation framework (TensorFlow, PyTorch, MXNet, Torch, Jax,
            Caffee2...).
        is_official: Is this an official implementation of the paper.
            Available only when listing repositories for a specific paper.
    """

    url: str
    owner: str
    name: str
    description: str
    stars: int
    framework: str
    is_official: Optional[bool]


class Repositories(Page):
    """Object representing a paginated page of repositories.

    Attributes:
        count: Number of elements matching the query.
        next_page: Number of the next page.
        previous_page: Number of the previous page.
        results: List of repositories on this page.
    """

    results: list[Repository]
