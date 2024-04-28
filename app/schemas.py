from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
	title:str
	content:str
	published:bool=False

class CreatePost(PostBase):
	pass

class PostResponse(PostBase):
	created_at:datetime