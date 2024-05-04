from pydantic.v1 import BaseSettings


class Setting(BaseSettings):
	postgres_password:str
	secret_key:str
	algorithm:str
	access_token_expire_minutes:int

	class Config:
		env_file=".env"

settings=Setting()