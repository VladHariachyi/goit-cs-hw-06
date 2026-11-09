from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import socket
from socket_server.server import TCP_IP, TCP_PORT
import json
import uvicorn

app = FastAPI()
FRONTEND_DIR = Path("frontend")
client = None

@app.on_event("startup")
async def startup():
    global client

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((TCP_IP, TCP_PORT))

    print("Connected to Socket TCP server")


@app.on_event("shutdown")
async def shutdown():
    global client

    if client:
        client.close()
        print("Disconnected from Socket TCP server")

@app.get("/")
async def index():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/message")
async def message_page():
    return FileResponse(FRONTEND_DIR / "message.html")

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return FileResponse(
        FRONTEND_DIR / "error.html",
        status_code=404
    )

@app.post("/message")
async def send_message(
    username: str = Form(...),
    message: str = Form(...)
):
    data = {
        "username": username,
        "message": message
    }

    try:
        print("DATA for client: ", json.dumps(data, ensure_ascii=False).encode("utf-8"))
        client.send(
            json.dumps(data, ensure_ascii=False).encode("utf-8")
        )
    except socket.error:
        client.close()

        raise HTTPException(
            status_code=503,
            detail="TCP server is unavailable"
        )

    return {
        "success": True
    }


app.mount(
    "/",
    StaticFiles(directory=FRONTEND_DIR),
    name="frontend"
)

def run():
    uvicorn.run(
        "http_server.server:app",
        host="0.0.0.0",
        port=3000
    )