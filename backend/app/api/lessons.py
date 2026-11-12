from fastapi import APIRouter, Depends

router = APIRouter()

lessons = [
    {
        "id": 1, 
        "title": "Die Farben",
        "level": "A1.2",
        "vocabulary": ["rot", "blau", "grün", "gelb", "schwarz", "weiß"],
    }
]


@router.get("/")
def get_lessons():
    return lessons

@router.get("/{lesson_id}")
def get_lesson(lesson_id: int):
    for lesson in lessons:
        if lesson["id"] == lesson_id:
            return lesson
    return {"error": "Lesson not found"}