import logging
import functools
from urllib import parse
from typing import Optional

from paperswithcode.config import config
from paperswithcode.http import HttpClient
from paperswithcode.errors import (
    HttpClientError,
    PydanticValidationError,
    ValidationError,
)
from paperswithcode.models import (
    Paper,
    Papers,
    Repository,
    Repositories,
    PaperRepos,
    Author,
    Authors,
    Conference,
    Conferences,
    Proceeding,
    Proceedings,
    Area,
    Areas,
    Task,
    TaskCreateRequest,
    TaskUpdateRequest,
    Tasks,
    Dataset,
    DatasetCreateRequest,
    DatasetUpdateRequest,
    Datasets,
    Method,
    Methods,
    Metric,
    Metrics,
    MetricCreateRequest,
    MetricUpdateRequest,
    Result,
    Results,
    ResultCreateRequest,
    ResultUpdateRequest,
    EvaluationTable,
    EvaluationTables,
    EvaluationTableCreateRequest,
    EvaluationTableUpdateRequest,
    EvaluationTableSyncRequest,
    EvaluationTableSyncResponse,
)


logger = logging.getLogger(__name__)


def handler(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except HttpClientError as e:
            if e.status_code == 401:
                # Try to refresh the token and call the function again.
                if self.http.authorization_method == self.http.Authorization.jwt:
                    try:
                        self.refresh()
                        return func(self, *args, **kwargs)
                    except Exception as e:
                        logger.warning("Failed to refresh token: %s", e)
            raise
        except PydanticValidationError as e:
            raise ValidationError(error=e)

    return wrapper


class PapersWithCodeClient:
    """PapersWithCode client."""

    def __init__(self, token=None, url=None):
        url = url or config.server_url
        self.http = HttpClient(
            url=f"{url}/api/v{config.api_version}",
            token=token or "",
            authorization_method=HttpClient.Authorization.token,
        )

    @staticmethod
    def __params(page: int, items_per_page: int, **kwargs) -> dict[str, str]:
        params = {key: str(value) for key, value in kwargs.items()}
        params["page"] = str(page)
        params["items_per_page"] = str(items_per_page)
        return params

    @staticmethod
    def __parse(url: str) -> int:
        """Return page number."""
        p = parse.urlparse(url)
        if p.query == "":
            return 1
        else:
            q = parse.parse_qs(p.query)
            return int(q.get("page", [1])[0])

    @classmethod
    def __page(cls, result, page_model):
        next_page = result["next"]
        if next_page is not None:
            next_page = cls.__parse(next_page)
        previous_page = result["previous"]
        if previous_page is not None:
            previous_page = cls.__parse(previous_page)
        return page_model(
            count=result["count"],
            next_page=next_page,
            previous_page=previous_page,
            results=result["results"],
        )

    @handler
    def search(
        self,
        q: Optional[str] = None,
        page: int = 1,
        items_per_page: int = 50,
    ) -> PaperRepos:
        """Search in a similar fashion to the frontpage search.

        Args:
            q: Filter papers by querying the paper title and abstract.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            PaperRepos object.
        """
        params = self.__params(page, items_per_page)
        timeout = None
        if q is not None:
            params["q"] = q
        return self.__page(
            self.http.get("/search/", params=params, timeout=timeout),
            PaperRepos,
        )

    @handler
    def paper_list(
        self,
        q: Optional[str] = None,
        arxiv_id: Optional[str] = None,
        title: Optional[str] = None,
        abstract: Optional[str] = None,
        ordering: Optional[str] = None,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Papers:
        """Return a paginated list of papers.

        Args:
            q: Filter papers by querying the paper title and abstract.
            arxiv_id: Filter papers by arxiv id.
            title: Filter papers by part of the title.
            abstract: Filter papers by part of the abstract.
            ordering: Which field to use when ordering the results.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            Papers object.
        """
        params = self.__params(page, items_per_page)
        timeout = None
        if q is not None:
            params["q"] = q
            timeout = 60
        if arxiv_id is not None:
            params["arxiv_id"] = arxiv_id
        if title is not None:
            params["title"] = title
        if abstract is not None:
            params["abstract"] = abstract
            timeout = 60
        if ordering is not None:
            params["ordering"] = ordering
        return self.__page(
            self.http.get("/papers/", params=params, timeout=timeout), Papers
        )

    @handler
    def paper_get(self, paper_id: str) -> Paper:
        """Return a paper by it's ID.

        Args:
            paper_id: ID of the paper.

        Returns:
            Paper object.
        """
        return Paper(**self.http.get(f"/papers/{paper_id}/"))

    @handler
    def paper_dataset_list(
        self,
        paper_id: str,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Repositories:
        """Return a list of datasets mentioned in the paper..

        Args:
            paper_id: ID of the paper.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            Datasets object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(f"/papers/{paper_id}/datasets/", params=params),
            Datasets,
        )

    @handler
    def paper_repository_list(
        self,
        paper_id: str,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Repositories:
        """Return a list of paper implementations.

        Args:
            paper_id: ID of the paper.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            Repositories object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(f"/papers/{paper_id}/repositories/", params=params),
            Repositories,
        )

    @handler
    def paper_task_list(
        self,
        paper_id: str,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Tasks:
        """Return a list of tasks mentioned in the paper.

        Args:
            paper_id: ID of the paper.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            Tasks object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(f"/papers/{paper_id}/tasks/", params=params), Tasks
        )

    @handler
    def paper_method_list(
        self,
        paper_id: str,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Methods:
        """Return a list of methods mentioned in the paper.

        Args:
            paper_id: ID of the paper.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            Methods object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(f"/papers/{paper_id}/methods/", params=params),
            Methods,
        )

    @handler
    def paper_result_list(
        self,
        paper_id: str,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Results:
        """Return a list of evaluation results for the paper.

        Args:
            paper_id: ID of the paper.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            Results object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(f"/papers/{paper_id}/results/", params=params),
            Results,
        )

    @handler
    def repository_list(
        self,
        q: Optional[str] = None,
        owner: Optional[str] = None,
        name: Optional[str] = None,
        stars: Optional[int] = None,
        framework: Optional[str] = None,
        ordering: Optional[str] = None,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Papers:
        """Return a paginated list of repositories.

        Args:
            q: Search all searchable fields.
            owner: Filter repositories by owner.
            name: Filter repositories by name.
            stars: Filter repositories by minimum number of stars.
            framework: Filter repositories by framework. Available values:
                tf, pytorch, mxnet, torch, caffe2, jax, paddle, mindspore.
            ordering: Which field to use when ordering the results.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            Repositories object.
        """
        params = self.__params(page, items_per_page)

        if q is not None:
            params["q"] = q
        if owner is not None:
            params["owner"] = owner
        if name is not None:
            params["name"] = name
        if stars is not None:
            params["stars"] = str(stars)
        if framework is not None:
            params["framework"] = framework
        if ordering is not None:
            params["ordering"] = ordering
        return self.__page(
            self.http.get("/repositories/", params=params),
            Repositories,
        )

    @handler
    def repository_owner_list(self, owner: str) -> Repositories:
        """List all repositories for a specific repo owner.

        Args:
            owner: Repository owner.

        Returns:
            Repositories object.
        """
        return self.__page(
            self.http.get(f"/repositories/{owner}"),
            Repositories,
        )

    @handler
    def repository_get(self, owner: str, name: str) -> Repository:
        """Return a repository by it's owner/name pair.

        Args:
            owner: Owner name.
            name: Repository name.

        Returns:
            Repository object.
        """
        return Repository(**self.http.get(f"/repositories/{owner}/{name}/"))

    @handler
    def repository_paper_list(
        self,
        owner: str,
        name: str,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Papers:
        """List all papers connected to the repository.

        Args:
            owner: Owner name.
            name: Repository name.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            Papers object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(f"/repositories/{owner}/{name}/papers/", params=params),
            Papers,
        )

    @handler
    def author_list(
        self,
        q: Optional[str] = None,
        full_name: Optional[str] = None,
        ordering: Optional[str] = None,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Authors:
        """Return a paginated list of paper authors.

        Args:
            q: Search all searchable fields.
            full_name: Filter authors by part of their full name.
            ordering: Which field to use when ordering the results.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            Repositories object.
        """
        params = self.__params(page, items_per_page)

        if q is not None:
            params["q"] = q
        if full_name is not None:
            params["full_name"] = full_name
        if ordering is not None:
            params["ordering"] = ordering
        return self.__page(self.http.get("/authors/", params=params), Authors)

    @handler
    def author_get(self, author_id: str) -> Author:
        """Return a specific author selected by its id.

        Args:
            author_id: Author id.

        Returns:
            Author object.
        """
        return Author(**self.http.get(f"/authors/{author_id}/"))

    @handler
    def author_paper_list(
        self,
        author_id: str,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Papers:
        """List all papers connected to the author.

        Args:
            author_id: Author id.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            Papers object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(f"/authors/{author_id}/papers/", params=params),
            Papers,
        )

    @handler
    def conference_list(
        self,
        q: Optional[str] = None,
        name: Optional[str] = None,
        ordering: Optional[str] = None,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Conferences:
        """Return a paginated list of conferences.

        Args:
            q: Search all searchable fields.
            name: Filter conferences by part of the name.
            ordering: Which field to use when ordering the results.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            Conferences object.
        """
        params = self.__params(page, items_per_page)
        if q is not None:
            params["q"] = q
        if name is not None:
            params["name"] = name
        if ordering is not None:
            params["ordering"] = ordering
        return self.__page(self.http.get("/conferences/", params=params), Conferences)

    @handler
    def conference_get(self, conference_id: str) -> Conference:
        """Return a conference by it's ID.

        Args:
            conference_id: ID of the conference.

        Returns:
            Conference object.
        """
        return Conference(**self.http.get(f"/conferences/{conference_id}/"))

    @handler
    def proceeding_list(
        self,
        conference_id: str,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Proceedings:
        """Return a paginated list of conference proceedings.

        Args:
            conference_id: ID of the conference.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            Proceedings object.
        """
        return self.__page(
            self.http.get(
                f"/conferences/{conference_id}/proceedings/",
                params=self.__params(page, items_per_page),
            ),
            Proceedings,
        )

    @handler
    def proceeding_get(self, conference_id: str, proceeding_id: str) -> Proceeding:
        """Return a conference proceeding by it's ID.

        Args:
            conference_id: ID of the conference.
            proceeding_id: ID of the proceeding.

        Returns:
            Proceeding object.
        """
        return Proceeding(
            **self.http.get(
                f"/conferences/{conference_id}/proceedings/{proceeding_id}/"
            )
        )

    @handler
    def proceeding_paper_list(
        self,
        conference_id: str,
        proceeding_id: str,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Papers:
        """Return a list of papers published in a confernce proceeding.

        Args:
            conference_id: ID of the conference.
            proceeding_id: ID of the proceding.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            Papers object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(
                f"/conferences/{conference_id}/proceedings/{proceeding_id}/papers/",
                params=params,
            ),
            Papers,
        )

    @handler
    def area_list(
        self,
        q: Optional[str] = None,
        name: Optional[str] = None,
        ordering: Optional[str] = None,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Areas:
        """Return a paginated list of areas.

        Args:
            q: Filter areas by querying the area name.
            name: Filter areas by part of the name.
            ordering: Which field to use when ordering the results.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            Areas object.
        """
        params = self.__params(page, items_per_page)
        timeout = None
        if q is not None:
            params["q"] = q
            timeout = 60
        if name is not None:
            params["name"] = name
        if ordering is not None:
            params["ordering"] = ordering
        return self.__page(
            self.http.get("/areas/", params=params, timeout=timeout), Areas
        )

    @handler
    def area_get(self, area_id: str) -> Area:
        """Return an area by it's ID.

        Args:
            area_id: ID of the area.

        Returns:
            Area object.
        """
        return Area(**self.http.get(f"/areas/{area_id}/"))

    @handler
    def area_task_list(
        self,
        area_id: str,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Tasks:
        """Return a paginated list of tasks in an area.

        Args:
            area_id: ID of the area.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            Tasks object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(f"/areas/{area_id}/tasks/", params=params), Tasks
        )

    @handler
    def task_list(
        self,
        q: Optional[str] = None,
        name: Optional[str] = None,
        ordering: Optional[str] = None,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Tasks:
        """Return a paginated list of tasks.

        Args:
            q: Filter tasks by querying the task name.
            name: Filter tasks by part of th name.
            ordering: Which field to use when ordering the results.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            Tasks object.
        """
        params = self.__params(page, items_per_page)
        timeout = None
        if q is not None:
            params["q"] = q
            timeout = 60
        if name is not None:
            params["name"] = name
        if ordering is not None:
            params["ordering"] = ordering
        return self.__page(
            self.http.get("/tasks/", params=params, timeout=timeout), Tasks
        )

    @handler
    def task_get(self, task_id: str) -> Task:
        """Return a task by it's ID.

        Args:
            task_id: ID of the task.

        Returns:
            Task object.
        """
        return Task(**self.http.get(f"/tasks/{task_id}/"))

    @handler
    def task_add(self, task: TaskCreateRequest) -> Task:
        """Add a task.

        Args:
           task: Task create request.

        Returns:
            Created task.
        """
        return Task(**self.http.post("/tasks/", data=task))

    @handler
    def task_update(self, task_id: str, task: TaskUpdateRequest) -> Task:
        """Update a task.

        Args:
            task_id: ID of the task.
            task: Task update request.

        Returns:
            Updated task.
        """
        return Task(**self.http.patch(f"/tasks/{task_id}/", data=task))

    @handler
    def task_delete(self, task_id: str):
        """Delete a task.

        Args:
            task_id: ID of the task.
        """
        self.http.delete(f"/tasks/{task_id}/")

    @handler
    def task_parent_list(
        self,
        task_id: str,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Tasks:
        """Return a paginated list of parent tasks for a selected task.

        Args:
            task_id: ID of the task.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            Tasks object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(f"/tasks/{task_id}/parents/", params=params), Tasks
        )

    @handler
    def task_child_list(
        self,
        task_id: str,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Tasks:
        """Return a paginated list of child tasks for a selected task.

        Args:
            task_id: ID of the task.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            Tasks object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(f"/tasks/{task_id}/children/", params=params), Tasks
        )

    @handler
    def task_paper_list(
        self,
        task_id: str,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Papers:
        """Return a paginated list of papers for a selected task.

        Args:
            task_id: ID of the task.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            Papers object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(f"/tasks/{task_id}/papers/", params=params), Papers
        )

    @handler
    def task_evaluation_list(
        self,
        task_id: str,
        page: int = 1,
        items_per_page: int = 50,
    ) -> EvaluationTables:
        """Return a list of evaluation tables for a selected task.

        Args:
            task_id: ID of the task.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            EvaluationTables object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(f"/tasks/{task_id}/evaluations/", params=params),
            EvaluationTables,
        )

    @handler
    def dataset_list(
        self,
        q: Optional[str] = None,
        name: Optional[str] = None,
        full_name: Optional[str] = None,
        ordering: Optional[str] = None,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Datasets:
        """Return a paginated list of datasets.

        Args:
            q: Filter datasets by querying the dataset name.
            name: Filter datasets by their name.
            full_name: Filter datasets by their full name.
            ordering: Which field to use when ordering the results.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            Datasets object.
        """
        params = self.__params(page, items_per_page)
        timeout = None
        if q is not None:
            params["q"] = q
            timeout = 60
        if name is not None:
            params["name"] = name
        if full_name is not None:
            params["full_name"] = full_name
        if ordering is not None:
            params["ordering"] = ordering
        return self.__page(
            self.http.get("/datasets/", params=params, timeout=timeout),
            Datasets,
        )

    @handler
    def dataset_get(self, dataset_id: str) -> Dataset:
        """Return a dastaset by it's ID.

        Args:
            dataset_id: ID of the dataset.

        Returns:
            Dataset object.
        """
        return Dataset(**self.http.get(f"/datasets/{dataset_id}/"))

    @handler
    def dataset_add(self, dataset: DatasetCreateRequest) -> Dataset:
        """Add a dataset.

        Args:
           dataset: Dataset create request.

        Returns:
            Created dataset.
        """
        return Dataset(**self.http.post("/datasets/", data=dataset))

    @handler
    def dataset_update(self, dataset_id: str, dataset: DatasetUpdateRequest) -> Dataset:
        """Update a dataset.

        Args:
            dataset_id: ID of the dataset.
            dataset: Dataset update request.

        Returns:
            Updated dataset.
        """
        return Dataset(**self.http.patch(f"/datasets/{dataset_id}/", data=dataset))

    @handler
    def dataset_delete(self, dataset_id: str):
        """Delete a dataset.

        Args:
            dataset_id: ID of the dataset.
        """
        self.http.delete(f"/datasets/{dataset_id}/")

    @handler
    def dataset_evaluation_list(
        self,
        dataset_id: str,
        page: int = 1,
        items_per_page: int = 50,
    ) -> EvaluationTables:
        """Return a list of evaluation tables for a selected dataset.

        Args:
            dataset_id: ID of the dasaset.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
           EvaluationTables object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(f"/datasets/{dataset_id}/evaluations/", params=params),
            EvaluationTables,
        )

    @handler
    def method_list(
        self,
        q: Optional[str] = None,
        name: Optional[str] = None,
        full_name: Optional[str] = None,
        ordering: Optional[str] = None,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Methods:
        """Return a paginated list of methods.

        Args:
            q: Search all searchable fields.
            name: Filter methods by part of the name.
            full_name: Filter methods by part of the full name.
            ordering: Which field to use when ordering the results.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            Methods object.
        """
        params = self.__params(page, items_per_page)
        timeout = None
        if q is not None:
            params["q"] = q
            timeout = 60
        if name is not None:
            params["name"] = name
        if full_name is not None:
            params["full_name"] = full_name
        if ordering is not None:
            params["ordering"] = ordering
        return self.__page(
            self.http.get("/methods/", params=params, timeout=timeout),
            Methods,
        )

    @handler
    def method_get(self, method_id) -> Method:
        """Return a method by it's ID.

        Args:
            method_id: ID of the method.

        Returns:
            Method object.
        """
        return Method(**self.http.get(f"/methods/{method_id}/"))

    @handler
    def evaluation_list(
        self,
        page: int = 1,
        items_per_page: int = 50,
    ) -> EvaluationTables:
        """Return a paginated list of evaluation tables.

        Args:
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            Evaluation table page object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get("/evaluations/", params=params), EvaluationTables
        )

    @handler
    def evaluation_get(self, evaluation_id: str) -> EvaluationTable:
        """Return a evaluation table by it's ID.

        Args:
            evaluation_id: ID of the evaluation table.

        Returns:
            Evaluation table object.
        """
        return EvaluationTable(**self.http.get(f"/evaluations/{evaluation_id}/"))

    @handler
    def evaluation_create(
        self,
        evaluation: EvaluationTableCreateRequest,
    ) -> EvaluationTable:
        """Create an evaluation table.

        Args:
            evaluation: Evaluation table create request object.

        Returns:
            The new created evaluation table.
        """
        return EvaluationTable(**self.http.post("/evaluations/", data=evaluation))

    @handler
    def evaluation_update(
        self,
        evaluation_id: str,
        evaluation: EvaluationTableUpdateRequest,
    ) -> EvaluationTable:
        """Update an evaluation table.

        Args:
            evaluation_id: ID of the evaluation table.
            evaluation: Evaluation table update request object.

        Returns:
            The updated evaluation table.
        """
        return EvaluationTable(
            **self.http.patch(f"/evaluations/{evaluation_id}/", data=evaluation)
        )

    @handler
    def evaluation_delete(self, evaluation_id: str):
        """Delete an evaluation table.

        Args:
            evaluation_id: ID of the evaluation table.
        """
        self.http.delete(f"/evaluations/{evaluation_id}/")

    @handler
    def evaluation_metric_list(
        self,
        evaluation_id: str,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Metrics:
        """List all metrics used in the evaluation table.

        Args:
            evaluation_id: ID of the evaluation table.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            Metrics object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(f"/evaluations/{evaluation_id}/metrics/", params=params),
            Metrics,
        )

    @handler
    def evaluation_metric_get(self, evaluation_id: str, metric_id: str) -> Metric:
        """Get a metrics used in the evaluation table.

        Args:
            evaluation_id: ID of the evaluation table.
            metric_id: ID of the metric.

        Returns:
            Requested metric.
        """
        return Metric(
            **self.http.get(f"/evaluations/{evaluation_id}/metrics/{metric_id}/")
        )

    @handler
    def evaluation_metric_add(
        self,
        evaluation_id: str,
        metric: MetricCreateRequest,
    ) -> Metric:
        """Add a metrics to the evaluation table.

        Args:
            evaluation_id: ID of the evaluation table.
            metric: Metric create request.

        Returns:
            Created metric.
        """
        return Metric(
            **self.http.post(f"/evaluations/{evaluation_id}/metrics/", data=metric)
        )

    @handler
    def evaluation_metric_update(
        self,
        evaluation_id: str,
        metric_id: str,
        metric: MetricUpdateRequest,
    ) -> Metric:
        """Update a metrics in the evaluation table.

        Args:
            evaluation_id: ID of the evaluation table.
            metric_id: ID of the metric.
            metric: Metric update request.

        Returns:
            Updated metric.
        """
        return Metric(
            **self.http.patch(
                f"/evaluations/{evaluation_id}/metrics/{metric_id}/",
                data=metric,
            )
        )

    @handler
    def evaluation_metric_delete(self, evaluation_id: str, metric_id: str):
        """Delete a metrics from the evaluation table.

        Args:
            evaluation_id: ID of the evaluation table.
            metric_id: ID of the metric.
        """
        self.http.delete(f"/evaluations/{evaluation_id}/metrics/{metric_id}/")

    @handler
    def evaluation_result_list(
        self,
        evaluation_id: str,
        page: int = 1,
        items_per_page: int = 50,
    ) -> Results:
        """List all results from the evaluation table.

        Args:
            evaluation_id: ID of the evaluation table.
            page: Desired page.
            items_per_page: Desired number of items per page.

        Returns:
            Results object.
        """
        params = self.__params(page, items_per_page)
        return self.__page(
            self.http.get(f"/evaluations/{evaluation_id}/results/", params=params),
            Results,
        )

    @handler
    def evaluation_result_get(self, evaluation_id: str, result_id: str) -> Result:
        """Get a result from the evaluation table.

        Args:
            evaluation_id: ID of the evaluation table.
            result_id: ID of the result.

        Returns:
            Requested result.
        """
        return Result(
            **self.http.get(f"/evaluations/{evaluation_id}/results/{result_id}/")
        )

    @handler
    def evaluation_result_add(
        self,
        evaluation_id: str,
        result: ResultCreateRequest,
    ) -> Result:
        """Add a result to the evaluation table.

        Args:
            evaluation_id: ID of the evaluation table.
            result: Result create request.

        Returns:
            Created result.
        """
        return Result(
            **self.http.post(f"/evaluations/{evaluation_id}/results/", data=result)
        )

    @handler
    def evaluation_result_update(
        self,
        evaluation_id: str,
        result_id: str,
        result: ResultUpdateRequest,
    ) -> Result:
        """Update a result in the evaluation table.

        Args:
            evaluation_id: ID of the evaluation table.
            result_id: ID of the result.
            result: Result update request.

        Returns:
            Updated result.
        """
        return Result(
            **self.http.patch(
                f"/evaluations/{evaluation_id}/results/{result_id}/",
                data=result,
            )
        )

    @handler
    def evaluation_result_delete(self, evaluation_id: str, result_id: str):
        """Delete a result from the evaluation table.

        Args:
            evaluation_id: ID of the evaluation table.
            result_id: ID of the result.
        """
        self.http.delete(f"/evaluations/{evaluation_id}/results/{result_id}/")

    @handler
    def evaluation_synchronize(
        self,
        evaluation: EvaluationTableSyncRequest,
    ) -> EvaluationTableSyncResponse:
        d = self.http.post("/rpc/evaluation-synchronize/", data=evaluation)
        d["results"] = [result for result in d["results"]]
        return EvaluationTableSyncResponse(**d)
