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

    def __eq__(self, other: NamedTuple) -> bool:
        ignore_fields = {"id"}
        return all((value == other.__dict__[key]) for key, value in self.__dict__.items()
                   if key not in ignore_fields)

    def __ne__(self, other: NamedTuple) -> bool:
        return not self.__eq__(other)
