from typing import Optional


from paperswithcode.models.page import Page
from paperswithcode.models.model import Model


class Dataset(Model):
    """Dataset object.

    Attributes:
        id: Dataset ID.
        name: Dataset name.
        full_name: Dataset full name.
        url: URL for dataset download.
    """

    id: str
    name: str
    full_name: Optional[str]
    url: Optional[str]


class DatasetCreateRequest(Model):
    """Task object.

    Attributes:
        name: Dataset name.
        full_name: Dataset full name.
        url: Dataset url.
    """

    name: str
    full_name: Optional[str] = None
    url: Optional[str] = None


class DatasetUpdateRequest(Model):
    """Evaluation table row object.

    Attributes:
        name: Dataset name.
        url: Dataset url.
    """

    name: Optional[str] = None
    url: Optional[str] = None


class Datasets(Page):
    """Object representing a paginated page of datasets.

    Attributes:
        count: Number of elements matching the query.
        next_page: Number of the next page.
        previous_page: Number of the previous page.
        results: List of datasets on this page.
    """

    results: list[Dataset]
