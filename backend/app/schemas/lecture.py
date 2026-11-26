from pydantic import BaseModel, Field


class VocabularyWord(BaseModel):
    word: str
    translation: str
    article: str | None = None


class Expression(BaseModel):
    expression: str
    translation: str


class GrammarExample(BaseModel):
    german: str
    english: str


class GrammarRule(BaseModel):
    title: str
    explanation: str
    examples: list[GrammarExample] = Field(default_factory=list)


class Lecture(BaseModel):
    id: int
    title: str
    level: str | None = None
    vocab: list[VocabularyWord] = Field(default_factory=list)
    expressions: list[Expression] = Field(default_factory=list)
    grammar_rules: list[GrammarRule] = Field(default_factory=list)
