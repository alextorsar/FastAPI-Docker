from pydantic import BaseModel
from typing import Optional


class ReviewMongo(BaseModel):
    placeId: Optional[str]
    restaurantName: Optional[str]
    name: Optional[str]
    text: str
    publishedAtDate: Optional[str]
    likesCount: Optional[int]
    reviewId: Optional[str]
    reviewerId: Optional[str]
    reviewerUrl: Optional[str]
    reviewerNumberOfReviews: Optional[int]
    isLocalGuide: Optional[bool]
    stars: int
    lastReview: Optional[bool]
    userOid: str
    restaurantOid: str
