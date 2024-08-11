import uvicorn

from fastapi import FastAPI


app = FastAPI(title="OnlineShop")

if __name__ == "__main__":
    uvicorn.run(
        __name__ + ":app",
        host='127.0.0.1',
        port=8000,
        reload=True
    )