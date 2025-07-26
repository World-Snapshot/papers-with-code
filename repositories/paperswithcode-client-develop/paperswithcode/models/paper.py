from datetime import date
from typing import Optional

from paperswithcode.models.page import Page
from paperswithcode.models.model import Model


class Paper(Model):
    """Paper object.

    Attributes:
        id: Paper ID.
        arxiv_id: ArXiv ID.
        nips_id: NIPS Conference ID.
        url_abs: URL to the paper abstract.
        url_pdf: URL to the paper PDF.
        title: Paper title.
        abstract: Paper abstract.
        authors: List of paper authors.
        published: Paper publication date.
        conference: ID of the conference in which the paper was published.
        conference_url_abs: URL to the conference paper page.
        conference_url_pdf: URL to the conference paper PDF.
        proceeding: ID of the conference proceeding in which the paper was published.
    """

    id: str
    arxiv_id: Optional[str]
    nips_id: Optional[str]
    url_abs: str
    url_pdf: str
    title: str
    abstract: str
    authors: list[str]
    published: date
    conference: Optional[str]
    conference_url_abs: Optional[str]
    conference_url_pdf: Optional[str]
    proceeding: Optional[str]


class Papers(Page):
    """Object representing a paginated page of papers.

    Attributes:
        count: Number of elements matching the query.
        next_page: Number of the next page.
        previous_page: Number of the previous page.
        results: List of papers on this page.
    """

    results: list[Paper]
