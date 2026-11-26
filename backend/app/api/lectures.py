import json
from pathlib import Path

from fastapi import APIRouter, HTTPException
from app.schemas.lecture import Lecture



router = APIRouter()

LECTURES_DIRECTORY = Path(__file__).resolve().parents[1] / "data" / "lectures"


def load_lectures() -> list[Lecture]:
    lectures = []
    for lecture_file in sorted(LECTURES_DIRECTORY.glob("*.json")):
        lecture_data = json.loads(lecture_file.read_text(encoding="utf-8"))
        lectures.append(Lecture.model_validate(lecture_data))
    return lectures


lectures = load_lectures()



@router.get("/", response_model=list[Lecture])
def get_lectures():
    return lectures

@router.get("/{lecture_id}", response_model=Lecture)
def get_lecture(lecture_id: int):
    for lecture in lectures:
        if lecture.id == lecture_id:
            return lecture
    raise HTTPException(status_code=404, detail="Lecture not found")
