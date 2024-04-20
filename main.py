from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app=FastAPI()

class Post(BaseModel):
	title:str
	content:str
	published:bool=True
	rating:int|None=None

my_post=[{"id":1,"title":"homework","content":"i did my homework"},{"id":2,"title":"title for post2","content":"content for post 2"}]

def find_post(id):
	for p in my_post:
		if p["id"]==id:
			return p

@app.get('/posts')
def hello():
	return {"data":my_post}

# @app.post('/createpost')
# def create_post(payload:dict=Body(...)):
# 	print(payload)
# 	return {"title":payload['title'],"content":payload['content']}


@app.post('/posts')
def create_post(post:Post):
	dict_post=post.dict()
	dict_post["id"]=randrange(0,100000000)
	my_post.append(dict_post)
	return {"message":dict_post}


@app.get('/posts/{id}')
def get_post(id:int):
	post=find_post(id)
	return {"data":post}
