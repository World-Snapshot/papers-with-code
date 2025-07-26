from typing import Optional

from paperswithcode.models.page import Page
from paperswithcode.models.model import Model


class Area(Model):
    """Area object.

    Representing an area of research.

    Attributes:
        id: Area ID.
        name: Area name.
    """

    id: str
    name: str


class Areas(Page):
    """Object representing a paginated page of areas.

    Attributes:
        count: Number of elements matching the query.
        next_page: Number of the next page.
        previous_page: Number of the previous page.
        results: List of areas on this page.
    """

    results: list[Area]


class Task(Model):
    """Task object.

    Attributes:
        id: Task ID.
        name: Task name.
        description: Task description.
    """

    id: str
    name: str
    description: str


class TaskCreateRequest(Model):
    """Task object.

    Attributes:
        name: Task name.
        description: Task description.
        area: Task area ID or area name.
        parent_task: ID of the parent task.
    """

    name: str
    description: str = ""
    area: Optional[str] = None
    parent_task: Optional[str] = None


class TaskUpdateRequest(Model):
    """Evaluation table row object.

    Attributes:
        name: Task name.
        description: Task description.
        area: Task area ID.
        parent_task: ID of the parent task.
    """

    name: Optional[str] = None
    description: Optional[str] = None
    area: Optional[str] = None
    parent_task: Optional[str] = None


class Tasks(Page):
    """Object representing a paginated page of tasks.

    Attributes:
        count: Number of elements matching the query.
        next_page: Number of the next page.
        previous_page: Number of the previous page.
        results: List of tasks on this page.
    """

    results: list[Task]
