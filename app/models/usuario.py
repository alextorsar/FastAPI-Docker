from pydantic import BaseModel


class UsuarioMongo(BaseModel):
    name: str
    reviewerId: str
    reviewerUrl: str
    reviewerNumberOfReviews: int
    isLocalGuide: bool
    numReviewsEnBD: int
