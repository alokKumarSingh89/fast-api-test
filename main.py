from fastapi import FastAPI
from typing import Optional
app = FastAPI()


@app.get('/')
def index():
    return {'message' : 'Hello'}


@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}
