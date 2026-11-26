from enum import Enum
from typing import Annotated, Literal

from pydantic import BaseModel, Field, model_validator


ITEMS_PER_EXERCISE = 10


class ExerciseType(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    MATCHING = "matching"
    FILL_GAPS = "fill_gaps"
    WORD_ORDERING = "word_ordering"
    READING_COMPREHENSION = "reading_comprehension"
    SENTENCE_CONSTRUCTION = "sentence_construction"
    FREE_WRITING = "free_writing"


class MultipleChoiceItem(BaseModel):
    prompt: str
    options: list[str]
    correct_option: int = Field(ge=0)


class MultipleChoiceExercise(BaseModel):
    type: Literal["multiple_choice"]
    items: list[MultipleChoiceItem] = Field(
        min_length=ITEMS_PER_EXERCISE, max_length=ITEMS_PER_EXERCISE
    )


class TrueFalseItem(BaseModel):
    statement: str
    is_true: bool


class TrueFalseExercise(BaseModel):
    type: Literal["true_false"]
    items: list[TrueFalseItem] = Field(
        min_length=ITEMS_PER_EXERCISE, max_length=ITEMS_PER_EXERCISE
    )


class MatchingItem(BaseModel):
    word: str
    image: str


class MatchingExercise(BaseModel):
    type: Literal["matching"]
    items: list[MatchingItem] = Field(
        min_length=ITEMS_PER_EXERCISE, max_length=ITEMS_PER_EXERCISE
    )


class FillGapItem(BaseModel):
    sentence: str
    accepted_answers: list[str]
    word_bank: list[str] = Field(default_factory=list)


class FillGapsExercise(BaseModel):
    type: Literal["fill_gaps"]
    items: list[FillGapItem] = Field(
        min_length=ITEMS_PER_EXERCISE, max_length=ITEMS_PER_EXERCISE
    )


class WordOrderingItem(BaseModel):
    words: list[str]
    correct_sentence: str


class WordOrderingExercise(BaseModel):
    type: Literal["word_ordering"]
    items: list[WordOrderingItem] = Field(
        min_length=ITEMS_PER_EXERCISE, max_length=ITEMS_PER_EXERCISE
    )


class ReadingComprehensionItem(BaseModel):
    question: str
    accepted_answers: list[str]


class ReadingComprehensionExercise(BaseModel):
    type: Literal["reading_comprehension"]
    passage: str
    items: list[ReadingComprehensionItem] = Field(
        min_length=ITEMS_PER_EXERCISE, max_length=ITEMS_PER_EXERCISE
    )


class SentenceConstructionItem(BaseModel):
    instruction: str
    required_words: list[str] = Field(default_factory=list)
    sample_answer: str


class SentenceConstructionExercise(BaseModel):
    type: Literal["sentence_construction"]
    items: list[SentenceConstructionItem] = Field(
        min_length=ITEMS_PER_EXERCISE, max_length=ITEMS_PER_EXERCISE
    )


class FreeWritingItem(BaseModel):
    topic: str
    instructions: str
    rubric: list[str]
    image: str | None = None


class FreeWritingExercise(BaseModel):
    type: Literal["free_writing"]
    items: list[FreeWritingItem] = Field(
        min_length=ITEMS_PER_EXERCISE, max_length=ITEMS_PER_EXERCISE
    )


ExerciseBlock = Annotated[
    MultipleChoiceExercise
    | TrueFalseExercise
    | MatchingExercise
    | FillGapsExercise
    | WordOrderingExercise
    | ReadingComprehensionExercise
    | SentenceConstructionExercise
    | FreeWritingExercise,
    Field(discriminator="type"),
]


class GeneratedExerciseSet(BaseModel):
    lecture_id: int
    exercises: list[ExerciseBlock] = Field(
        min_length=len(ExerciseType), max_length=len(ExerciseType)
    )

    @model_validator(mode="after")
    def require_one_block_per_type(self):
        actual_types = [exercise.type for exercise in self.exercises]
        expected_types = {exercise_type.value for exercise_type in ExerciseType}
        if len(set(actual_types)) != len(expected_types) or set(actual_types) != expected_types:
            raise ValueError("Provide exactly one exercise block for each exercise type")
        return self
