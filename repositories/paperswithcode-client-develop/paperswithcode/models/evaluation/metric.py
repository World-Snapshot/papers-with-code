from typing import Optional

from paperswithcode.models.page import Page
from paperswithcode.models.model import Model


class Metric(Model):
    """Metric object.

    Metric used for evaluation.

    Attributes:
        id: Metric id.
        name: Metric name.
        description: Metric description.
        is_loss: Is this a loss metric.
    """

    id: str
    name: str
    description: str
    is_loss: bool


class Metrics(Page):
    """Object representing a paginated page of metrics.

    Attributes:
        count: Number of elements matching the query.
        next_page: Number of the next page.
        previous_page: Number of the previous page.
        results: List of metrics on this page.
    """

    results: list[Metric]


class MetricCreateRequest(Model):
    """Metric object.

    Metric used for evaluation.

    Attributes:
        name: Metric name.
        description: Metric description.
        is_loss: Is this a loss metric.
    """

    name: str
    description: str
    is_loss: bool


class MetricUpdateRequest(Model):
    """Metric object.

    Metric used for evaluation.

    Attributes:
        name: Metric name.
        description: Metric description.
        is_loss: Is this a loss metric.
    """

    name: Optional[str] = None
    description: Optional[str] = None
    is_loss: Optional[bool] = None
