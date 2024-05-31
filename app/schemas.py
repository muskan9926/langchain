from pydantic import BaseModel

class Message(BaseModel):
    document_name: str
    collection_name: str


class QuestionInput(BaseModel):
    question: str
    session_id: str

