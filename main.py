from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from Backend.chat import router
from fastapi.middleware.cors import CORSMiddleware
from Backend.rag import rag
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(rag)
app.include_router(router)

@app.get("/")
def serve_frontend():
    return FileResponse("Frontend/index.html")

app.mount("/static", StaticFiles(directory="Frontend"), name="static")
