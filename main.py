from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from routers import sign
from routers import todo

app = FastAPI()

app.mount("/public", StaticFiles(directory="public"), name="public")

@app.get("/", response_class=HTMLResponse)
def read_root():
    return FileResponse("./public/index.html")  

app.include_router(sign.router, prefix="/sign", tags=["sign"])
app.include_router(todo.router, prefix="/todo", tags=["todo"])