from fastapi import FastAPI,Response,status,HTTPException,Depends

from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import os
from dotenv import load_dotenv
from .database import engine,get_db
from . import models,schemas,utils
from .routers import user,post

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


app.include_router(user.router)
app.include_router(post.router)