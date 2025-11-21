import uvicorn
import os

if __name__ == "__main__":
    print(os.getcwd())
    os.chdir(os.getcwd())
    uvicorn.run("main:app", port=8000, reload=True)