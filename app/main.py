from fastapi import FastAPI,Response,status,HTTPException
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


def find_index(id):
	for i,p in enumerate(my_post):
		if p["id"]==id:
			return i

@app.get('/posts')
def hello():
	return {"data":my_post}

# @app.post('/createpost')
# def create_post(payload:dict=Body(...)):
# 	print(payload)
# 	return {"title":payload['title'],"content":payload['content']}


@app.post('/posts',status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
	dict_post=post.dict()
	dict_post["id"]=randrange(0,100000000)
	my_post.append(dict_post)

	return {"message":dict_post}


@app.get('/posts/{id}')
def get_post(id:int,response:Response):
	post=find_post(id)
	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with id:{id} not found")
		# response.status_code=status.HTTP_404_NOT_FOUND
		# return {"detail":f"the post with id:{id} not found"}
	return {"data":post}


@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
	index=find_index(id)
	if index==None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with id:{id} not found")
	my_post.pop(index)
	return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id:int,post:Post):
	index=find_index(id)
	if index==None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with id:{id} not found")
	post_dict=post.dict()
	post_dict["id"]=id
	my_post[index]=post_dict
	return {"data":post}

