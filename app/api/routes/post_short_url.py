from fastapi import APIRouter

router = APIRouter()


@router.post("/short_url")
async def post_short_url():
    print("hello world")
    return None