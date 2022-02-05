from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oauth
from sqlalchemy.orm import Session

router = APIRouter(prefix="/likes", tags=["Likes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def like(
    like: schemas.Likes,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth.get_current_user),
):

    post = db.query(models.Post).filter(models.Post.id == like.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {like.post_id} does not exist",
        )
    like_query = db.query(models.Likes).filter(
        models.Likes.post_id == like.post_id,
        models.Likes.user_id == current_user.id,
    )
    found_like = like_query.first()
    if like.dir == 1:
        if found_like:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User: {current_user.id} has already liked post {like.post_id}",
            )

        new_like = models.Likes(post_id=like.post_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "Successfully added like"}

    else:
        if not found_like:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Like does not exist"
            )

        like_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted like"}
