from fastapi import APIRouter

router = APIRouter()

@router.post("/register")
def register_user(data: dict):
    return {
        "message": "User registered successfully",
        "user": data
    }
