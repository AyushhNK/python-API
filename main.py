from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app=FastAPI()

class Post(BaseModel):
	title:str
	content:str
	published:bool=True
	rating:int|None=None

@app.get('/')
def hello():
	return {"message":"hello world"}

# @app.post('/createpost')
# def create_post(payload:dict=Body(...)):
# 	print(payload)
# 	return {"title":payload['title'],"content":payload['content']}


@app.post('/createpost')
def create_post(post:Post):
	print(post)
	dict_post=post.dict()
	print(dict_post)
	return {"message":post}