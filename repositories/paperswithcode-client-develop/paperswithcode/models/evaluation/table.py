from typing import Optional

from paperswithcode.models.page import Page
from paperswithcode.models.model import Model


class EvaluationTable(Model):
    """Evaluation table object.

    Attributes:
        id: Evaluation table ID.
        task: ID of the task used in evaluation.
        dataset: ID of the dataset used in evaluation.
        description: Evaluation table description.
        mirror_url: URL to the evaluation table that this table is a mirror of.
    """

    id: str
    task: str
    dataset: str
    description: str = ""
    mirror_url: Optional[str] = None


class EvaluationTableCreateRequest(Model):
    """Evaluation table create request object.

    Attributes:
        task: ID of the task used in evaluation.
        dataset: ID of the dataset used in evaluation.
        description: Evaluation table description.
        mirror_url: URL to the evaluation table that this table is a mirror of.
    """

    task: str
    dataset: str
    description: str = ""
    mirror_url: Optional[str] = None


class EvaluationTableUpdateRequest(Model):
    """Evaluation table update request object.

    Attributes:
        task: ID of the task used in evaluation.
        dataset: ID of the dataset used in evaluation.
        description: Evaluation table description.
        mirror_url: URL to the evaluation table that this table is a mirror of.
    """

    task: Optional[str] = None
    dataset: Optional[str] = None
    description: Optional[str] = None
    mirror_url: Optional[str] = None


class EvaluationTables(Page):
    """Object representing a paginated page of evaluation tables.

    Attributes:
        count: Number of elements matching the query.
        next_page: Number of the next page.
        previous_page: Number of the previous page.
        results: List of evaluation tables on this page.
    """

    results: list[EvaluationTable]
