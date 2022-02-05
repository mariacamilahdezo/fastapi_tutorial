from .. import models, schemas, oauth
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from ..database import get_db
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostResponse])
#@router.get("/")
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    results = (
        db.query(models.Post, func.count(models.Likes.post_id).label("likes"))
        .join(models.Likes, models.Likes.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .all()
    )
    print(results)
    print(limit)
    return posts


# Pydantic model, but later storing with dicts
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth.get_current_user),
):
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published),
    # )  # The order matter

    # new_post = cursor.fetchone()

    #    cursor.execute(
    #        f"INSERT INTO posts (title, content, published) VALUES({post.title}, {post.content})"
    #    ) # Waring, not use cause can give the user data manipulation
    """
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)

    """
    # print(**post.dict())
    # new_post = models.Post(
    #     title=post.title, content=post.content, published=post.published
    # )
    print(current_user.id)
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


"""
@router.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return post
"""

# Retrieve posts
@router.get("/{id}", response_model=schemas.PostResponse)
def get_posts(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth.get_current_user),
):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    # print(test_post)
    # post = find_post(id)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} not found"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    return post


"""
@app.get("/posts/{id}") # previously, if not, change to router
def get_posts(id: int, response: Response):

    post = find_post(id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message'}: f'post with id: {id} not found'}
    return {"post_detail": post}
"""


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth.get_current_user),
):
    # deleting post
    # finding the index
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)
    # if index == None:
    post_delete = db.query(models.Post).filter(models.Post.id == id)
    post = post_delete.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    # my_posts.pop(index)

    post_delete.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_posts(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth.get_current_user),
):
    # #cursor.execute(
    #     """UPDATE posts SET title = %s, content= %s, published=%s WHERE id= %s RETURNING *""",
    #     (post.title, post.content, post.published, str(id)),
    # 3)
    # #pdated_post = cursor.fetchone()
    # #conn.commit()
    # index = find_index_post(id)
    # if index == None:
    post_update = db.query(models.Post).filter(models.Post.id == id)
    post = post_update.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    post_update.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    # post_dict = post.dict()
    # post_dict["id"] = id
    # my_posts[index] = post_dict
    return Response(status_code=status.HTTP_200_OK)
