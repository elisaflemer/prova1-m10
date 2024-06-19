import pydantic

class CreateReviewRequest(pydantic.BaseModel):
    usuario : str
    review: str
    serie_filme: str
    estrelas: int
