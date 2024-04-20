from fastapi import FastAPI
from fastapi.params import Body

app=FastAPI()

@app.get('/')
def hello():
	return {"message":"hello world"}

@app.post('/createpost')
def create_post(payload:dict=Body(...)):
	print(payload)
	return {"title":payload['title'],"content":payload['content']}