import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.jobs import job

progress_router = APIRouter(prefix="/ws", tags=["Progress"])


@progress_router.websocket("/progress/{job_id}")
async def websocket_progress(websocket: WebSocket, job_id: str):
    await websocket.accept()

    try:
        last_percent = -1

        while True:
            data = job.get_progress(job_id)

            if not data:
                await websocket.send_json({"stage": "unknown", "percent": 0})
                await asyncio.sleep(1)
                continue

            if data["percent"] != last_percent:
                await websocket.send_json(data)
                last_percent = data["percent"]

            if data["stage"] == "done":
                break

            await asyncio.sleep(0.5)

    except WebSocketDisconnect:
        pass
