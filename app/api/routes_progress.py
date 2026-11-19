import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.jobs import job

progress_router = APIRouter(prefix="/ws", tags=["Progress"])


@progress_router.websocket("/progress/{job_id}")
async def websocket_progress(websocket: WebSocket, job_id: str):
    await websocket.accept()

    # -1 garante que o primeiro estado (revision 0) também seja enviado.
    ultima_revisao = -1

    try:
        while True:
            state = job.get_progress(job_id)

            if state is None:
                await websocket.send_json(
                    {"stage": "error", "error": "Job não encontrado"}
                )
                await websocket.close()
                return

            if state["revision"] != ultima_revisao:
                await websocket.send_json(state)
                ultima_revisao = state["revision"]

            if state["stage"] in {"done", "error"}:
                break

            await asyncio.sleep(0.2)

        await websocket.close()

    except WebSocketDisconnect:
        pass
