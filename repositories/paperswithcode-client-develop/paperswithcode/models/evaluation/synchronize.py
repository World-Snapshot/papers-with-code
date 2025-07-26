from pydantic import Field
from typing import Optional

from paperswithcode.models.model import Model
from paperswithcode.models.evaluation.result import _ResultRequest


class ResultSyncRequest(_ResultRequest):
    """Evaluation table row object.

    Attributes:
        metrics: Dictionary of metrics and metric values.
        methodology: Methodology used for this implementation.
        uses_additional_data: Does this evaluation uses additional data not provided
            in the dataset used for other evaluations.
        paper: Paper describing the evaluation.
        external_id: Optional external ID used to identify rows when doing sync.
        evaluated_on: Evaluation date in YYYY-MM-DD format
        external_source_url: The URL to the external source (eg competition).
    """

    metrics: dict
    methodology: str
    paper: Optional[str]
    uses_additional_data: bool = False
    external_id: Optional[str] = ""
    evaluated_on: str
    external_source_url: Optional[str] = None


class MetricSyncRequest(Model):
    """Metric object.

    Metric used for evaluation.

    Attributes:
        name: Metric name.
        description: Metric description.
        is_loss: Is this a loss metric.
    """

    name: str
    description: str = ""
    is_loss: bool = True


class EvaluationTableSyncRequest(Model):
    """Evaluation table object.

    Attributes:
        task: ID of the task used in evaluation.
        dataset: ID of the dataset used in evaluation.
        description: Evaluation table description.
        mirror_url: URL to the evaluation table that this table is a mirror of.
        external_id: Optional external ID used to identify rows when doing sync.
        metric: List of MetricSyncRequest objects used in the evaluation.
        results: List of ResultSyncRequest objects - results of the evaluation.
    """

    task: str
    dataset: str
    description: str = ""
    mirror_url: Optional[str] = None
    external_id: Optional[str] = None
    metrics: list[MetricSyncRequest] = Field(default_factory=list)
    results: list[ResultSyncRequest] = Field(default_factory=list)


class ResultSyncResponse(Model):
    """Evaluation table row object.

    Attributes:
        id: Result id.
        metrics: Dictionary of metrics and metric values.
        methodology: Methodology used for this implementation.
        uses_additional_data: Does this evaluation uses additional data not provided
            in the dataset used for other evaluations.
        paper: Paper describing the evaluation.
        external_id: Optional external ID used to identify rows when doing sync.
        evaluated_on: Evaluation date in YYYY-MM-DD format
        external_source_url: The URL to the external source (eg competition)
    """

    id: str
    metrics: dict
    methodology: str
    paper: Optional[str]
    uses_additional_data: bool = False
    external_id: Optional[str] = ""
    evaluated_on: Optional[str] = None
    external_source_url: Optional[str] = None


class MetricSyncResponse(Model):
    """Metric object.

    Metric used for evaluation.

    Attributes:
        name: Metric name.
        description: Metric description.
        is_loss: Is this a loss metric.
    """

    name: str
    description: str = ""
    is_loss: bool = True


class EvaluationTableSyncResponse(Model):
    """Evaluation table object.

    Attributes:
        id: Evaluation table ID.
        task: ID of the task used in evaluation.
        dataset: ID of the dataset used in evaluation.
        description: Evaluation table description.
        mirror_url: URL to the evaluation table that this table is a mirror of.
        external_id: Optional external ID used to identify rows when doing sync.
        metric: List of metrics sync objects used in the evaluation.
        results: List of result sync objects - results of the evaluation.
    """

    id: str
    task: str
    dataset: str
    description: str = ""
    mirror_url: Optional[str] = None
    external_id: Optional[str] = ""
    metrics: list[MetricSyncResponse] = Field(default_factory=list)
    results: list[ResultSyncResponse] = Field(default_factory=list)
