from fastapi import APIRouter

router = APIRouter()

@router.get("/centers")
def get_centers():
    return [
        {"name": "Mysuru Aadhaar Center", "queue": 10},
        {"name": "Bangalore Aadhaar Center", "queue": 25}
    ]
