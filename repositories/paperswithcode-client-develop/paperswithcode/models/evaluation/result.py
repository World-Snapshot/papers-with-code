from typing import Optional
from datetime import datetime

from paperswithcode.models.page import Page
from paperswithcode.models.model import Model


class Result(Model):
    """Evaluation table row object.

    Attributes:
        id: Result id.
        best_rank: Best rank of the row.
        metrics: Dictionary of metrics and metric values.
        methodology: Methodology used for this implementation.
        uses_additional_data: Does this evaluation uses additional data not provided
            in the dataset used for other evaluations.
        paper: Paper describing the evaluation.
        best_metric: Name of the best metric.
        evaluated_on: Date of the result evaluation in YYYY-MM-DD format.
        external_source_url: The URL to the external source (eg competition).
    """

    id: str
    best_rank: Optional[int]
    metrics: dict
    methodology: str
    uses_additional_data: bool
    paper: Optional[str]
    best_metric: Optional[str]
    evaluated_on: Optional[str]
    external_source_url: Optional[str]


class Results(Page):
    """Object representing a paginated page of results.

    Attributes:
        count: Number of elements matching the query.
        next_page: Number of the next page.
        previous_page: Number of the previous page.
        results: List of results on this page.
    """

    results: list[Result]


class _ResultRequest(Model):
    def dict(
        self,
        *,
        include=None,
        exclude=None,
        by_alias: bool = False,
        skip_defaults: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ):
        d = super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )
        evaluated_on = d.get("evaluated_on")
        if isinstance(evaluated_on, datetime):
            d["evaluated_on"] = evaluated_on.strftime("%Y-%m-%d")
        return d


class ResultCreateRequest(_ResultRequest):
    """Evaluation table row object.

    Attributes:
        metrics: Dictionary of metrics and metric values.
        methodology: Methodology used for this implementation.
        uses_additional_data: Does this evaluation uses additional data not provided
            in the dataset used for other valuations.
        paper: Paper describing the evaluation.
        evaluated_on: Date of the result evaluation: YYYY-MM-DD format.
        external_source_url: The URL to the external source (eg competition).
    """

    metrics: dict
    methodology: str
    uses_additional_data: Optional[bool] = False
    paper: Optional[str] = None
    evaluated_on: Optional[str] = None
    external_source_url: Optional[str] = None


class ResultUpdateRequest(_ResultRequest):
    """Evaluation table row object.

    Attributes:
        metrics: Dictionary of metrics and metric values.
        methodology: Methodology used for this implementation.
        uses_additional_data: Does this evaluation uses additional data not provided
            in the dataset used for other evaluations.
        paper: Paper describing the evaluation.
        evaluated_on: Date of the result evaluation: YYYY-MM-DD format.
        external_source_url: The URL to the external source (eg competition).
    """

    metrics: Optional[dict] = None
    methodology: Optional[str] = None
    uses_additional_data: Optional[bool] = None
    paper: Optional[str] = None
    evaluated_on: Optional[str] = None
    external_source_url: Optional[str] = None
