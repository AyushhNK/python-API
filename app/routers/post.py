from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from typing import List
from ..database import engine,get_db
from .. import models,schemas,utils

router=APIRouter(
	prefix="/posts",
	tags=['Posts']
	)


@router.get('/',response_model=List[schemas.PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
	# cursor.execute("""SELECT * FROM posts""")
	# posts=cursor.fetchall()
	posts=db.query(models.Post).all()
	return posts

# @router.post('/createpost')
# def create_post(payload:dict=Body(...)):
# 	print(payload)
# 	return {"title":payload['title'],"content":payload['content']}


@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_post(post:schemas.CreatePost,db: Session = Depends(get_db)):
	# cursor.execute("""INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
	# new_post=cursor.fetchone()
	# conn.commit()

	new_post=models.Post(**post.dict())
	db.add(new_post)
	db.commit()
	db.refresh(new_post)
	return new_post


@router.get('/{id}',response_model=schemas.PostResponse)
def get_post(id:int,response:Response,db: Session = Depends(get_db)):
	# cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id)))
	# post=cursor.fetchone()

	post=db.query(models.Post).filter(models.Post.id==id).first()
	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with id:{id} not found")
	return post


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db)):
	# cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(str(id)))
	# deleted_post=cursor.fetchone()
	# conn.commit()

	post=db.query(models.Post).filter(models.Post.id==id)
	if post.first()==None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with id:{id} not found")
	else:
		post.delete()
		db.commit()
	return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}',response_model=schemas.PostResponse)
def update_post(id:int,post:schemas.CreatePost):
	# cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,str(id)))
	# updated_post=cursor.fetchone()
	# conn.commit()

	post_query=db.query(models.Post).filter(models.Post.id==id)
	p=post_query.first()

	if post==None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with id:{id} not found")
	p.update(post.dict())
	db.commit()
	return updated_post
