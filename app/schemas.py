from pydantic import BaseModel,EmailStr,ConfigDict
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
	pass

class CreatePost(PostBase):
	pass

class UserOut(BaseModel):
	email:EmailStr
	id:int
	created_at:datetime

	class Config:
		orm_mode:True

class PostResponse(PostBase):
	id:int
	created_at:datetime
	owner_id:int
	owner:UserOut
	title:str
	content:str
	published:bool=False

	class Config:
		orm_mode:True

class PostOut(PostBase):
	Post:PostResponse
	votes:int

	class Config:
		orm_mode:True

class UserCreate(BaseModel):
	email:EmailStr
	password:str
	created_at:datetime


class UserLogin(BaseModel):
	email:EmailStr
	password:str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
	model_config = ConfigDict(coerce_numbers_to_str=True)

	id:Optional[str]=None


class Vote(BaseModel):
	post_id:int
	dir:conint(le=1)