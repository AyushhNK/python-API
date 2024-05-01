from pydantic import BaseModel,EmailStr
from datetime import datetime

class PostBase(BaseModel):
	title:str
	content:str
	published:bool=False

class CreatePost(PostBase):
	pass

class PostResponse(PostBase):
	created_at:datetime

class UserCreate(BaseModel):
	email:EmailStr
	password:str
	created_at:datetime

class UserOut(BaseModel):
	email:EmailStr
	id:int
	created_at:datetime

class UserLogin(BaseModel):
	email:EmailStr
	password:str

class TokenData(BaseModel):
	id:str|None=None