from pydantic import BaseModel


class ReviewMongo(BaseModel):
    placeId: str
    restaurantName: str
    name: str
    text: str
    publishedAtDate: str
    likesCount: int
    reviewId: str
    reviewerId: str
    reviewerUrl: str
    reviewerNumberOfReviews: int
    isLocalGuide: bool
    stars: int
    lastReview: bool
