import sys
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json
import asyncio

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agents.tutor_agent import TutorAgent

app = FastAPI(title="C Tutor Web", version="1.0.0")

# 初始化智能体
tutor_agent = TutorAgent()


# 存储WebSocket连接
class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)


manager = ConnectionManager()

# 提供静态文件
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def read_index():
    return FileResponse("app/static/index.html")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # 接收前端消息
            data = await websocket.receive_text()
            message_data = json.loads(data)

            if message_data["type"] == "user_message":
                response = await tutor_agent.process_user_message(
                    message_data["content"],
                    message_data.get("code_context", {})
                )
                await manager.send_personal_message(json.dumps(response), websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "python_version": "3.9.13", "service": "C Tutor Web"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)