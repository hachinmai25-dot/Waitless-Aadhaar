from fastapi import APIRouter

router = APIRouter()

@router.post("/book-slot")
def book_slot(data: dict):
    return {
        "message": "Slot booked successfully",
        "details": data
    }
