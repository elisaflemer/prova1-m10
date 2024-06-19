from fastapi import APIRouter, HTTPException, status, Depends
from models.reviews import Review
from models.schemas import CreateReviewRequest
from database import get_db
from cache import redis_client
from sqlalchemy.orm import Session
from sqlalchemy import update

from typing import List

import logging

LOGGER = logging.getLogger(__name__)

router = APIRouter(tags=["reviews"])


@router.post("/")
def create_review(
    review: CreateReviewRequest,
    status_code=status.HTTP_201_CREATED,
    db: Session = Depends(get_db),
):
    LOGGER.info(
        {
            "message": "Creating review",
            "status": "success",
            "method": "POST",
            "url": "/review",
        }
    )
    try:

        review = Review(
            usuario=review.usuario,
            review=review.review,
            serie_filme=review.serie_filme,
            estrelas=review.estrelas,
        )
        LOGGER.debug(msg=f"New review: {review}")

        db.add(review)
        db.commit()
        db.refresh(review)
        review = review.to_dict()
        return {"id": review["id"]}

    except KeyError:
        LOGGER.warning(
            {
                "message": "Invalid request",
                "status": "error",
                "method": "POST",
                "url": "/review",
            }
        )
        raise HTTPException(status_code=400, detail="Invalid request")

    except Exception as e:
        LOGGER.error(
            {
                "message": "Error creating post",
                "status": "error",
                "method": "POST",
                "url": "/review",
                "error": str(e),
            }
        )
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
def get_reviews(db: Session = Depends(get_db)):
    LOGGER.info(
        {
            "message": "Getting reviews",
            "status": "success",
            "method": "GET",
            "url": "/review",
        }
    )
    resultado = redis_client.get("reviews")
    if resultado:
        return {"reviews": eval(resultado.decode())}
    reviews = db.query(Review).all()
    redis_client.set("reviews", str([review.to_dict() for review in reviews]), 10)
    return {"reviews": [review.to_dict() for review in reviews]}


@router.get("/{id}")
def get_review(id: int, db: Session = Depends(get_db)):
    LOGGER.info(
        {
            "message": "Getting review",
            "id": id,
            "status": "success",
            "method": "GET",
            "url": "/review",
        }
    )
    resultado = redis_client.get("review-" + str(Review.id))
    if resultado:
        return {"review": eval(resultado.decode())}
    try: 
        review = db.query(Review).filter(Review.id == id).first()
        redis_client.set("review-" + str(Review.id), str(review), 10)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        return {"review": review.to_dict()}
    except Exception as e:
        LOGGER.error(
            {
                "message": "Error getting review",
                "id": id,
                "status": "error",
                "method": "GET",
                "url": "/review",
                "error": str(e),
            }
        )
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}")
def delete_review(id: int, db: Session = Depends(get_db), status_code=status.HTTP_204_NO_CONTENT):
    try:
        LOGGER.info(
            {
                "message": "Deleting review",
                "id": id,
                "status": "success",
                "method": "DELETE",
                "url": "/review",
            }
        )
        review = db.query(Review).filter(Review.id == id).first()
        db.delete(review)
        db.commit()
        return {"status": "deleted successfully"}
    except Exception as e:
        LOGGER.error(
            {
                "message": "Error deleting review",
                "id": id,
                "status": "error",
                "method": "DELETE",
                "url": "/review",
                "error": str(e),
            }
        )
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{id}")
def update_review(id: int, review: CreateReviewRequest, db: Session = Depends(get_db), status_code=status.HTTP_200_OK):
    try:
        LOGGER.info(
            {
                "message": "Updating review",
                "id": id,
                "status": "success",
                "method": "PUT",
                "url": "/review",
            }
        )
        db.query(Review).filter(Review.id == id).update({
            "usuario": review.usuario,
            "review": review.review,
            "serie_filme": review.serie_filme,
            "estrelas": review.estrelas
        
        })
        db.commit()
        db.flush()
        return {"review": {
            "id": id,
            "usuario": review.usuario,
            "review": review.review,
            "serie_filme": review.serie_filme,
            "estrelas": review.estrelas
        
        }}
        
    except Exception as e:
        LOGGER.error(
            {
                "message": "Error updating review",
                "id": id,
                "status": "error",
                "method": "PUT",
                "url": "/review",
                "error": str(e),
            }
        )
        raise HTTPException(status_code=500, detail=str(e))
