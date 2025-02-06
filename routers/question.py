from fastapi import APIRouter
from fastapi import  HTTPException
from models import QuestionBase,Question,Choice
from database import db_dependency

# Create router instance for question-related endpoints
router = APIRouter( prefix="/question",tags=["questions"])


@router.get("/")
async def get_questions(db: db_dependency):
    result = db.query(Question).all()
    return result

@router.post("/")
async def create_question(question: QuestionBase, db: db_dependency):
    """
    Create a new question with associated choices
    Args:
        question (QuestionBase): Question data including choices
        db (Session): Database session dependency
    Returns:
        None
    """
    # Create new Question record
    db_question = Question(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    # Create Choice records for each choice in the question
    for choise in question.choices:
        db_choise = Choice(
            choice_text=choise.choice_text, 
            is_correct=choise.is_correct, 
            question_id=db_question.id
        )
        db.add(db_choise)
    db.commit()

@router.get("/{question_text}")
async def get_question(question_text: str, db: db_dependency):
    """
    Get a specific question by ID
    Args:
        question_id (int): ID of the question to retrieve
        db (Session): Database session dependency
    Returns:
        Question: Question object if found
    Raises:
        HTTPException: If question is not found
    """
    # Query database for question matching the ID
    result = db.query(Question).filter(Question.question_text.ilike(f"%{question_text}%")).limit(5).all()
    # Raise 404 if question not found
    if not result:
        raise HTTPException(status_code=404, detail="Question not found")
    return result
@router.delete("/{question_id}")
async def delete_question(question_id: int, db: db_dependency):
    result = db.query(Question).filter(Question.id == question_id).first()
    choices = db.query(Choice).filter(Choice.question_id == question_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="Question not found")
    for choice in choices:
        db.delete(choice)
    db.delete(result)
    db.commit()

@router.patch("/{question_id}")
async def update_question(question_id: int, question: str, db: db_dependency):
    result = db.query(Question).filter(Question.id == question_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Question not found")
    result.question_text = question
    db.commit()





