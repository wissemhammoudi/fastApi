from fastapi import FastAPI ,HTTPException, Depends
import uvicorn  # Import uvicorn
from pydantic import BaseModel
from typing import List ,Annotated
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import models 
#FastAPI is a Python class that provides all the functionality for your API.
app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool
class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/questions/")
async def create_question(question: QuestionBase, db: db_dependency):
    db_question = models.Question(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = models.Choice(choice_text=choice.choice_text, is_correct=choice.is_correct, question_id=db_question.id)
        db.add(db_choice)
    db.commit()
@app.get("/questions/{question_id}")
async def get_questions(question_id: int, db: db_dependency):
    result =   db.query(models.Question).filter(models.Question.id == question_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Question not found")
    return result
@app.get("/choices/{question_id}")
async def get_choices(question_id: int, db: db_dependency):
    result = db.query(models.Choice).filter(models.Choice.question_id == question_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="Choice not found")
    return result

# Run the app using uvicorn programmatically
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)