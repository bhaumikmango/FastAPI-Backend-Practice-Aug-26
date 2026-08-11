from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get('/')
def root():
    return {"message" : "Welcome to the API"}

@app.get('/')
def root():
    return {"message" : "Hello World"} #will skip this and use the first match for the certain path

@app.get('/posts')
def get_posts():
    return {"Data" : "Content of Posts"}

@app.post('/create/posts')
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"new_post":f"Title: {payload['title']}; Content: {payload['content']}"}