from fastapi import APIRouter

index = APIRouter(tags=["Health"])

@index.get("/health")
def check_health():
    return {"msg": "Server up to you and for you", "code": 200}
