from typing import NamedTuple


class AmazonBookReview(NamedTuple):
    reviewer_id: str
    asin: str
    reviewer_name: str
    helpful: list[int, int]
    review_text: str
    overall: float
    summary: str
    unix_review_time: int
    review_time: str
