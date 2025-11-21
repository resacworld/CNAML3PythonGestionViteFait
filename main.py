from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from RG import *

app = FastAPI()

@app.get("/")
def root():
    return {"message": "HEllo World"}

# @app.get("/test", response_class=HTMLResponse)
# def test():
#     return "<html><head><title>Test Page</title></head><body><h1>This is a test page</h1></body></html>"

@app.get("/projects")
def projects():
    return mesProjects()