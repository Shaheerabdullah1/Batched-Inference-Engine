from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.core.batch_worker import batch_manager
from app.core.batch_manager import BatchRequest
from app.schemas.models import GenerateRequest

router = APIRouter()


@router.post("/generate")
async def generate(req: GenerateRequest):

    batch_req = BatchRequest(req.prompt)

    # add to batch queue
    await batch_manager.add_request(batch_req)

    async def token_generator():
        while True:
            token = await batch_req.queue.get()

            if token == "[DONE]":
                yield "data: [DONE]\n\n"
                break

            yield f"data: {token}\n\n"

    return StreamingResponse(
        token_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@router.get("/health")
def health():
    return {"status": "ok"}