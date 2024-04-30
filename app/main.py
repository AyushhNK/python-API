from fastapi import FastAPI,Response,status,HTTPException,Depends
from typing import List
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from . import models,schemas,utils
from .database import engine,get_db

load_dotenv()



models.Base.metadata.create_all(bind=engine)

app=FastAPI()


PASSWORD=os.environ.get('POSTGRES_PASSWORD')

while True:
	try:
		conn=psycopg2.connect(host="localhost",database="fastapi",user="postgres",password=PASSWORD,cursor_factory=RealDictCursor)
		cursor=conn.cursor()
		print("connection to the database sucessful")
		break
	except Exception as error:
		print("connection to the database failed")
		print("error:",error)
		time.sleep(2)

my_post=[{"id":1,"title":"homework","content":"i did my homework"},{"id":2,"title":"title for post2","content":"content for post 2"}]

def find_post(id):
	for p in my_post:
		if p["id"]==id:
			return p


def find_index(id):
	for i,p in enumerate(my_post):
		if p["id"]==id:
			return i

@app.get('/posts',response_model=List[schemas.PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
	# cursor.execute("""SELECT * FROM posts""")
	# posts=cursor.fetchall()
	posts=db.query(models.Post).all()
	return posts

# @app.post('/createpost')
# def create_post(payload:dict=Body(...)):
# 	print(payload)
# 	return {"title":payload['title'],"content":payload['content']}


@app.post('/posts',status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_post(post:schemas.CreatePost,db: Session = Depends(get_db)):
	# cursor.execute("""INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
	# new_post=cursor.fetchone()
	# conn.commit()

	new_post=models.Post(**post.dict())
	db.add(new_post)
	db.commit()
	db.refresh(new_post)
	return new_post


@app.get('/posts/{id}',response_model=schemas.PostResponse)
def get_post(id:int,response:Response,db: Session = Depends(get_db)):
	# cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id)))
	# post=cursor.fetchone()

	post=db.query(models.Post).filter(models.Post.id==id).first()
	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with id:{id} not found")
	return post


@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
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

@app.put('/posts/{id}',response_model=schemas.PostResponse)
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


@app.post('/users',status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db: Session = Depends(get_db)):

	hashed_password=utils.hash(user.password)
	user.password=hashed_password
	new_user=models.User(**user.dict())
	db.add(new_user)
	db.commit()
	db.refresh(new_user)
	return new_user

@app.get('/users/{id}',response_model=schemas.UserOut)
def get_user(id:int,db: Session = Depends(get_db)):
	user=db.query(models.User).filter(models.User.id==id).first()
	if user is None:
		raise HTTPException(status_code=HTTP_404_NOT_FOUND,detail=f"user with {id} not found")
	return user
