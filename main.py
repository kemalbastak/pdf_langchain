import uvicorn
from core.app import app


@app.get("/hello")
def hello():
    return {"hello": "hello my name"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host='0.0.0.0', reload=True)
